from typing import List , Optional , Tuple
from abc import ABC , abstractmethod
from pydantic import BaseModel , confloat
from .compositing.locale_en import sentences , words
from .compositing.keys import * # import the k_*** keys
from .defs import *
import random
import math

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
    
class ExtensionComponent(BaseModel,ABC):

    @abstractmethod
    def desc(self,style_guide:StyleGuide,declarations:DeclarationsMask=DeclarationsMask.ALL)->Tuple[Optional[str],DeclarationsMask]:
        pass


    def recurse(self,children:list,style_guide:StyleGuide,declarations:DeclarationsMask,limit:Optional[int]=None):
        descs = []
        declarations_ = []
        count = 1
        for child in children:
            if limit is not None and count>limit:
                break 
            desc , declaration_ = child.desc(style_guide,declarations)
            if desc is not None:
                declarations_.append(declaration_)
                descs.append(desc)
        for declaration_  in declarations_:
            declarations &= declaration_
        return descs , declarations


class Envelope(ExtensionComponent):

    attack : confloat(ge=0.0,le=1.0)
    decay  : confloat(ge=0.0,le=1.0)
    sustain: confloat(ge=0.0,le=1.0)
    release: confloat(ge=0.0,le=1.0)
    type   : EnvelopeType

    def desc(self,style_guide:StyleGuide,declarations:DeclarationsMask=DeclarationsMask.ALL)->Tuple[Optional[str],DeclarationsMask]:
        return None    
    
class LFO(ExtensionComponent):

    waveform: WaveformEnum
    frequency : confloat(ge=0.0,le=1.0)
    delay : confloat(ge=0.0,le=1.0)

    def desc(self,style_guide:StyleGuide,declarations:DeclarationsMask=DeclarationsMask.ALL)->Tuple[Optional[str],DeclarationsMask]:
        return None,declarations   

class OscillatorShape(ExtensionComponent):

    waveform : WaveformEnum
    volume : confloat(ge=0.0,le=1.0)|None=None

    def desc(self,style_guide:StyleGuide,declarations:DeclarationsMask=DeclarationsMask.ALL)->Tuple[Optional[str],DeclarationsMask]:

        # select proper formats
        compositing = sentences[k_shape][k_compositing][style_guide.value]

        # select which flavour of mix declaration we will take ...
        compose_keys = self._filter_compositing_keys(compositing,declarations)
        
        # pick compisiting formats and strings
        flavour_key = random.choice( compose_keys ) 
        compose_loc = random.choice( compositing[flavour_key] )

        # update declarations: if we used "vol_*" we can tell the children that its been used
        has_volume   = flavour_key in [k_shape_w_vol]
        declarations = declarations & (DeclarationsMask.ALL - DeclarationsMask.SHAPE_LEVEL) if has_volume  else declarations

        # recurse
        # no recursion

        # compose sentence
        waveform_name = words[self.waveform.value]
        volume_desc = self._get_volume_desc(style_guide,declarations) # in case we need it
        shape_desc = compose_loc.format(waveform_name=waveform_name,volume_desc=volume_desc)

        return shape_desc , declarations   

    def _filter_compositing_keys(self,compositing:dict,declarations:DeclarationsMask):
        # lets add the volume info if we want it
        use_vol = (declarations & DeclarationsMask.SHAPE_LEVEL != 0)
        compositing_copy = compositing.copy()
        if not use_vol:
            compositing_copy.pop(k_shape_w_vol,None)
        else:
            compositing_copy.pop(k_shape_no_vol,None)

        assert len(compositing_copy) > 0
        return list(compositing_copy.keys())    

    def _get_volume_desc(self,style_guide:StyleGuide,declarations:DeclarationsMask)->str:
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
    
class Oscillator(ExtensionComponent):

    shapes : List[OscillatorShape]=[]
    volume : confloat(ge=0.0,le=1.0)
    sub : bool 

    # when we used balanced writing, we won't output the volumes ...
    def desc(self,style_guide:StyleGuide,declarations:DeclarationsMask=DeclarationsMask.ALL)->Tuple[Optional[str],DeclarationsMask]:

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
        osc_type    = random.choice( osc_type[k_osc_sub] if self.sub else osc_type[k_osc_sub_not])
        osc_article = random.choice( osc_article[k_osc_sub] if self.sub else osc_article[k_osc_sub_not])

        # update declarations: if we used "vol_*" we can tell the children that its been used
        has_osc_vol = flavour_key in [k_osc_vol_plural,k_osc_vol_singular]
        declarations = declarations & (DeclarationsMask.ALL - DeclarationsMask.OSC_LEVEL) if has_osc_vol  else declarations
        # lets not show the shape level if the oscillator doesn't blend shapes
        use_shape_vol = len(shapes)>1 and random.random()>0.5
        declarations = declarations & (DeclarationsMask.ALL - DeclarationsMask.SHAPE_LEVEL) if not use_shape_vol  else declarations

        # recurse
        limit = 1 if style_guide in [ StyleGuide.BASIC , StyleGuide.SUCCINT ] else None # we only look at the first Shape in those modes
        shapes_desc , declarations = self.recurse(shapes,style_guide=style_guide,declarations=declarations,limit=limit)

        # compose sentence
        shapes_desc = glue.join(shapes_desc)
        volume_desc = self._get_volume_desc(style_guide,declarations) # in case we need it
        shapes_desc = compose_loc.format(shapes_desc=shapes_desc,volume_desc=volume_desc,osc_type=osc_type,osc_article=osc_article)

        return shapes_desc , declarations
    
    def _filter_compositing_keys(self,compositing:dict,declarations:DeclarationsMask):
        # lets add the volume info if we want it
        use_vol = (declarations & DeclarationsMask.OSC_LEVEL != 0)
        compositing_copy = compositing.copy()
        if len(self.shapes)==1:
            compositing_copy.pop(k_osc_plural,None)
            compositing_copy.pop(k_osc_vol_plural,None)
        else:
            compositing_copy.pop(k_osc_singular,None)
            compositing_copy.pop(k_osc_vol_singular,None)
        if not use_vol:
            compositing_copy.pop(k_osc_vol_plural,None)
            compositing_copy.pop(k_osc_vol_singular,None)
        else:
            compositing_copy.pop(k_osc_plural,None)
            compositing_copy.pop(k_osc_singular,None)

        assert len(compositing_copy) > 0
        return list(compositing_copy.keys())

    def _get_volume_desc(self,style_guide:StyleGuide,declarations:DeclarationsMask)->str:
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

    
class Filter(ExtensionComponent):

    def desc(self,style_guide:StyleGuide,declarations:DeclarationsMask=DeclarationsMask.ALL)->Tuple[Optional[str],DeclarationsMask]:
        return None , declarations

class Modulation(ExtensionComponent):

    source_id  : ModulationSourceID
    source     : Optional[Oscillator|LFO|Envelope]=None
    dest_id    : ModulationDestID
    dest       : Optional[Oscillator|Filter|LFO|Envelope]=None
    dest_param : ModulationDestParam
    level      : confloat(ge=0.0,le=1.0)

    def desc(self,style_guide:StyleGuide,declarations:DeclarationsMask=DeclarationsMask.ALL)->Tuple[Optional[str],DeclarationsMask]:
        return None , declarations
        
class ModulationMatrix(ExtensionComponent):

    modulations : List[Modulation]=[]
    # pwm   : Optional[List[Modulation]]=None
    # pitch : Optional[List[Modulation]]=None
    # ring  : Optional[List[ModulationSource]]=None
    # cross : Optional[List[ModulationSource]]=None
    # sync  : Optional[List[ModulationSource]]=None

    def desc(self,style_guide:StyleGuide,declarations:DeclarationsMask=DeclarationsMask.ALL)->Tuple[Optional[str],DeclarationsMask]:
        return None , declarations
    
    def add_modulation(self,modulation:Modulation):
        self.modulations.append(modulation)

class Effect(ExtensionComponent):

    type : EffectType

    def desc(self,style_guide:StyleGuide,declarations:DeclarationsMask=DeclarationsMask.ALL)->Tuple[Optional[str],DeclarationsMask]:
        return None , declarations



class SoundToneDescription(ExtensionComponent):

    oscillators:Optional[List[Oscillator]]=None
    filters: Optional[List[Filter]]=None
    envelopes: Optional[List[Envelope]]=None 
    lfos: Optional[List[LFO]]=None
    effects: Optional[List[Effect]]=None
    mod_matrix: Optional[ModulationMatrix]=None

    def desc(self,style_guide:StyleGuide,declarations:DeclarationsMask=DeclarationsMask.ALL)->Tuple[Optional[str],DeclarationsMask]:

        osc_desc , declarations = self._desc_oscillators(style_guide=style_guide,declarations=declarations)

        return osc_desc , declarations
    
    def _desc_oscillators(self,style_guide:StyleGuide,declarations:DeclarationsMask=DeclarationsMask.ALL)->Tuple[Optional[str],DeclarationsMask]:

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

        # update declarations: if we used "mix_balanced" or "mix", this is a forward declaration and we should consider OSC_LEVEL declared
        is_forward_decl = flavour_key in [k_oscs_mix_balanced,k_oscs_mix_forward]
        declarations    = declarations & (DeclarationsMask.ALL - DeclarationsMask.OSC_LEVEL) if is_forward_decl  else declarations

        # recurse
        oscillators_descs , declarations = self.recurse(oscillators,style_guide=style_guide,declarations=declarations)

        # compose sentence
        oscillators_desc = glue.join(oscillators_descs)
        oscillators_mix  = self._get_oscillators_mix(style_guide,declarations) # in case we need it
        oscillators_desc = compose_loc.format(oscillators_desc=oscillators_desc,oscillators_mix=oscillators_mix)

        return oscillators_desc , declarations
    
    def _get_oscillators_mix(self,style_guide:StyleGuide,declarations:DeclarationsMask)->str:
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
        use_mix = (declarations & DeclarationsMask.OSC_LEVEL != 0)
        use_balanced = self._is_osc_mix_balanced()
        compositing_copy = compositing.copy()
        if len(self.oscillators)==1:
            compositing_copy.pop(k_oscs_plural,None)
            compositing_copy.pop(k_oscs_mix_forward,None)
            compositing_copy.pop(k_oscs_mix_balanced,None)
        else:
            compositing_copy.pop(k_oscs_singular,None)
        if not use_mix:
            compositing_copy.pop(k_oscs_mix_forward,None)
            compositing_copy.pop(k_oscs_mix_balanced)
        if not use_balanced:
            compositing_copy.pop(k_oscs_mix_balanced,None)
        assert len(compositing_copy) > 0
        return list(compositing_copy.keys())     





