from typing import List , Optional , Tuple , Callable
from abc import ABC , abstractmethod
from pydantic import BaseModel , confloat , conint
from .locale_en import sentences , words , cleanup
from .keys import * # import the k_*** keys
from ..defs import *
import random
import math
import re
from ..schema import *

def get_word(key):
    r = words[key]    
    if(isinstance(r,list)):
        return random.choice(r)
    return r

class Descriptor():

    def recurse(self,
                class_method:Callable,
                children:list,
                style_guide:StyleGuide,
                flavour:DeclarationFlavour=DeclarationFlavour.NONE,
                declarations:DeclarationsMask=DeclarationsMask.ALL,
                limit:Optional[int]=None):
        descs = []
        declarations_ = []
        count = 1
        for child in children:
            if limit is not None and count>limit:
                break 
            desc , flavour , declaration_ = class_method(child,style_guide,flavour,declarations)
            if desc is not None:
                declarations_.append(declaration_)
                descs.append(desc)
        # update cross-level declarations, after the fact
        for declaration_  in declarations_:
            declarations &= declaration_
        return descs , flavour , declarations    

    ##############
    #
    # ENVELOPE
    #
    ##############

    def desc_envelope(self,
             envelope:Envelope,
             style_guide:StyleGuide,
             flavour:DeclarationFlavour=DeclarationFlavour.NONE,
             declarations:DeclarationsMask=DeclarationsMask.ALL
             )->Tuple[Optional[str],DeclarationFlavour,DeclarationsMask]:
        return None , flavour , declarations
    
    ##############
    #
    # LFO
    #
    ##############

    
    def desc_lfo(self,
             lfo:LFO,
             style_guide:StyleGuide,
             flavour:DeclarationFlavour=DeclarationFlavour.NONE,
             declarations:DeclarationsMask=DeclarationsMask.ALL,
             )->Tuple[Optional[str],DeclarationFlavour,DeclarationsMask]:
        return None,flavour,declarations   
    
    ##############
    #
    # OSC SHAPE
    #
    ##############


    def desc_osc_shape(self,
             shape:OscillatorShape,
             style_guide:StyleGuide,
             flavour:DeclarationFlavour=DeclarationFlavour.NONE,
             declarations:DeclarationsMask=DeclarationsMask.ALL,
             )->Tuple[Optional[str],DeclarationFlavour,DeclarationsMask]:

        # select proper formats
        compositing = sentences[k_shape][k_compositing][style_guide.value]

        # select which flavour of mix declaration we will take ...
        compose_keys = self._filter_osc_shape_compositing_keys(shape,compositing,declarations)

        # pick compisiting formats and strings
        flavour_key = random.choice( compose_keys ) 
        compose_loc = random.choice( compositing[flavour_key] )

        if declarations & DeclarationsMask.SHAPE_VOLUME == 0: # should not happen
            flavour = flavour & (DeclarationFlavour.ALL - DeclarationFlavour.GRP_SHAPE_VOLUME_ALL) | DeclarationFlavour.SHAPE_VOLUME_NONE

        # update declarations: if we used "vol_*" we can tell the children that its been used
        has_volume   = flavour_key in [k_comp_shape_default] and (flavour & DeclarationFlavour.GRP_SHAPE_VOLUME_PRESENT != 0)
        declarations = declarations & (DeclarationsMask.ALL - DeclarationsMask.SHAPE_VOLUME) if has_volume  else declarations

        # update the flavour with what we will actually be outputting (some compositing may not include the volume)
        if "{volume_desc}" not in compose_loc:
            flavour = flavour & ( DeclarationFlavour.ALL - DeclarationFlavour.GRP_SHAPE_VOLUME_ALL ) | DeclarationFlavour.SHAPE_VOLUME_NONE

        # recurse
        # no recursion

        # compose sentence
        waveform_name = get_word(shape.waveform.value)
        waveform_width = get_word(shape.width.value) if shape.width is not None else None
        waveform_width = f"{waveform_width} " if waveform_width is not None else ""
        volume_desc , flavour = self._get_osc_shape_volume_desc(shape,style_guide,flavour,declarations) # in case we need it
        shape_desc = compose_loc.format(waveform_name=waveform_name,volume_desc=volume_desc,waveform_width=waveform_width)

        return shape_desc , flavour , declarations   
    
    def _get_osc_shape_volume_desc(self,
                                   shape:OscillatorShape,
                         style_guide:StyleGuide,
                         flavour:DeclarationFlavour,
                         declarations:DeclarationsMask)->Tuple[str,DeclarationFlavour]:
        
        if flavour & DeclarationFlavour.SHAPE_VOLUME_NUMBER:
            flavour = flavour & (DeclarationFlavour.ALL - DeclarationFlavour.GRP_SHAPE_VOLUME_ALL) | DeclarationFlavour.SHAPE_VOLUME_NUMBER
            vol_value = self._get_osc_shape_volume_desc_as_number(shape,style_guide,flavour,declarations)
            compositing_vol = random.choice( sentences[k_shape][k_comp_shape_vol][style_guide.value] )
            volume_value = compositing_vol.format(volume_value=vol_value)
            return volume_value , flavour
        elif flavour & DeclarationFlavour.SHAPE_VOLUME_NONE:
            flavour = flavour & (DeclarationFlavour.ALL - DeclarationFlavour.GRP_SHAPE_VOLUME_ALL) | DeclarationFlavour.SHAPE_VOLUME_NONE
            volume_value = ""
            return volume_value , flavour
        else:
            # we haven't pick a volume flavour yet, pick one now
            flavours = [ 
                DeclarationFlavour.SHAPE_VOLUME_NONE ,
                DeclarationFlavour.SHAPE_VOLUME_NUMBER ,
            ]
            flavour_select = random.choice(flavours)
            flavour = flavour & (DeclarationFlavour.ALL - DeclarationFlavour.GRP_SHAPE_VOLUME_ALL) | flavour_select
            return self._get_osc_shape_volume_desc(shape,style_guide=style_guide,flavour=flavour,declarations=declarations)    

    def _get_osc_shape_volume_desc_as_number(self,
                         shape:OscillatorShape,
                         style_guide:StyleGuide,
                         flavour:DeclarationFlavour,
                         declarations:DeclarationsMask)->str:
        match style_guide:
            case StyleGuide.BASIC:
                volume = f"{round(100.0*shape.volume)}"
                return volume
            case StyleGuide.SUCCINT:
                volume = f"{round(100.0*shape.volume)}%"
                return volume
            case StyleGuide.CONCISE:
                volume = f"{round(100.0*shape.volume)}%"
                return volume
            case StyleGuide.DETAILED:
                volume = f"{round(100.0*shape.volume,2)}%"
                return volume
            case StyleGuide.SPECIFICATION:
                volume = f"{round(100.0*shape.volume,2)}%"
                return volume
        
    def _filter_osc_shape_compositing_keys(self,shape:OscillatorShape,compositing:dict,declarations:DeclarationsMask):
        # lets add the volume info if we want it
        compositing_copy = compositing.copy()
        assert len(compositing_copy) > 0
        return list(compositing_copy.keys())
    
    ##############
    #
    # OSC/OP
    #
    ##############

    def desc_osc_or_op(self,
             oscillator: Oscillator|Operator,
             style_guide:StyleGuide,
             flavour:DeclarationFlavour=DeclarationFlavour.NONE,
             declarations:DeclarationsMask=DeclarationsMask.ALL,
             )->Tuple[Optional[str],DeclarationFlavour,DeclarationsMask]:  

        if isinstance(oscillator,Oscillator):
            return self.desc_osc(oscillator,style_guide,flavour,declarations)  
        elif isinstance(oscillator,Operator):
            return self.desc_op(oscillator,style_guide,flavour,declarations)  
        
    ##############
    #
    # OSC
    #
    ##############

    # when we used balanced writing, we won't output the volumes ...
    def desc_osc(self,
             oscillator: Oscillator,
             style_guide:StyleGuide,
             flavour:DeclarationFlavour=DeclarationFlavour.NONE,
             declarations:DeclarationsMask=DeclarationsMask.ALL,
             )->Tuple[Optional[str],DeclarationFlavour,DeclarationsMask]:

        # select proper formats
        compositing = sentences[k_oscillator][k_compositing][style_guide.value]
        osc_type    = sentences[k_oscillator][k_osc_type]
        osc_article = sentences[k_oscillator][k_osc_article]
        comp_osc_id = sentences[k_oscillator][k_comp_osc_id][style_guide.value]

        # select which flavour of mix declaration we will take ...
        compose_keys = self._filter_osc_compositing_keys(oscillator,compositing,flavour,declarations)
        
        # pick compisiting formats and strings
        flavour_key = random.choice( compose_keys ) 
        compose_loc = random.choice( compositing[flavour_key] )
        compose_id  = random.choice( comp_osc_id[flavour_key] )
        osc_type    = random.choice( osc_type[k_comp_osc_sub] if oscillator.sub else osc_type[k_comp_osc_sub_not])
        osc_article = random.choice( osc_article[k_comp_osc_sub] if oscillator.sub else osc_article[k_comp_osc_sub_not])

        # update flavour according to existing declarations
        if declarations & DeclarationsMask.OSC_VOLUME == 0:
            flavour = flavour & (DeclarationFlavour.ALL - DeclarationFlavour.GRP_OSC_VOLUME_ALL) | DeclarationFlavour.OSC_VOLUME_NONE
        if declarations & DeclarationsMask.SHAPE_VOLUME == 0: # should not happen
            flavour = flavour & (DeclarationFlavour.ALL - DeclarationFlavour.GRP_SHAPE_VOLUME_ALL) | DeclarationFlavour.SHAPE_VOLUME_NONE

        # update declarations: considerations that impact children
        has_osc_vol = True # at this point lets consider OSC_VOLUME declared
        declarations = declarations & (DeclarationsMask.ALL - DeclarationsMask.OSC_VOLUME) if has_osc_vol  else declarations
        # lets not show the shape level if the oscillator doesn't blend shapes
        dont_use_shape_vol = len(oscillator.shapes)<2 or random.random()>0.5
        declarations = declarations & (DeclarationsMask.ALL - DeclarationsMask.SHAPE_VOLUME) if dont_use_shape_vol  else declarations        

        # update the flavour and declarations with trhe actual situation (some strings may not include replacement patterns)
        if flavour & (DeclarationFlavour.OSC_VOLUME_NUMBER|DeclarationFlavour.OSC_VOLUME_TEXT_POST) !=0 and "{volume_desc_post}" not in compose_loc \
        or flavour & DeclarationFlavour.OSC_VOLUME_TEXT_PRE !=0 and "{volume_desc_pre}" not in compose_loc:
            flavour = flavour & ( DeclarationFlavour.ALL - DeclarationFlavour.GRP_OSC_VOLUME_ALL ) | DeclarationFlavour.OSC_VOLUME_NONE
            declarations = declarations & (DeclarationsMask.ALL - DeclarationsMask.OSC_VOLUME)

        # sub-compositing
        vol_desc_post , vol_desc_pre ,flavour = self.desc_osc_volume(oscillator,style_guide,flavour,declarations)
        desc_tuning ,flavour = self.desc_osc_tuning(oscillator,style_guide,flavour,declarations)
        shapes_desc , flavour = self.desc_osc_shapes(oscillator,style_guide,flavour,declarations)
        osc_id = compose_id.format(rank=oscillator.rank) if flavour & DeclarationFlavour.OSC_OTHER_WITH_ID else ""
        
        osc_desc = compose_loc.format(shapes_desc=shapes_desc,
                                        volume_desc_post=vol_desc_post,
                                        volume_desc_pre=vol_desc_pre,
                                        osc_type=osc_type,
                                        osc_article=osc_article,
                                        tuning_desc=desc_tuning,
                                        osc_id=osc_id)
        
        return osc_desc , flavour , declarations
    
    def _filter_osc_compositing_keys(self,oscillator:Oscillator,
                                     compositing:dict,
                                     flavour:DeclarationFlavour,
                                     declarations:DeclarationsMask):
        # lets add the volume info if we want it
        compositing_copy = compositing.copy()
        if flavour & DeclarationFlavour.OSC_OTHER_FOR_OPERATOR == 0:
            compositing_copy.pop(k_comp_osc_for_operator,None)
            if len(oscillator.shapes)==1:
                compositing_copy.pop(k_comp_osc_plural,None)
            else:
                compositing_copy.pop(k_comp_osc_singular,None)
        else:
            compositing_copy.pop(k_comp_osc_singular,None)
            compositing_copy.pop(k_comp_osc_plural,None)
        assert len(compositing_copy) > 0
        return list(compositing_copy.keys())

    def desc_osc_volume(self,
                        oscillator:Oscillator,
                         style_guide:StyleGuide,
                         flavour:DeclarationFlavour,
                         declarations:DeclarationsMask)->Tuple[str,DeclarationFlavour]:
        
        if flavour & DeclarationFlavour.OSC_VOLUME_NUMBER:
            flavour = flavour & (DeclarationFlavour.ALL - DeclarationFlavour.GRP_OSC_VOLUME_ALL) | DeclarationFlavour.OSC_VOLUME_NUMBER
            vol_value = self._get_osc_volume_desc_as_number(oscillator,style_guide,flavour,declarations)
            if style_guide.value not in sentences[k_oscillator][k_comp_osc_vol_number]:
                return "" , "" , flavour & (DeclarationFlavour.ALL - DeclarationFlavour.GRP_OSC_VOLUME_ALL) | DeclarationFlavour.OSC_VOLUME_NONE
            compositing_vol = random.choice( sentences[k_oscillator][k_comp_osc_vol_number][style_guide.value] )
            vol_desc_post = compositing_vol.format(volume_value=vol_value)
            vol_desc_pre  = ""
            return vol_desc_post , vol_desc_pre , flavour
        elif flavour & DeclarationFlavour.OSC_VOLUME_TEXT_POST:
            flavour = flavour & (DeclarationFlavour.ALL - DeclarationFlavour.GRP_OSC_VOLUME_ALL) | DeclarationFlavour.OSC_VOLUME_TEXT_POST
            vol_text = self._get_osc_volume_desc_as_text(oscillator,style_guide,flavour,declarations)
            if style_guide.value not in sentences[k_oscillator][k_comp_osc_vol_number]:
                return "" , "" , flavour & (DeclarationFlavour.ALL - DeclarationFlavour.GRP_OSC_VOLUME_ALL) | DeclarationFlavour.OSC_VOLUME_NONE
            compositing_vol = random.choice( sentences[k_oscillator][k_comp_osc_vol_text_post][style_guide.value] )
            vol_desc_post = compositing_vol.format(volume_text=vol_text)
            vol_desc_pre  = ""
            return vol_desc_post , vol_desc_pre , flavour
        elif flavour & DeclarationFlavour.OSC_VOLUME_TEXT_PRE:
            flavour = flavour & (DeclarationFlavour.ALL - DeclarationFlavour.GRP_OSC_VOLUME_ALL) | DeclarationFlavour.OSC_VOLUME_TEXT_PRE
            vol_text = self._get_osc_volume_desc_as_text(oscillator,style_guide,flavour,declarations)
            if style_guide.value not in sentences[k_oscillator][k_comp_osc_vol_number]:
                return "" , "" , flavour & (DeclarationFlavour.ALL - DeclarationFlavour.GRP_OSC_VOLUME_ALL) | DeclarationFlavour.OSC_VOLUME_NONE
            compositing_vol = random.choice( sentences[k_oscillator][k_comp_osc_vol_text_pre][style_guide.value] )
            vol_desc_post = ""
            vol_desc_pre  = compositing_vol.format(volume_text=vol_text)
            return vol_desc_post , vol_desc_pre, flavour
        elif flavour & DeclarationFlavour.OSC_VOLUME_NONE:
            flavour = flavour & (DeclarationFlavour.ALL - DeclarationFlavour.GRP_OSC_VOLUME_ALL) | DeclarationFlavour.OSC_VOLUME_NONE
            vol_desc_post = ""
            vol_desc_pre  = ""
            return vol_desc_post , vol_desc_pre , flavour
        else:
            # we haven't pick a volume flavour yet, pick one now
            flavours = [ 
                DeclarationFlavour.OSC_VOLUME_NONE ,
                DeclarationFlavour.OSC_VOLUME_NUMBER ,
                DeclarationFlavour.OSC_VOLUME_TEXT_POST ,
                DeclarationFlavour.OSC_VOLUME_TEXT_PRE
            ]
            flavour_select = random.choice(flavours)
            flavour = flavour & (DeclarationFlavour.ALL - DeclarationFlavour.GRP_OSC_VOLUME_ALL) | flavour_select
            return self.desc_osc_volume(oscillator,style_guide=style_guide,flavour=flavour,declarations=declarations)     
        
    def _get_osc_volume_desc_as_number(self,
                                   oscillator:Oscillator,
                                   style_guide:StyleGuide,
                                   flavour:DeclarationFlavour,
                                   declarations:DeclarationsMask)->str:
        match style_guide:
            case StyleGuide.BASIC:
                volume = round(100.0*oscillator.volume)
                return volume
            case StyleGuide.SUCCINT:
                volume = f"{round(100.0*oscillator.volume)}%"
                return volume
            case StyleGuide.CONCISE:
                volume = f"{round(100.0*oscillator.volume)}%"
                return volume
            case StyleGuide.DETAILED:
                volume = f"{round(100.0*oscillator.volume,2)}%"
                return volume
            case StyleGuide.SPECIFICATION:
                volume = f"{round(100.0*oscillator.volume,2)}%"
                return volume
            
    def _get_osc_volume_desc_as_text(self,
                                     oscillator:Oscillator,
                                 style_guide:StyleGuide,
                                 flavour:DeclarationFlavour,
                                 declarations:DeclarationsMask)->str:

        if oscillator.volume==0.0:
            volume_group = 0 
        elif oscillator.volume<1.0:
            volume_group = math.ceil(oscillator.volume/20.0) # 1,5
        else:
            volume_group = 6
        
        match style_guide:
            case StyleGuide.BASIC:
                volume = get_word(f"k_volume_grp{volume_group}")
                return volume
            case StyleGuide.SUCCINT:
                volume = get_word(f"k_volume_grp{volume_group}")
                return volume
            case StyleGuide.CONCISE:
                volume = get_word(f"k_volume_grp{volume_group}")
                return volume
            case StyleGuide.DETAILED:
                volume = get_word(f"k_volume_grp{volume_group}")
                return volume
            case StyleGuide.SPECIFICATION:
                volume = get_word(f"k_volume_grp{volume_group}")
                return volume       
                
    def desc_osc_tuning(self,
                        oscillator:Oscillator,
                         style_guide:StyleGuide,
                         flavour:DeclarationFlavour,
                         declarations:DeclarationsMask)->Tuple[str,DeclarationFlavour]:
        
        if flavour & DeclarationFlavour.OSC_TUNING_PITCH:
            flavour = flavour & (DeclarationFlavour.ALL - DeclarationFlavour.GRP_OSC_TUNING_ALL) | DeclarationFlavour.OSC_TUNING_PITCH
            tuning_coarse , tuning_fine = self.osc_tuning_values(oscillator,style_guide,flavour,declarations)
            if tuning_coarse == "" and tuning_fine == "":
                return "" , flavour
            if style_guide.value not in sentences[k_oscillator][k_comp_osc_tuning]:
                return "" , flavour & (DeclarationFlavour.ALL - DeclarationFlavour.GRP_OSC_TUNING_ALL) | DeclarationFlavour.OSC_TUNING_NONE
            compositing_tuning = random.choice( sentences[k_oscillator][k_comp_osc_tuning][style_guide.value] )
            tuning_val = compositing_tuning.format(tuning_coarse=tuning_coarse,tuning_fine=tuning_fine,osc_i=oscillator.rank)
            return tuning_val , flavour
        elif flavour & DeclarationFlavour.OSC_TUNING_OCT:
            flavour = flavour & (DeclarationFlavour.ALL - DeclarationFlavour.GRP_OSC_TUNING_ALL) | DeclarationFlavour.OSC_TUNING_OCT
            tuning_coarse , tuning_fine = self.osc_tuning_values(oscillator,style_guide,flavour,declarations)
            if tuning_coarse == "" and tuning_fine == "":
                return "" , flavour
            if style_guide.value not in sentences[k_oscillator][k_comp_osc_tuning]:
                return "" , flavour & (DeclarationFlavour.ALL - DeclarationFlavour.GRP_OSC_TUNING_ALL) | DeclarationFlavour.OSC_TUNING_NONE
            compositing_tuning = random.choice( sentences[k_oscillator][k_comp_osc_tuning][style_guide.value] )
            tuning_val = compositing_tuning.format(tuning_coarse=tuning_coarse,tuning_fine=tuning_fine,osc_i=oscillator.rank)
            return tuning_val , flavour
        elif flavour & DeclarationFlavour.OSC_TUNING_NONE:
            flavour = flavour & (DeclarationFlavour.ALL - DeclarationFlavour.GRP_OSC_TUNING_ALL) | DeclarationFlavour.OSC_TUNING_NONE
            return "" , flavour
        else:
            # we haven't pick a volume flavour yet, pick one now
            flavours = [ 
                DeclarationFlavour.OSC_TUNING_NONE ,
                DeclarationFlavour.OSC_TUNING_PITCH ,
                DeclarationFlavour.OSC_TUNING_OCT ,
            ]
            flavour_select = random.choice(flavours)
            flavour = flavour & (DeclarationFlavour.ALL - DeclarationFlavour.GRP_OSC_TUNING_ALL) | flavour_select
            return self.desc_osc_tuning(oscillator,style_guide=style_guide,flavour=flavour,declarations=declarations)                   

    def osc_tuning_values(self,oscillator:Oscillator,style_guide:StyleGuide,flavour:DeclarationFlavour,declarations:DeclarationsMask)->Tuple[str,str]:

        osc_i = oscillator.rank
        if not oscillator.sub:
            tune_coarse = oscillator.tune_coarse
            tune_fine   = oscillator.tune_fine
        else:
            tune_coarse = oscillator.sub_octave
            tune_fine   = None
        if flavour & DeclarationFlavour.OSC_TUNING_PITCH:
            if style_guide.value not in sentences[k_oscillator][k_comp_osc_tuning_pitch]:
                return "",""
            comp_tuning_coarse , comop_tuning_fine = random.choice( sentences[k_oscillator][k_comp_osc_tuning_pitch][style_guide.value] )
            tune_coarse_sign = (f"{tune_coarse}" if tune_coarse==0 else f"{tune_coarse:+}").format(tune_coarse=tune_coarse) if tune_coarse is not None else None
            tune_coarse_str = comp_tuning_coarse.format(tune_coarse=tune_coarse_sign) if tune_coarse_sign is not None else ""
            tune_fine_sign = (f"{tune_fine:.2}" if tune_fine==0 else f"{tune_fine:+.2}").format(tune_fine=round(tune_fine,2)) if tune_fine is not None else None
            tune_fine_str   = comop_tuning_fine.format(tune_fine=tune_fine_sign) if tune_fine_sign is not None and tune_fine != 0.0 else ""
            return tune_coarse_str , tune_fine_str
        else: 
            if style_guide.value not in sentences[k_oscillator][k_comp_osc_tuning_oct]:
                return "",""
            comp_tuning_coarse , comop_tuning_fine = random.choice( sentences[k_oscillator][k_comp_osc_tuning_oct][style_guide.value] )
            tune_coarse_sign = (f"{tune_coarse}" if tune_coarse==0 else f"{tune_coarse:+}").format(tune_coarse=round(tune_coarse/12.0)) if tune_coarse is not None else None
            tune_coarse_str = comp_tuning_coarse.format(tune_coarse=tune_coarse_sign) if tune_coarse_sign is not None else ""
            tune_fine_sign = (f"{tune_fine:.2}" if tune_fine==0 else f"{tune_fine:+.2}").format(tune_fine=round(tune_fine/12.0*100.0,2)) if tune_fine is not None else None
            tune_fine_str   = comop_tuning_fine.format(tune_fine=tune_fine_sign) if tune_fine_sign is not None and tune_fine != 0.0 else ""
            return tune_coarse_str , tune_fine_str    

    def desc_osc_shapes(self,oscillator:Oscillator,style_guide:StyleGuide,flavour:DeclarationFlavour,declarations:DeclarationsMask)->Tuple[str,DeclarationFlavour]:
        
        shapes = list(filter(None,oscillator.shapes))

        if shapes is None or len(shapes)==0:
            return None
        
        # recurse
        limit = 1 if style_guide in [ StyleGuide.BASIC , StyleGuide.SUCCINT ] else None # we only look at the first Shape in those modes
        shapes_desc , flavour , declarations = self.recurse(self.desc_osc_shape,shapes,style_guide=style_guide,flavour=flavour,declarations=declarations,limit=limit)

        # compose sentence
        glues       = sentences[k_oscillator][k_glue][style_guide.value]
        glue        = random.choice( glues )
        shapes_desc = glue.join(shapes_desc)
        return shapes_desc , flavour 
    

    ##############
    #
    # OP
    #
    ##############

    # when we used balanced writing, we won't output the volumes ...
    def desc_op(self,
             operator: Operator,
             style_guide:StyleGuide,
             flavour:DeclarationFlavour=DeclarationFlavour.NONE,
             declarations:DeclarationsMask=DeclarationsMask.ALL,
             )->Tuple[Optional[str],DeclarationFlavour,DeclarationsMask]:

        # select proper formats
        compositing = sentences[k_operator][k_compositing][style_guide.value]
        glues       = sentences[k_operator][k_glue][style_guide.value]

        # select which flavours of mix declaration we will pick from ...
        compose_keys = self._filter_op_compositing_keys(operator,compositing,declarations)

        # pick compisiting formats and strings
        flavour_key = random.choice( compose_keys )
        glue        = random.choice( glues[flavour_key] )
        compose_loc = random.choice( compositing[flavour_key] )

        # lets simplify declarations here ...
        declarations_local = declarations & (DeclarationsMask.ALL - DeclarationsMask.OSC_VOLUME - DeclarationsMask.SHAPE_VOLUME)
        flavour_local = flavour & (DeclarationFlavour.ALL - DeclarationFlavour.GRP_OSC_VOLUME_ALL) | DeclarationFlavour.OSC_VOLUME_NONE
        flavour_local = flavour_local & (DeclarationFlavour.ALL - DeclarationFlavour.GRP_SHAPE_VOLUME_ALL) | DeclarationFlavour.SHAPE_VOLUME_NONE
        flavour_local = flavour_local & (DeclarationFlavour.ALL - DeclarationFlavour.GRP_OSC_OTHER) | DeclarationFlavour.OSC_OTHER_WITH_ID | DeclarationFlavour.OSC_OTHER_FOR_OPERATOR

        # sub-compositing
        operands_descs , flavour_local , declarations_local = self.recurse(self.desc_op_id_or_component,
                                                               self._sort_op_components_first(operator),
                                                               style_guide=style_guide,
                                                               flavour=flavour_local,
                                                               declarations=declarations_local)

        # compose sentence
        operands_desc = glue.join(operands_descs)
        op_type = self._get_op_type(operator,style_guide,flavour,declarations)
        operator_desc = compose_loc.format(operands_desc=operands_desc,operator_type=op_type)

        return operator_desc , flavour , declarations
    
    def _sort_op_components_first(self,operator:Operator):

        def component_sort_key(e:ComponentID|Component):
            if isinstance(e,ComponentID):
                renamed = re.sub(r'^(\w+)([\d]{1,1})$',r'\g<1>0\2',e.name)
                key = f"z_{renamed}"
                return key
            else:
                key = f"a_{e.__class__.__name__}{e.rank:02d}"
                return key 
        
        return sorted(operator.operands,key=component_sort_key )
    
    def _filter_op_compositing_keys(self,operator:Operator,compositing:dict,declarations:DeclarationsMask):
        # use_mix = (declarations & DeclarationsMask.OSC_VOLUME != 0)
        # use_balanced = self._is_osc_mix_balanced()
        compositing_copy = compositing.copy()
        if operator.type == Operation.FEEDBACK:
            compositing_copy.pop(k_comp_op_more_operands,None)
            compositing_copy.pop(k_comp_op_two_operands,None)
            compositing_copy.pop(k_comp_op_one_operand,None)

        elif len(operator.operands)==1:
            compositing_copy.pop(k_comp_op_feedback,None)
            compositing_copy.pop(k_comp_op_two_operands,None)
            compositing_copy.pop(k_comp_op_more_operands,None)
        else:
            compositing_copy.pop(k_comp_op_feedback,None)
            compositing_copy.pop(k_comp_op_one_operand,None)
        assert len(compositing_copy) > 0
        return list(compositing_copy.keys())         
    
    def desc_op_id_or_component(
            self,
            obj:ComponentID|Component,
            style_guide:StyleGuide,
            flavour:DeclarationFlavour=DeclarationFlavour.NONE,
            declarations:DeclarationsMask=DeclarationsMask.ALL,
        ):
        if isinstance(obj,ComponentID):
            return str(obj.name),flavour,declarations
        else:
            return self.desc(obj,style_guide,flavour,declarations)
        
    def _get_op_type(self,
                                     operator:Operator,
                                 style_guide:StyleGuide,
                                 flavour:DeclarationFlavour,
                                 declarations:DeclarationsMask)->str:

        operation_name = operator.type.lower()
        
        match style_guide:
            case StyleGuide.BASIC:
                op_type = get_word(f"k_operation_{operation_name}")
                return op_type
            case StyleGuide.SUCCINT:
                op_type = get_word(f"k_operation_{operation_name}")
                return op_type
            case StyleGuide.CONCISE:
                op_type = get_word(f"k_operation_{operation_name}")
                return op_type
            case StyleGuide.DETAILED:
                op_type = get_word(f"k_operation_{operation_name}")
                return op_type
            case StyleGuide.SPECIFICATION:
                op_type = get_word(f"k_operation_{operation_name}")
                return op_type               


    ##############
    #
    # FILTER
    #
    ##############

    
    def desc_filter(self,
                    filter:Filter,
             style_guide:StyleGuide,
             flavour:DeclarationFlavour=DeclarationFlavour.NONE,
             declarations:DeclarationsMask=DeclarationsMask.ALL,
             )->Tuple[Optional[str],DeclarationFlavour,DeclarationsMask]:
        return None , flavour , declarations
    
    ##############
    #
    # AMPLIFIER
    #
    ##############

    def desc_amp(self,
                 amplifier:Amplifier,
             style_guide:StyleGuide,
             flavour:DeclarationFlavour=DeclarationFlavour.NONE,
             declarations:DeclarationsMask=DeclarationsMask.ALL,
             )->Tuple[Optional[str],DeclarationFlavour,DeclarationsMask]:
        return None , flavour , declarations   

    ##############
    #
    # MODULATION
    #
    ##############

    def desc_mod(self,
                modulation:Modulation,
             style_guide:StyleGuide,
             flavour:DeclarationFlavour=DeclarationFlavour.NONE,
             declarations:DeclarationsMask=DeclarationsMask.ALL,
             )->Tuple[Optional[str],DeclarationFlavour,DeclarationsMask]:
        return None , flavour , declarations
    
    ##############
    #
    # MODULATION MATRIX
    #
    ##############

    def desc_mod_matrix(self,
                        mod_matrix:ModulationMatrix,
             style_guide:StyleGuide,
             flavour:DeclarationFlavour=DeclarationFlavour.NONE,
             declarations:DeclarationsMask=DeclarationsMask.ALL,
             )->Tuple[Optional[str],DeclarationFlavour,DeclarationsMask]:
        return None , flavour , declarations
    
    ##############
    #
    # EFFECT
    #
    ##############

    def desc_fx(self,
                effect:Effect,
             style_guide:StyleGuide,
             flavour:DeclarationFlavour=DeclarationFlavour.NONE,
             declarations:DeclarationsMask=DeclarationsMask.ALL,
             )->Tuple[Optional[str],DeclarationFlavour,DeclarationsMask]:
        return None , flavour , declarations
    
    ##############
    #
    # SETTINGS
    #
    ##############


    def desc_settings(self,
            settings:GlobalSettings,
             style_guide:StyleGuide,
             flavour:DeclarationFlavour=DeclarationFlavour.NONE,
             declarations:DeclarationsMask=DeclarationsMask.ALL,
             )->Tuple[Optional[str],DeclarationFlavour,DeclarationsMask]:
        return None , flavour , declarations    
    
    ##############
    #
    # ARCHTECTURE
    #
    ##############

    def desc_arch(self,
             architecture:Architecture,
             style_guide:StyleGuide,
             flavour:DeclarationFlavour=DeclarationFlavour.NONE,
             declarations:DeclarationsMask=DeclarationsMask.ALL
             )->Tuple[Optional[str],DeclarationFlavour,DeclarationsMask]:
        
        if isinstance(architecture,SubtractiveArchitecture):
            return self.desc_arch_sub(
                architecture,
                style_guide,
                flavour,
                declarations
            )


    ##############
    #
    # SUBTRACTIVE ARCH
    #
    ##############

    def desc_arch_sub(self,
             architecture:SubtractiveArchitecture,
             style_guide:StyleGuide,
             flavour:DeclarationFlavour=DeclarationFlavour.NONE,
             declarations:DeclarationsMask=DeclarationsMask.ALL
             )->Tuple[Optional[str],DeclarationFlavour,DeclarationsMask]:
        
        k_self_compositing = k_comp_archs_plural if flavour & DeclarationFlavour.ARCHS_PLURAL else k_comp_archs_singular

        # if we have some operators, lets add the ID in the description of the oscillators, to know what we're referring to
        has_operators = self._arch_sub_has_operators(architecture)
        if has_operators:
            flavour = flavour & (DeclarationFlavour.ALL - DeclarationFlavour.OSC_OTHER_WITH_ID) | DeclarationFlavour.OSC_OTHER_WITH_ID
        
        # select proper formats
        compositing = sentences[k_architecture_sub][k_self_compositing][style_guide.value]

        # pick compisiting format
        compose_loc = random.choice( compositing )

        # recurse
        oscs_desc , flavour , declarations = self.desc_arch_sub_oscillators(
                                                                    architecture,
                                                                    style_guide=style_guide,
                                                                   flavour=flavour,
                                                                   declarations=declarations)
        
        if oscs_desc is None:
            oscs_desc = "Oscillators are not part of signal path."
        

        # compose sentence
        desc = compose_loc.format(oscs_desc=oscs_desc)

        for regex , repl in cleanup.items():
            desc = re.sub(regex,repl,desc)

        return desc , flavour , declarations   

    def _arch_sub_has_operators(self,architecture:SubtractiveArchitecture)->bool:
        for osc_op in architecture.oscillators:
            if isinstance(osc_op,Operator):
                return True
        return False     


    def desc_arch_sub_oscillators(self,
                          architecture:SubtractiveArchitecture,
                          style_guide:StyleGuide,
                          flavour:DeclarationFlavour=DeclarationFlavour.NONE,
                          declarations:DeclarationsMask=DeclarationsMask.ALL
                          )->Tuple[Optional[str],DeclarationFlavour,DeclarationsMask]:
        
        # list of oscillators
        if isinstance(architecture.oscillators,list):
            oscillators = list(filter(None,architecture.oscillators))
        elif isinstance(architecture.oscillators,Mixer):
            oscillators = list(filter(None,architecture.oscillators.inputs))

        if oscillators is None or len(oscillators)==0:
            return None , flavour , declarations
        
        # select proper formats
        compositing = sentences[k_oscillators][k_compositing][style_guide.value]
        glues       = sentences[k_oscillators][k_glue][style_guide.value]

        # select which flavours of mix declaration we will pick from ...
        compose_keys = self._filter_arch_sub_compositing_keys(architecture,compositing,declarations)

        # pick compisiting format
        glue        = random.choice( glues )
        flavour_key = random.choice( compose_keys )
        compose_loc = random.choice( compositing[flavour_key] )

        # update flavour according to existing declarations
        if declarations & DeclarationsMask.OSC_VOLUME == 0: # should rarely happen unless explicitly specify at the root call
            flavour = flavour & (DeclarationFlavour.ALL - DeclarationFlavour.GRP_OSCS_MIX_ALL) | DeclarationFlavour.OSCS_MIX_NONE
        
        # update declarations: if we used "mix_balanced" or "mix", this is a forward declaration and we should consider OSC_LEVEL declared
        # is_forward_decl = flavour_key in [k_comp_oscs_mix_balanced,k_comp_oscs_mix_forward]
        # has_volume   = flavour_key in [k_comp_oscs_plural] and (flavour & DeclarationFlavour.GRP_OSCS_MIX_PRESENT != 0)
        has_volume = "{oscillators_mix_desc}" in compose_loc and (flavour & DeclarationFlavour.GRP_OSCS_MIX_PRESENT != 0)
        declarations    = declarations & (DeclarationsMask.ALL - DeclarationsMask.OSC_VOLUME) if has_volume  else declarations

        # prepare the sub-parts
        oscillators_mix_desc , flavour = self.__get_arch_sub_oscillators_mix_desc(architecture,style_guide,flavour,declarations) # in case we need it
        oscillators_tuning_desc , tuning_flavour = self.desc_arch_sub_oscs_tuning(architecture,style_guide,flavour,declarations) # in case we need it
        flavour = tuning_flavour # ???

        # update the flavour with what we will actually be outputting (some compositing may not include the mixing)
        if (flavour & (DeclarationFlavour.OSCS_MIX_BALANCED|DeclarationFlavour.OSCS_MIX_FORWARD) !=0 and "{oscillators_mix_desc}" not in compose_loc):
            flavour = flavour & ( DeclarationFlavour.ALL - DeclarationFlavour.GRP_OSCS_MIX_ALL ) | DeclarationFlavour.OSCS_MIX_NONE
            # cancel any declaration of osc volume
            declarations = declarations & (DeclarationsMask.ALL - DeclarationsMask.OSC_VOLUME)
        if (flavour & DeclarationFlavour.OSCS_TUNING_AFTERWARDS !=0 and "{oscillators_tuning_desc}" not in compose_loc):
            flavour = flavour & ( DeclarationFlavour.ALL - DeclarationFlavour.GRP_OSCS_TUNING_ALL ) | DeclarationFlavour.OSCS_TUNING_NONE
            flavour = flavour & ( DeclarationFlavour.ALL - DeclarationFlavour.GRP_OSC_TUNING_ALL ) 
            # cancel any declaration of osc tuning
            declarations = declarations & (DeclarationsMask.ALL - DeclarationsMask.OSC_TUNING)
        if oscillators_tuning_desc is None or oscillators_tuning_desc=="":
            oscillators_tuning_desc = ""
            flavour = flavour & ( DeclarationFlavour.ALL - DeclarationFlavour.GRP_OSCS_TUNING_ALL ) | DeclarationFlavour.OSCS_TUNING_NONE
            flavour = flavour & ( DeclarationFlavour.ALL - DeclarationFlavour.GRP_OSC_TUNING_ALL ) # reset also for the OSC
            declarations = declarations & (DeclarationsMask.ALL - DeclarationsMask.OSC_TUNING)
        if flavour & (DeclarationFlavour.OSCS_TUNING_AFTERWARDS) !=0:
            flavour = flavour & ( DeclarationFlavour.ALL - DeclarationFlavour.GRP_OSC_TUNING_ALL ) | DeclarationFlavour.OSC_TUNING_NONE

        # recurse
        oscillators_descs , flavour , declarations = self.recurse(self.desc_osc_or_op,oscillators,style_guide=style_guide,flavour=flavour,declarations=declarations)

        # compose sentence
        oscillators_desc = glue.join(oscillators_descs)
        oscillators_desc = compose_loc.format(oscillators_desc=oscillators_desc,
                                            oscillators_mix_desc=oscillators_mix_desc,
                                            oscillators_tuning_desc=oscillators_tuning_desc)

        return oscillators_desc , flavour , declarations
    
    def __get_arch_sub_oscillators_mix_desc(self,architecture:SubtractiveArchitecture,style_guide:StyleGuide,flavour:DeclarationFlavour,declarations:DeclarationsMask)->Tuple[str,DeclarationFlavour]:

        # we choose a balanced mix flavour but the mix is not balanced ... remove it ...
        if flavour & DeclarationFlavour.OSCS_MIX_BALANCED != 0 and not self._is_arch_sub_osc_mix_balanced(architecture):
            flavour = flavour & (DeclarationFlavour.ALL - DeclarationFlavour.OSCS_MIX_BALANCED) 

        if flavour & DeclarationFlavour.OSCS_MIX_FORWARD:
            flavour = flavour & (DeclarationFlavour.ALL - DeclarationFlavour.GRP_OSCS_MIX_ALL) | DeclarationFlavour.OSCS_MIX_FORWARD
            mix_value = self._get_arch_sub_oscillators_mix(architecture,style_guide,flavour,declarations)
            if style_guide.value not in sentences[k_oscillators][k_comp_oscs_mix_forward]:
                return None , flavour & (DeclarationFlavour.ALL - DeclarationFlavour.GRP_OSCS_MIX_ALL) | DeclarationFlavour.OSCS_MIX_NONE
            compositing_mix = random.choice( sentences[k_oscillators][k_comp_oscs_mix_forward][style_guide.value] )
            mix_desc = compositing_mix.format(oscillators_mix=mix_value)
            return mix_desc , flavour
        elif flavour & DeclarationFlavour.OSCS_MIX_BALANCED:
            flavour = flavour & (DeclarationFlavour.ALL - DeclarationFlavour.GRP_OSCS_MIX_ALL) | DeclarationFlavour.OSCS_MIX_BALANCED
            mix_value = self._get_arch_sub_oscillators_mix(architecture,style_guide,flavour,declarations)
            if style_guide.value not in sentences[k_oscillators][k_comp_oscs_mix_forward]:
                return None , flavour & (DeclarationFlavour.ALL - DeclarationFlavour.GRP_OSCS_MIX_ALL) | DeclarationFlavour.OSCS_MIX_NONE
            compositing_mix = random.choice( sentences[k_oscillators][k_comp_oscs_mix_balanced][style_guide.value] )
            mix_desc = compositing_mix.format(oscillators_mix=mix_value)
            return mix_desc , flavour
        elif flavour & DeclarationFlavour.OSCS_MIX_DEFAULT:
            flavour = flavour & (DeclarationFlavour.ALL - DeclarationFlavour.GRP_OSCS_MIX_ALL) | DeclarationFlavour.OSCS_MIX_DEFAULT
            mix_value = self._get_arch_sub_oscillators_mix(architecture,style_guide,flavour,declarations)
            if style_guide.value not in sentences[k_oscillators][k_comp_oscs_mix_forward]:
                return None , flavour & (DeclarationFlavour.ALL - DeclarationFlavour.GRP_OSCS_MIX_ALL) | DeclarationFlavour.OSCS_MIX_NONE
            compositing_mix = random.choice( sentences[k_oscillators][k_comp_oscs_mix_default][style_guide.value] )
            mix_desc  = compositing_mix.format(oscillators_mix=mix_value)
            return mix_desc , flavour
        elif flavour & DeclarationFlavour.OSCS_MIX_NONE:
            flavour = flavour & (DeclarationFlavour.ALL - DeclarationFlavour.GRP_OSCS_MIX_ALL) | DeclarationFlavour.OSCS_MIX_NONE
            mix_desc = ""
            return mix_desc , flavour
        else:
            # we haven't pick a mix flavour yet, pick one now
            flavours = [ 
                DeclarationFlavour.OSCS_MIX_NONE,
                DeclarationFlavour.OSCS_MIX_FORWARD ,
                DeclarationFlavour.OSCS_MIX_DEFAULT
            ]
            if self._is_arch_sub_osc_mix_balanced(architecture):
                flavours.append(DeclarationFlavour.OSCS_MIX_BALANCED) 

            flavour_select = random.choice(flavours)
            flavour = flavour & (DeclarationFlavour.ALL - DeclarationFlavour.GRP_OSCS_MIX_ALL) | flavour_select
            return self.__get_arch_sub_oscillators_mix_desc(architecture,style_guide=style_guide,flavour=flavour,declarations=declarations)    
    
    def _get_arch_sub_oscillators_mix(self,architecture:SubtractiveArchitecture,style_guide:StyleGuide,flavour:DeclarationFlavour,declarations:DeclarationsMask)->str:
        total_vol = 0.0
        for osc in architecture.oscillators:
            total_vol += osc.volume
        multiplier = 1 / total_vol if total_vol != 0.0 else 1.0
        match style_guide:
            case StyleGuide.BASIC:
                volumes = [ f"{round(100.0*osc.volume*multiplier)}" for osc in architecture.oscillators]
                return "/".join(volumes)
            case StyleGuide.SUCCINT:
                volumes = [ f"{round(100.0*osc.volume*multiplier)}%" for osc in architecture.oscillators]
                return "/".join(volumes)
            case StyleGuide.CONCISE:
                volumes = [ f"{round(100.0*osc.volume*multiplier)}%" for osc in architecture.oscillators]
                return "/".join(volumes)
            case StyleGuide.DETAILED:
                volumes = [ f"{round(100.0*osc.volume*multiplier,2)}%" for osc in architecture.oscillators]
                return "/".join(volumes)
            case StyleGuide.SPECIFICATION:
                volumes = [ f"{round(100.0*osc.volume*multiplier,2)}%" for osc in architecture.oscillators]
                return "/".join(volumes)

    def _is_arch_sub_osc_mix_balanced(self,architecture:SubtractiveArchitecture)->bool:
        if architecture.oscillators is None or len(architecture.oscillators)==1:
            return False
        vol_total = 0.0
        for osc in architecture.oscillators:
            vol_total += osc.volume

        if vol_total==0.0:
            return True
        vol_avg = vol_total / len(architecture.oscillators)

        for osc in architecture.oscillators:
            if osc.volume > vol_avg * 1.2 or osc.volume < vol_avg * 0.8 :
                return False
            
        return True
    
    def desc_arch_sub_oscs_tuning(self,architecture:SubtractiveArchitecture,
                                  style_guide:StyleGuide,
                                  flavour:DeclarationFlavour,
                                  declarations:DeclarationsMask)->Tuple[str,DeclarationFlavour]:

        if flavour & DeclarationFlavour.OSCS_TUNING_AFTERWARDS:
            flavour = flavour & (DeclarationFlavour.ALL - DeclarationFlavour.GRP_OSCS_TUNING_ALL) | DeclarationFlavour.OSCS_TUNING_AFTERWARDS
            tuning_values , flavour = self._get_arch_sub_oscillators_tuning(architecture,style_guide,flavour,declarations)
            if style_guide.value not in sentences[k_oscillators][k_comp_oscs_tuning_afterwards] or tuning_values is None:
                return None , flavour & (DeclarationFlavour.ALL - DeclarationFlavour.GRP_OSCS_TUNING_ALL) | DeclarationFlavour.OSCS_TUNING_NONE
            compositing_tuning = random.choice( sentences[k_oscillators][k_comp_oscs_tuning_afterwards][style_guide.value] )
            tuning_desc = compositing_tuning.format(oscillators_tuning=tuning_values)
            return tuning_desc , flavour
        elif flavour & DeclarationFlavour.OSCS_TUNING_NONE:
            flavour = flavour & (DeclarationFlavour.ALL - DeclarationFlavour.GRP_OSCS_TUNING_ALL) | DeclarationFlavour.OSCS_TUNING_NONE
            tuning_values = ""
            return tuning_values , flavour
        else:
            # we haven't pick a mix flavour yet, pick one now
            flavours = [ 
                DeclarationFlavour.OSCS_TUNING_NONE,
                DeclarationFlavour.OSCS_TUNING_AFTERWARDS,
            ]
            flavour_select = random.choice(flavours)
            flavour = flavour & (DeclarationFlavour.ALL - DeclarationFlavour.GRP_OSCS_TUNING_ALL) | flavour_select
            return self.desc_arch_sub_oscs_tuning(architecture,style_guide=style_guide,flavour=flavour,declarations=declarations)  
        
    # almost a copy of Oscillator::desc_tuning
    # but using the k_oscillators key instead, to compose the tuning string differently
    # (no "OSC1" as this would not make sense within the OSC context)
    # we're still updating the flavours at the OSC level because why not ... 
    # we could do it now or later ...
    def desc_arch_sub_osc_tuning(self,
                        architecture:SubtractiveArchitecture,
                        osc:Oscillator,
                         style_guide:StyleGuide,
                         flavour:DeclarationFlavour,
                         declarations:DeclarationsMask)->Tuple[str,DeclarationFlavour]:
        
        if flavour & DeclarationFlavour.OSC_TUNING_PITCH:
            flavour = flavour & (DeclarationFlavour.ALL - DeclarationFlavour.GRP_OSC_TUNING_ALL) | DeclarationFlavour.OSC_TUNING_PITCH
            tuning_coarse , tuning_fine = self.osc_tuning_values(osc,style_guide,flavour,declarations)
            if tuning_coarse == "" and tuning_fine == "":
                return "" , flavour
            if style_guide.value not in sentences[k_oscillators][k_comp_osc_tuning]: # notice the k_oscillators key
                return "" , flavour & (DeclarationFlavour.ALL - DeclarationFlavour.GRP_OSC_TUNING_ALL) | DeclarationFlavour.OSC_TUNING_NONE
            compositing_tuning = random.choice( sentences[k_oscillators][k_comp_osc_tuning][style_guide.value] )
            tuning_val = compositing_tuning.format(tuning_coarse=tuning_coarse,tuning_fine=tuning_fine,osc_i=osc.rank)
            return tuning_val , flavour
        elif flavour & DeclarationFlavour.OSC_TUNING_OCT:
            flavour = flavour & (DeclarationFlavour.ALL - DeclarationFlavour.GRP_OSC_TUNING_ALL) | DeclarationFlavour.OSC_TUNING_OCT
            tuning_coarse , tuning_fine = self.osc_tuning_values(osc,style_guide,flavour,declarations)
            if tuning_coarse == "" and tuning_fine == "":
                return "" , flavour
            if style_guide.value not in sentences[k_oscillators][k_comp_osc_tuning]:
                return "" , flavour & (DeclarationFlavour.ALL - DeclarationFlavour.GRP_OSC_TUNING_ALL) | DeclarationFlavour.OSC_TUNING_NONE
            compositing_tuning = random.choice( sentences[k_oscillators][k_comp_osc_tuning][style_guide.value] )
            tuning_val = compositing_tuning.format(tuning_coarse=tuning_coarse,tuning_fine=tuning_fine,osc_i=osc.rank)
            return tuning_val , flavour
        elif flavour & DeclarationFlavour.OSC_TUNING_NONE:
            flavour = flavour & (DeclarationFlavour.ALL - DeclarationFlavour.GRP_OSC_TUNING_ALL) | DeclarationFlavour.OSC_TUNING_NONE
            return "" , flavour
        else:
            # we haven't pick a volume flavour yet, pick one now
            flavours = [ 
                DeclarationFlavour.OSC_TUNING_NONE ,
                DeclarationFlavour.OSC_TUNING_PITCH ,
                DeclarationFlavour.OSC_TUNING_OCT ,
            ]
            flavour_select = random.choice(flavours)
            flavour = flavour & (DeclarationFlavour.ALL - DeclarationFlavour.GRP_OSC_TUNING_ALL) | flavour_select
            return self.desc_arch_sub_osc_tuning(architecture,osc,style_guide=style_guide,flavour=flavour,declarations=declarations)             
        
    def _get_arch_sub_oscillators_tuning(self,architecture:SubtractiveArchitecture,style_guide:StyleGuide,flavour:DeclarationFlavour,declarations:DeclarationsMask)->Tuple[str,DeclarationFlavour]:
        tunings = []
        # dont update master flavour
        # lets see globally what is going on and depending on final result, the sub-calls can re-generate
        for osc in architecture.oscillators: # if this is a mixer, this will iterate as well ...
            # we may have some operands that are actual objects of Oscillators instead of References (ComponentID)
            if isinstance(osc,Operator):
                for osc_ in osc.operands:
                    if isinstance(osc_,ComponentID):
                        continue # the matching OSC should be defined in the usual oscillators list ...
                    elif isinstance(osc_,Oscillator):
                        desc_tuning , flavour = self.desc_arch_sub_osc_tuning(architecture,osc_,style_guide,flavour,declarations)
                        if desc_tuning is not None and desc_tuning!= "":
                            tunings.append(desc_tuning)
            else:
                desc_tuning , flavour = self.desc_arch_sub_osc_tuning(architecture,osc,style_guide,flavour,declarations)
                if desc_tuning is not None and desc_tuning!= "":
                    tunings.append(desc_tuning)
        if len(tunings)==0:
            return None , flavour
        if style_guide.value not in sentences[k_oscillators][k_comp_oscs_tuning_glue]:
            return None , flavour 
        tuning_glue = random.choice( sentences[k_oscillators][k_comp_oscs_tuning_glue][style_guide.value] )
        return tuning_glue.join(tunings) ,flavour              
    
    def _filter_arch_sub_compositing_keys(self,architecture:SubtractiveArchitecture,compositing:dict,declarations:DeclarationsMask):
        # use_mix = (declarations & DeclarationsMask.OSC_VOLUME != 0)
        # use_balanced = self._is_osc_mix_balanced()
        compositing_copy = compositing.copy()
        if len(architecture.oscillators)==1:
            compositing_copy.pop(k_comp_oscs_plural,None)
            compositing_copy.pop(k_comp_oscs_mix_forward,None) # should not be present anymore
            compositing_copy.pop(k_comp_oscs_mix_balanced,None) # should not be present anymore
        else:
            compositing_copy.pop(k_comp_oscs_singular,None)
        # if not use_mix:
        #     compositing_copy.pop(k_comp_oscs_mix_forward,None) # should not be present anymore
        #     compositing_copy.pop(k_comp_oscs_mix_balanced) # should not be present anymore
        # if not use_balanced:
        #     compositing_copy.pop(k_comp_oscs_mix_balanced,None) # should not be present anymore
        assert len(compositing_copy) > 0
        return list(compositing_copy.keys())     


    ##############
    #
    # SoundTone Description
    #
    ##############


    def desc_desc(self,
            soundtonedesc:SoundToneDescription,
             style_guide:StyleGuide,
             flavour:DeclarationFlavour=DeclarationFlavour.NONE,
             declarations:DeclarationsMask=DeclarationsMask.ALL
             )->Tuple[Optional[str],DeclarationFlavour,DeclarationsMask]:
        

        architectures = list(filter(None,soundtonedesc.architectures))

        if architectures is None or len(architectures)==0:
            return "everything is off"
        
        # select proper formats
        compositing = sentences[k_description][k_compositing][style_guide.value]
        glues       = sentences[k_description][k_glue][style_guide.value]

        # pick compisiting format
        glue        = random.choice( glues )
        compose_loc = random.choice( compositing )

        # set the flavour for the architecture
        if len(soundtonedesc.architectures)>1:
            flavour = flavour & (DeclarationFlavour.ALL - DeclarationFlavour.GRP_ARCHS_ALL) | DeclarationFlavour.ARCHS_PLURAL
        else:
            flavour = flavour & (DeclarationFlavour.ALL - DeclarationFlavour.GRP_ARCHS_ALL) | DeclarationFlavour.ARCHS_SINGULAR

        # recurse
        architectures_descs , flavour , declarations = self.recurse(self.desc_arch,architectures,style_guide=style_guide,flavour=flavour,declarations=declarations)

        # compose sentence
        architectures_desc = glue.join(architectures_descs)
        architectures_desc = compose_loc.format(architectures_desc=architectures_desc)    

        return architectures_desc , flavour , declarations
    

    def desc(
             self,
             obj: Component,
             style_guide:StyleGuide,
             flavour:DeclarationFlavour=DeclarationFlavour.NONE,
             declarations:DeclarationsMask=DeclarationsMask.ALL,
             )->Tuple[Optional[str],DeclarationFlavour,DeclarationsMask]:  
        
        if isinstance(obj,Oscillator):
            return self.desc_osc(obj,style_guide,flavour,declarations)
        elif isinstance(obj,Filter):
            return self.desc_filter(obj,style_guide,flavour,declarations)
        elif isinstance(obj,SubtractiveArchitecture):
            return self.desc_arch_sub(obj,style_guide,flavour,declarations)
        elif isinstance(obj,SoundToneDescription):
            return self.desc_desc(obj,style_guide,flavour,declarations)