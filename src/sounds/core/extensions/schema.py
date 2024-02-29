from typing import List , Optional
from abc import ABC , abstractmethod
from pydantic import BaseModel , confloat
from .compositing.locale_en import sentences
from .compositing.keys import * # import the k_*** keys
from .defs import *
import random
    
class ExtensionComponent(BaseModel,ABC):

    @abstractmethod
    def desc(self,style_guide:StyleGuide,declarations:DeclarationsMask=DeclarationsMask.ALL)->Optional[str]:
        pass

class Envelope(ExtensionComponent):

    attack : confloat(ge=0.0,le=1.0)
    decay  : confloat(ge=0.0,le=1.0)
    sustain: confloat(ge=0.0,le=1.0)
    release: confloat(ge=0.0,le=1.0)
    type   : EnvelopeType

    def desc(self,style_guide:StyleGuide,declarations:DeclarationsMask=DeclarationsMask.ALL)->Optional[str]:
        return None    
    
class LFO(ExtensionComponent):

    shape: OscillatorShapeEnum
    frequency : confloat(ge=0.0,le=1.0)
    delay : confloat(ge=0.0,le=1.0)

    def desc(self,style_guide:StyleGuide,declarations:DeclarationsMask=DeclarationsMask.ALL)->Optional[str]:
        return None     

class OscillatorShape(ExtensionComponent):

    shape : OscillatorShapeEnum
    volume : confloat(ge=0.0,le=1.0)|None=None

    def desc(self,style_guide:StyleGuide,declarations:DeclarationsMask=DeclarationsMask.ALL)->Optional[str]:
        return None
    
class Oscillator(ExtensionComponent):

    shapes : List[OscillatorShape]=[]
    volume : confloat(ge=0.0,le=1.0)
    sub : bool 

    # when we used balanced writing, we won't output the volumes ...
    def desc(self,style_guide:StyleGuide,declarations:DeclarationsMask=DeclarationsMask.ALL)->Optional[str]:
        return "an oscillator"
    
class Filter(ExtensionComponent):

    def desc(self,style_guide:StyleGuide,declarations:DeclarationsMask=DeclarationsMask.ALL)->Optional[str]:
        return None

class Modulation(ExtensionComponent):

    source_id  : ModulationSourceID
    source     : Optional[Oscillator|LFO|Envelope]=None
    dest_id    : ModulationDestID
    dest       : Optional[Oscillator|Filter|LFO|Envelope]=None
    dest_param : ModulationDestParam
    level      : confloat(ge=0.0,le=1.0)

    def desc(self,style_guide:StyleGuide,declarations:DeclarationsMask=DeclarationsMask.ALL)->Optional[str]:
        return None
        
class ModulationMatrix(ExtensionComponent):

    modulations : List[Modulation]=[]
    # pwm   : Optional[List[Modulation]]=None
    # pitch : Optional[List[Modulation]]=None
    # ring  : Optional[List[ModulationSource]]=None
    # cross : Optional[List[ModulationSource]]=None
    # sync  : Optional[List[ModulationSource]]=None

    def desc(self,style_guide:StyleGuide,declarations:DeclarationsMask=DeclarationsMask.ALL)->Optional[str]:
        return None
    
    def add_modulation(self,modulation:Modulation):
        self.modulations.append(modulation)

class Effect(ExtensionComponent):

    type : EffectType

    def desc(self,style_guide:StyleGuide,declarations:DeclarationsMask=DeclarationsMask.ALL)->Optional[str]:
        return None


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

    
class SoundToneDescription(ExtensionComponent):

    oscillators:Optional[List[Oscillator]]=None
    filters: Optional[List[Filter]]=None
    envelopes: Optional[List[Envelope]]=None 
    lfos: Optional[List[LFO]]=None
    effects: Optional[List[Effect]]=None
    mod_matrix: Optional[ModulationMatrix]=None

    def desc(self,style_guide:StyleGuide,declarations:DeclarationsMask=DeclarationsMask.ALL)->Optional[str]:

        osc_desc = self._desc_oscillators(style_guide=style_guide,declarations=declarations)

        return osc_desc
    
    def _desc_oscillators(self,style_guide:StyleGuide,declarations:DeclarationsMask=DeclarationsMask.ALL)->Optional[str]:
        if self.oscillators is None or len(self.oscillators)==0:
            return None
        
        # select proper formats
        compositing = sentences[k_oscillators][k_compositing][style_guide.value]
        glues       = sentences[k_oscillators][k_glue][style_guide.value]

        # select which flavour of mix declaration we will take ...
        declare_mix  = declarations & DeclarationsMask.OSC_MIX
        mix_balanced = self._is_osc_mix_balanced() 
        compose_keys = list(compositing.keys())
        if len(self.oscillators)==1:
            compose_keys.remove(k_plural)
        else:
            compose_keys.remove(k_singular)
        if not declare_mix:
            compose_keys.remove(k_forward_mix)
            compose_keys.remove(k_balanced_mix)
        if not mix_balanced:
            compose_keys.remove(k_balanced_mix)
        assert len(compose_keys) > 0
        flavour_key  = random.choice( compose_keys ) # filter the "balanced" when the mix is not balanced
        compositing_choices = compositing[flavour_key]
        
        # pick compisiting format
        glue        = random.choice( glues )
        compositing = random.choice( compositing_choices )

        # update declarations: if we used "balanced_mix" or "forward_mix", this is a forward declaration and we should consider OSC_MIX declared
        is_forward_decl = flavour_key in [k_balanced_mix,k_forward_mix]
        declarations    = declarations & (DeclarationsMask.ALL - DeclarationsMask.OSC_MIX) if is_forward_decl  else declarations

        # recurse
        oscillators_descs : List = [osc.desc(style_guide,declarations) for osc in self.oscillators]

        # compose sentence
        oscillators_desc_inner = glue.join(oscillators_descs)
        oscillators_desc = compositing.format(oscillators_desc=oscillators_desc_inner)

        return oscillators_desc
    
    def _is_osc_mix_balanced(self):
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







