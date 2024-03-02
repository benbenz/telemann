from typing import List , Optional , Tuple
from abc import ABC , abstractmethod
from pydantic import BaseModel , confloat , conint
from .compositing.locale_en import sentences , words , cleanup
from .compositing.keys import * # import the k_*** keys
from .defs import *
import random
import math
import re

"""
This should add the field analysis in sound_info and add the following sections:

oscs: [
        { shapes : [ 'square'|'triangle'|'sine'|'pwm'|'saw'|'sawup'|'sawdown'|'sample'|'additive'|'digital'|'other'|'sub', ...] , mix: 0.0...1.0 , pwm: true|false } ,
        { shapes : ['square'|'triangle'|'sine'|'pwm'|'saw'|'sawup'|'sawdown'|'sample'|'additive'|'digital'|'other'|'sub', ...] , mix: 0.0...1.0 , pwm: true|false } ,
        ...
] ,
filters : [
    { type : 'lowpass'|'highpass'|'bandpass'|'other' , slope: '6dB'|'12dB'|'18dB'|'24dB'... } ,
    { type : 'lowpass'|'highpass'|'bandpass'|'other' , slope: '6dB'|'12dB'|'18dB'|'24dB'... } ,
    ...        
] ,
envs: { 
    { attack: 'fast'|'medium'|'slow' , release: 'fast'|'medium'|'slow' , sustain: 'low'|'medium'|'high' , decay:'slow'|'medium'|'fast'} ,
    { attack: 'fast'|'medium'|'slow' , release: 'fast'|'medium'|'slow' , sustain: 'low'|'medium'|'high' , decay:'slow'|'medium'|'fast'} ,
    ...
} ,
modulation: {
    cross_modulation: true|false,
    ring_modulation: 0.0....1.0,
    sync: true|false,
    pitch_env: 0.0...1.0
    pitch_lfo: 0.0...1.0
    filter_env: 0.0...1.0
    filter_lfo: 0.0...1.0
    amp_env: 0.0...1.0
    amp_lfo: 0.0...1.0
}
"""

def get_word(key):
    r = words[key]    
    if(isinstance(r,list)):
        return random.choice(r)
    return r
    
class ExtensionComponent(BaseModel,ABC):

    @abstractmethod
    def desc(self,
             style_guide:StyleGuide,
             flavour:DeclarationFlavour=DeclarationFlavour.NONE, # use to uniformize a flavour of style accross siblings
             declarations:DeclarationsMask=DeclarationsMask.ALL, # use to pass what has been declared in the recursion
             )->Tuple[Optional[str],DeclarationFlavour,DeclarationsMask]:
        pass


    def recurse(self,
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
            desc , flavour , declaration_ = child.desc(style_guide,flavour,declarations)
            if desc is not None:
                declarations_.append(declaration_)
                descs.append(desc)
        # update cross-level declarations, after the fact
        for declaration_  in declarations_:
            declarations &= declaration_
        return descs , flavour , declarations


class Envelope(ExtensionComponent):

    attack : confloat(ge=0.0,le=1.0)
    decay  : confloat(ge=0.0,le=1.0)
    sustain: confloat(ge=0.0,le=1.0)
    release: confloat(ge=0.0,le=1.0)
    type   : EnvelopeType

    def desc(self,
             style_guide:StyleGuide,
             flavour:DeclarationFlavour=DeclarationFlavour.NONE,
             declarations:DeclarationsMask=DeclarationsMask.ALL
             )->Tuple[Optional[str],DeclarationFlavour,DeclarationsMask]:
        return None , flavour , declarations
    
class LFO(ExtensionComponent):

    waveform: WaveformEnum
    frequency : confloat(ge=0.0,le=1.0)
    delay : confloat(ge=0.0,le=1.0)

    def desc(self,
             style_guide:StyleGuide,
             flavour:DeclarationFlavour=DeclarationFlavour.NONE,
             declarations:DeclarationsMask=DeclarationsMask.ALL,
             )->Tuple[Optional[str],DeclarationFlavour,DeclarationsMask]:
        return None,flavour,declarations   

class OscillatorShape(ExtensionComponent):

    waveform : WaveformEnum
    volume : confloat(ge=0.0,le=1.0)|None=None
    width: WaveformWidthEnum|None = None

    def desc(self,
             style_guide:StyleGuide,
             flavour:DeclarationFlavour=DeclarationFlavour.NONE,
             declarations:DeclarationsMask=DeclarationsMask.ALL,
             )->Tuple[Optional[str],DeclarationFlavour,DeclarationsMask]:

        # select proper formats
        compositing = sentences[k_shape][k_compositing][style_guide.value]

        # select which flavour of mix declaration we will take ...
        compose_keys = self._filter_compositing_keys(compositing,declarations)

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
        waveform_name = get_word(self.waveform.value)
        waveform_width = get_word(self.width.value) if self.width is not None else None
        waveform_width = f"{waveform_width}-" if waveform_width is not None else ""
        volume_desc , flavour = self._get_volume_desc(style_guide,flavour,declarations) # in case we need it
        shape_desc = compose_loc.format(waveform_name=waveform_name,volume_desc=volume_desc,waveform_width=waveform_width)

        return shape_desc , flavour , declarations   
    
    def _get_volume_desc(self,
                         style_guide:StyleGuide,
                         flavour:DeclarationFlavour,
                         declarations:DeclarationsMask)->Tuple[str,DeclarationFlavour]:
        
        if flavour & DeclarationFlavour.SHAPE_VOLUME_NUMBER:
            flavour = flavour & (DeclarationFlavour.ALL - DeclarationFlavour.GRP_SHAPE_VOLUME_ALL) | DeclarationFlavour.SHAPE_VOLUME_NUMBER
            vol_value = self._get_volume_desc_as_number(style_guide,flavour,declarations)
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
            return self._get_volume_desc(style_guide=style_guide,flavour=flavour,declarations=declarations)    

    def _get_volume_desc_as_number(self,
                         style_guide:StyleGuide,
                         flavour:DeclarationFlavour,
                         declarations:DeclarationsMask)->str:
        match style_guide:
            case StyleGuide.BASIC:
                volume = f"{round(100.0*self.volume)}"
                return volume
            case StyleGuide.SUCCINT:
                volume = f"{round(100.0*self.volume)}%"
                return volume
            case StyleGuide.CONCISE:
                volume = f"{round(100.0*self.volume)}%"
                return volume
            case StyleGuide.DETAILED:
                volume = f"{round(100.0*self.volume,2)}%"
                return volume
            case StyleGuide.SPECIFICATION:
                volume = f"{round(100.0*self.volume,2)}%"
                return volume
        
    def _filter_compositing_keys(self,compositing:dict,declarations:DeclarationsMask):
        # lets add the volume info if we want it
        compositing_copy = compositing.copy()
        assert len(compositing_copy) > 0
        return list(compositing_copy.keys())
    
class Oscillator(ExtensionComponent):

    shapes : List[OscillatorShape]=[]
    volume : confloat(ge=0.0,le=1.0)
    tune_coarse :  Optional[conint(multiple_of=12,ge=-24,le=24)]=None # = range = octave
    tune_fine : Optional[confloat(ge=-6.0,le=6.0)]=None
    detune : Optional[confloat(ge=0.0,le=1.0)]=None
    sub : bool=False
    sub_octave : Optional[conint(ge=-4,le=-1)]=None # [-4,-1] suboscillator octave range

    # when we used balanced writing, we won't output the volumes ...
    def desc(self,
             style_guide:StyleGuide,
             flavour:DeclarationFlavour=DeclarationFlavour.NONE,
             declarations:DeclarationsMask=DeclarationsMask.ALL,
             )->Tuple[Optional[str],DeclarationFlavour,DeclarationsMask]:

        shapes = list(filter(None,self.shapes))

        if shapes is None or len(shapes)==0:
            return None
        
        # select proper formats
        compositing = sentences[k_oscillator][k_compositing][style_guide.value]
        glues       = sentences[k_oscillator][k_glue][style_guide.value]
        osc_type    = sentences[k_oscillator][k_osc_type]
        osc_article = sentences[k_oscillator][k_osc_article]

        # select which flavour of mix declaration we will take ...
        compose_keys = self._filter_compositing_keys(compositing,declarations)
        
        # pick compisiting formats and strings
        glue        = random.choice( glues )
        flavour_key = random.choice( compose_keys ) 
        compose_loc = random.choice( compositing[flavour_key] )
        osc_type    = random.choice( osc_type[k_comp_osc_sub] if self.sub else osc_type[k_comp_osc_sub_not])
        osc_article = random.choice( osc_article[k_comp_osc_sub] if self.sub else osc_article[k_comp_osc_sub_not])

        # update flavour according to existing declarations
        if declarations & DeclarationsMask.OSC_VOLUME == 0:
            flavour = flavour & (DeclarationFlavour.ALL - DeclarationFlavour.GRP_OSC_VOLUME_ALL) | DeclarationFlavour.OSC_VOLUME_NONE
        if declarations & DeclarationsMask.SHAPE_VOLUME == 0: # should not happen
            flavour = flavour & (DeclarationFlavour.ALL - DeclarationFlavour.GRP_SHAPE_VOLUME_ALL) | DeclarationFlavour.SHAPE_VOLUME_NONE

        # update declarations: considerations that impact children
        has_osc_vol = True # at this point lets consider OSC_VOLUME declared
        declarations = declarations & (DeclarationsMask.ALL - DeclarationsMask.OSC_VOLUME) if has_osc_vol  else declarations
        # lets not show the shape level if the oscillator doesn't blend shapes
        dont_use_shape_vol = len(shapes)<2 or random.random()>0.5
        declarations = declarations & (DeclarationsMask.ALL - DeclarationsMask.SHAPE_VOLUME) if dont_use_shape_vol  else declarations        

        # update the flavour with what we will actually be outputting (some compositing may not include the volume)
        if (flavour & (DeclarationFlavour.OSC_VOLUME_NUMBER|DeclarationFlavour.OSC_VOLUME_TEXT_POST) !=0 and "{volume_desc_post}" not in compose_loc) \
          or (flavour&DeclarationFlavour.OSC_VOLUME_TEXT_PRE!=0 and "{volume_desc_pre}" not in compose_loc):
            flavour = flavour & ( DeclarationFlavour.ALL - DeclarationFlavour.GRP_OSC_VOLUME_ALL ) | DeclarationFlavour.OSC_VOLUME_NONE

        vol_desc_post , vol_desc_pre ,flavour = self._get_volume_descs(style_guide,flavour,declarations)
        
        # update the flavour and declarations with trhe actual situation (some strings may not include replacement patterns)
        if flavour & (DeclarationFlavour.OSC_VOLUME_NUMBER|DeclarationFlavour.OSC_VOLUME_TEXT_POST) !=0 and "{volume_desc_post}" not in compose_loc \
        or flavour & DeclarationFlavour.OSC_VOLUME_TEXT_PRE !=0 and "{volume_desc_pre}" not in compose_loc:
            flavour = flavour & ( DeclarationFlavour.ALL - DeclarationFlavour.GRP_OSC_VOLUME_ALL ) | DeclarationFlavour.OSC_VOLUME_NONE
            declarations = declarations & (DeclarationsMask.ALL - DeclarationsMask.OSC_VOLUME)

        # recurse
        limit = 1 if style_guide in [ StyleGuide.BASIC , StyleGuide.SUCCINT ] else None # we only look at the first Shape in those modes
        shapes_desc , flavour , declarations = self.recurse(shapes,style_guide=style_guide,flavour=flavour,declarations=declarations,limit=limit)

        # compose sentence
        shapes_desc = glue.join(shapes_desc)
        shapes_desc = compose_loc.format(shapes_desc=shapes_desc,
                                        volume_desc_post=vol_desc_post,
                                        volume_desc_pre=vol_desc_pre,
                                        osc_type=osc_type,
                                        osc_article=osc_article)
        
        return shapes_desc , flavour , declarations
    
    def _filter_compositing_keys(self,compositing:dict,declarations:DeclarationsMask):
        # lets add the volume info if we want it
        compositing_copy = compositing.copy()
        if len(self.shapes)==1:
            compositing_copy.pop(k_comp_osc_plural,None)
        else:
            compositing_copy.pop(k_comp_osc_singular,None)
        assert len(compositing_copy) > 0
        return list(compositing_copy.keys())

    def _get_volume_descs(self,
                         style_guide:StyleGuide,
                         flavour:DeclarationFlavour,
                         declarations:DeclarationsMask)->Tuple[str,DeclarationFlavour]:
        
        if flavour & DeclarationFlavour.OSC_VOLUME_NUMBER:
            flavour = flavour & (DeclarationFlavour.ALL - DeclarationFlavour.GRP_OSC_VOLUME_ALL) | DeclarationFlavour.OSC_VOLUME_NUMBER
            vol_value = self._get_volume_desc_as_number(style_guide,flavour,declarations)
            compositing_vol = random.choice( sentences[k_oscillator][k_comp_osc_vol_number][style_guide.value] )
            vol_desc_post = compositing_vol.format(volume_value=vol_value)
            vol_desc_pre  = ""
            return vol_desc_post , vol_desc_pre , flavour
        elif flavour & DeclarationFlavour.OSC_VOLUME_TEXT_POST:
            flavour = flavour & (DeclarationFlavour.ALL - DeclarationFlavour.GRP_OSC_VOLUME_ALL) | DeclarationFlavour.OSC_VOLUME_TEXT_POST
            vol_text = self._get_volume_desc_as_text(style_guide,flavour,declarations)
            compositing_vol = random.choice( sentences[k_oscillator][k_comp_osc_vol_text_post][style_guide.value] )
            vol_desc_post = compositing_vol.format(volume_text=vol_text)
            vol_desc_pre  = ""
            return vol_desc_post , vol_desc_pre , flavour
        elif flavour & DeclarationFlavour.OSC_VOLUME_TEXT_PRE:
            flavour = flavour & (DeclarationFlavour.ALL - DeclarationFlavour.GRP_OSC_VOLUME_ALL) | DeclarationFlavour.OSC_VOLUME_TEXT_PRE
            vol_text = self._get_volume_desc_as_text(style_guide,flavour,declarations)
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
            return self._get_volume_descs(style_guide=style_guide,flavour=flavour,declarations=declarations)     
        
    def _get_volume_desc_as_number(self,
                                   style_guide:StyleGuide,
                                   flavour:DeclarationFlavour,
                                   declarations:DeclarationsMask)->str:
        match style_guide:
            case StyleGuide.BASIC:
                volume = round(100.0*self.volume)
                return volume
            case StyleGuide.SUCCINT:
                volume = f"{round(100.0*self.volume)}%"
                return volume
            case StyleGuide.CONCISE:
                volume = f"{round(100.0*self.volume)}%"
                return volume
            case StyleGuide.DETAILED:
                volume = f"{round(100.0*self.volume,2)}%"
                return volume
            case StyleGuide.SPECIFICATION:
                volume = f"{round(100.0*self.volume,2)}%"
                return volume
            
    def _get_volume_desc_as_text(self,
                                 style_guide:StyleGuide,
                                 flavour:DeclarationFlavour,
                                 declarations:DeclarationsMask)->str:

        if self.volume==0.0:
            volume_group = 0 
        elif self.volume<1.0:
            volume_group = math.ceil(self.volume/20.0) # 1,5
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

    
class Filter(ExtensionComponent):

    def desc(self,
             style_guide:StyleGuide,
             flavour:DeclarationFlavour=DeclarationFlavour.NONE,
             declarations:DeclarationsMask=DeclarationsMask.ALL,
             )->Tuple[Optional[str],DeclarationFlavour,DeclarationsMask]:
        return None , flavour , declarations
    
class Amplifier(ExtensionComponent):

    volume: confloat(ge=0.0,le=1.0)

    def desc(self,
             style_guide:StyleGuide,
             flavour:DeclarationFlavour=DeclarationFlavour.NONE,
             declarations:DeclarationsMask=DeclarationsMask.ALL,
             )->Tuple[Optional[str],DeclarationFlavour,DeclarationsMask]:
        return None , flavour , declarations    

class Modulation(ExtensionComponent):

    source_id  : ModulationSourceID
    source     : Optional[Oscillator|LFO|Envelope]=None
    dest_id    : ModulationDestID
    dest       : Optional[Oscillator|Filter|LFO|Envelope]=None
    dest_param : ModulationDestParam
    depth      : float

    def desc(self,
             style_guide:StyleGuide,
             flavour:DeclarationFlavour=DeclarationFlavour.NONE,
             declarations:DeclarationsMask=DeclarationsMask.ALL,
             )->Tuple[Optional[str],DeclarationFlavour,DeclarationsMask]:
        return None , flavour , declarations
        
class ModulationMatrix(ExtensionComponent):

    modulations : List[Modulation]=[]
    # pwm   : Optional[List[Modulation]]=None
    # pitch : Optional[List[Modulation]]=None
    # ring  : Optional[List[ModulationSource]]=None
    # cross : Optional[List[ModulationSource]]=None
    # sync  : Optional[List[ModulationSource]]=None

    def desc(self,
             style_guide:StyleGuide,
             flavour:DeclarationFlavour=DeclarationFlavour.NONE,
             declarations:DeclarationsMask=DeclarationsMask.ALL,
             )->Tuple[Optional[str],DeclarationFlavour,DeclarationsMask]:
        return None , flavour , declarations
    
    def add_modulation(self,modulation:Modulation):
        self.modulations.append(modulation)

class Effect(ExtensionComponent):

    type : EffectType

    def desc(self,
             style_guide:StyleGuide,
             flavour:DeclarationFlavour=DeclarationFlavour.NONE,
             declarations:DeclarationsMask=DeclarationsMask.ALL,
             )->Tuple[Optional[str],DeclarationFlavour,DeclarationsMask]:
        return None , flavour , declarations
    

class GlobalSettings(ExtensionComponent):
    
    detune : Optional[confloat(ge=0.0,le=1.0)]=None

    def desc(self,
             style_guide:StyleGuide,
             flavour:DeclarationFlavour=DeclarationFlavour.NONE,
             declarations:DeclarationsMask=DeclarationsMask.ALL,
             )->Tuple[Optional[str],DeclarationFlavour,DeclarationsMask]:
        return None , flavour , declarations    

class SoundToneDescription(ExtensionComponent):

    oscillators:Optional[List[Oscillator]]=None
    filters: Optional[List[Filter]]=None
    amplifier: Optional[Amplifier]=None
    envelopes: Optional[List[Envelope]]=None 
    lfos: Optional[List[LFO]]=None
    effects: Optional[List[Effect]]=None
    mod_matrix: Optional[ModulationMatrix]=None
    settings: Optional[GlobalSettings]=None

    def desc(self,
             style_guide:StyleGuide,
             flavour:DeclarationFlavour=DeclarationFlavour.NONE,
             declarations:DeclarationsMask=DeclarationsMask.ALL
             )->Tuple[Optional[str],DeclarationFlavour,DeclarationsMask]:
        
        # select proper formats
        compositing = sentences[k_description][k_compositing][style_guide.value]

        # pick compisiting format
        compose_loc = random.choice( compositing )

        # recurse
        oscs_desc , flavour , declarations = self._desc_oscillators(style_guide=style_guide,
                                                                   flavour=flavour,
                                                                   declarations=declarations)
        

        # compose sentence
        desc = compose_loc.format(oscs_desc=oscs_desc)

        for regex , repl in cleanup.items():
            desc = re.sub(regex,repl,desc)

        return desc , flavour , declarations        


    def _desc_oscillators(self,
                          style_guide:StyleGuide,
                          flavour:DeclarationFlavour=DeclarationFlavour.NONE,
                          declarations:DeclarationsMask=DeclarationsMask.ALL
                          )->Tuple[Optional[str],DeclarationFlavour,DeclarationsMask]:

        oscillators = list(filter(None,self.oscillators))

        if oscillators is None or len(oscillators)==0:
            return None
        
        # select proper formats
        compositing = sentences[k_oscillators][k_compositing][style_guide.value]
        glues       = sentences[k_oscillators][k_glue][style_guide.value]

        # select which flavours of mix declaration we will pick from ...
        compose_keys = self._filter_compositing_keys(compositing,declarations)
        
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
        oscillators_mix_desc , flavour = self.__get_oscillators_mix_desc(style_guide,flavour,declarations) # in case we need it

        # update the flavour with what we will actually be outputting (some compositing may not include the mixing)
        if (flavour & (DeclarationFlavour.OSCS_MIX_BALANCED|DeclarationFlavour.OSCS_MIX_FORWARD) !=0 and "{oscillators_mix_desc}" not in compose_loc):
            flavour = flavour & ( DeclarationFlavour.ALL - DeclarationFlavour.GRP_OSCS_MIX_ALL ) | DeclarationFlavour.OSCS_MIX_NONE
            declarations = declarations & (DeclarationsMask.ALL - DeclarationsMask.OSC_VOLUME)

        # recurse
        oscillators_descs , flavour , declarations = self.recurse(oscillators,style_guide=style_guide,flavour=flavour,declarations=declarations)

        # compose sentence
        oscillators_desc = glue.join(oscillators_descs)
        oscillators_desc = compose_loc.format(oscillators_desc=oscillators_desc,oscillators_mix_desc=oscillators_mix_desc)

        return oscillators_desc , flavour , declarations
    
    def __get_oscillators_mix_desc(self,style_guide:StyleGuide,flavour:DeclarationFlavour,declarations:DeclarationsMask)->str:

        # we choose a balanced mix flavour but the mix is not balanced ... remove it ...
        if flavour & DeclarationFlavour.OSCS_MIX_BALANCED != 0 and not self._is_osc_mix_balanced():
            flavour = flavour & (DeclarationFlavour.ALL - DeclarationFlavour.OSCS_MIX_BALANCED) 

        if flavour & DeclarationFlavour.OSCS_MIX_FORWARD:
            flavour = flavour & (DeclarationFlavour.ALL - DeclarationFlavour.GRP_OSCS_MIX_ALL) | DeclarationFlavour.OSCS_MIX_FORWARD
            mix_value = self._get_oscillators_mix(style_guide,flavour,declarations)
            if style_guide.value not in sentences[k_oscillators][k_comp_oscs_mix_forward]:
                return None , flavour & (DeclarationFlavour.ALL - DeclarationFlavour.GRP_OSCS_MIX_ALL) | DeclarationFlavour.OSCS_MIX_NONE
            compositing_mix = random.choice( sentences[k_oscillators][k_comp_oscs_mix_forward][style_guide.value] )
            mix_desc = compositing_mix.format(oscillators_mix=mix_value)
            return mix_desc , flavour
        elif flavour & DeclarationFlavour.OSCS_MIX_BALANCED:
            flavour = flavour & (DeclarationFlavour.ALL - DeclarationFlavour.GRP_OSCS_MIX_ALL) | DeclarationFlavour.OSCS_MIX_BALANCED
            mix_value = self._get_oscillators_mix(style_guide,flavour,declarations)
            if style_guide.value not in sentences[k_oscillators][k_comp_oscs_mix_forward]:
                return None , flavour & (DeclarationFlavour.ALL - DeclarationFlavour.GRP_OSCS_MIX_ALL) | DeclarationFlavour.OSCS_MIX_NONE
            compositing_mix = random.choice( sentences[k_oscillators][k_comp_oscs_mix_balanced][style_guide.value] )
            mix_desc = compositing_mix.format(oscillators_mix=mix_value)
            return mix_desc , flavour
        elif flavour & DeclarationFlavour.OSCS_MIX_DEFAULT:
            flavour = flavour & (DeclarationFlavour.ALL - DeclarationFlavour.GRP_OSCS_MIX_ALL) | DeclarationFlavour.OSCS_MIX_DEFAULT
            mix_value = self._get_oscillators_mix(style_guide,flavour,declarations)
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
            if self._is_osc_mix_balanced():
                flavours.append(DeclarationFlavour.OSCS_MIX_BALANCED) 

            flavour_select = random.choice(flavours)
            flavour = flavour & (DeclarationFlavour.ALL - DeclarationFlavour.GRP_OSCS_MIX_ALL) | flavour_select
            return self.__get_oscillators_mix_desc(style_guide=style_guide,flavour=flavour,declarations=declarations)    
    
    def _get_oscillators_mix(self,style_guide:StyleGuide,flavour:DeclarationFlavour,declarations:DeclarationsMask)->str:
        total_vol = 0.0
        for osc in self.oscillators:
            total_vol += osc.volume
        multiplier = 1 / total_vol if total_vol != 0.0 else 1.0
        match style_guide:
            case StyleGuide.BASIC:
                volumes = [ f"{round(100.0*osc.volume*multiplier)}" for osc in self.oscillators]
                return "/".join(volumes)
            case StyleGuide.SUCCINT:
                volumes = [ f"{round(100.0*osc.volume*multiplier)}%" for osc in self.oscillators]
                return "/".join(volumes)
            case StyleGuide.CONCISE:
                volumes = [ f"{round(100.0*osc.volume*multiplier)}%" for osc in self.oscillators]
                return "/".join(volumes)
            case StyleGuide.DETAILED:
                volumes = [ f"{round(100.0*osc.volume*multiplier,2)}%" for osc in self.oscillators]
                return "/".join(volumes)
            case StyleGuide.SPECIFICATION:
                volumes = [ f"{round(100.0*osc.volume*multiplier,2)}%" for osc in self.oscillators]
                return "/".join(volumes)

    def _is_osc_mix_balanced(self)->bool:
        if self.oscillators is None or len(self.oscillators)==1:
            return False
        vol_total = 0.0
        for osc in self.oscillators:
            vol_total += osc.volume

        if vol_total==0.0:
            return True
        vol_avg = vol_total / len(self.oscillators)

        for osc in self.oscillators:
            if osc.volume > vol_avg * 1.2 or osc.volume < vol_avg * 0.8 :
                return False
            
        return True
    
    def _filter_compositing_keys(self,compositing:dict,declarations:DeclarationsMask):
        # use_mix = (declarations & DeclarationsMask.OSC_VOLUME != 0)
        # use_balanced = self._is_osc_mix_balanced()
        compositing_copy = compositing.copy()
        if len(self.oscillators)==1:
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





