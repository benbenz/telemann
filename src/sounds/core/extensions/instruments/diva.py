
from .base import InstrumentExtension
from pedalboard import AudioProcessorParameter, ExternalPlugin
from sounds.models import SoundSource 
from typing import List
from ..schema import *

VOL_THRESH = 0.05 


class DivaExtension(InstrumentExtension):

    def arp_disable(self, instrument):     
        self.arp_set(instrument,0.0)

    def arp_is_on(self, instrument)->bool:     
        return self.arp_get(instrument)==1.0

    def arp_get(self, instrument)->float|List:     
        if 'arp_onoff' in instrument.parameters: # VST plugin
            return instrument.parameters['arp_onoff'].raw_value
        elif 'arpeggiator_onoff' in instrument.parameters: # AudioUnit
            return instrument.parameters['arpeggiator_onoff'].raw_value

    def arp_set(self, instrument, value: float|List):
        if 'arp_onoff' in instrument.parameters: # VST plugin
            instrument.parameters['arp_onoff'].raw_value = value
        elif 'arpeggiator_onoff' in instrument.parameters: # AudioUnit
            instrument.parameters['arpeggiator_onoff'].raw_value = value

    def analyze_sound(self, parameters:dict) -> SoundToneDescription:

        oscs = self._get_oscs(parameters)

        filters = self._get_filters(parameters)

        return SoundToneDescription(
            oscillators=oscs,
        )



############################################################################################################
#
# OSC section
#
############################################################################################################        

    def _get_oscs(self,params:dict)->List[Oscillator]:
        oscs = []
        model = params['osc_model']['value'] #instrument.parameters['model'].string_value
        if model == '0': #'Triple VCO':
            oscs = self._get_oscs_triple(params,3)
        elif model == '1': #'Dual VCO':
            oscs = self._get_oscs_dual(params)
        elif model == '2': #'DCO':
            oscs = self._get_oscs_dco(params)
        elif model == '3': #'Dual VCO Eco':
            oscs = self._get_oscs_eco(params,2)
        elif model == '4': #'Digital':
            oscs = self._get_oscs_digital(params,2)
        return oscs



    def _get_oscs_triple(self,params:dict,count:int)->List[Oscillator]:
        oscs = []
        for i in range(count):
            i_vco = i+1
            vol = self._get_osc_volume(params,i_vco)
            if vol > VOL_THRESH:
                oscs.append(Oscillator(shapes=self._get_osc_shapes_continuous(params,i_vco),
                               sub=False,
                               volume=vol))
        return oscs 
    
    def _get_oscs_dual(self,params:dict)->List[Oscillator]:
        oscs = []
        mix = params['osc_oscmix']['raw_value']
        if mix < 1.0 - VOL_THRESH : # OSC1 has significant volume
            oscs.append(Oscillator(shapes=self._get_osc_shapes_additive(params,1),
                               volume=self._get_osc_volume_simple(params,1),
                                sub=False))
        if mix > VOL_THRESH : # OSC2 has significant volume
            oscs.append(Oscillator(shapes=self._get_osc_shapes_additive(params,2),
                               volume=self._get_osc_volume_simple(params,2),
                                sub=False))
        return oscs     
    
    def _get_oscs_dco(self,params:dict) -> List[Oscillator] :
        oscs = []
        pulse_shape = params[f"osc_pulseshape"]["value"]
        saw_shape = params[f"osc_sawshape"]["value"]
        sub_shape = params[f"osc_suboscshape"]["value"]
        sub_vol = params[f"volume3"]["raw_value"]
        if pulse_shape != "0":
            oscs.append(Oscillator(shapes=[OscillatorShape(shape=OscillatorShapeEnum.PULSE)],
                                volume=1.0,
                                sub=False))
        if saw_shape != "0":
            oscs.append(Oscillator(shapes=[OscillatorShape(shape=OscillatorShapeEnum.SAWTOOTH)],
                                volume=1.0,
                                sub=False))
        if sub_vol > VOL_THRESH:
            oscs.append(Oscillator(shapes=[OscillatorShape(shape=OscillatorShapeEnum.SAWTOOTH)],
                                volume=sub_vol,
                                sub=True))
        return oscs
    
    def _get_oscs_eco(self,params:dict,count:int) -> List[Oscillator] :
        oscs = []
        for i in range(count):
            i_vco = i+1
            vol = self._get_osc_volume(params,i_vco)
            if vol > VOL_THRESH: 
                shapes = self._get_osc_shapes_eco(params,i_vco)
                if shapes is not None:
                    oscs.append(
                        Oscillator(shapes=shapes,volume=vol,sub=False)
                    )
        return oscs     
    
    def _get_oscs_digital(self,params:dict,count:int) -> List[Oscillator]:
        oscs = []
        for i in range(count):
            i_vco = i+1
            vol = self._get_osc_volume_simple(params,i_vco)
            if vol > VOL_THRESH: 
                shapes = self._get_osc_shapes_digital(params,i_vco)
                if shapes is not None:
                    oscs.append(
                            Oscillator(shapes=shapes,volume=vol,sub=False)
                    )
        return oscs        

    
    def _get_osc_shapes_continuous(self,params:dict,i:int) -> List[OscillatorShape]:
        shapes = []
        osc_shape = params[f"osc_shape{i}"]["value"]
        osc_shape = float(osc_shape)
        th_offset = 0.2
        if osc_shape <= 1.0 + th_offset:
            shapes = [ OscillatorShape(shape=OscillatorShapeEnum.SAWUP) ]
        elif osc_shape <= 2.0:
            shapes = [ OscillatorShape(shape=OscillatorShapeEnum.SAWUP) , OscillatorShape(shape=OscillatorShapeEnum.TRIANGLE) ]
        elif osc_shape <= 3.0 - th_offset:
            shapes = [ OscillatorShape(shape=OscillatorShapeEnum.TRIANGLE) , OscillatorShape(shape=OscillatorShapeEnum.SAWUP) ]
        elif osc_shape <= 3.0 + th_offset:
            shapes = [ OscillatorShape(shape=OscillatorShapeEnum.TRIANGLE) ]
        elif osc_shape <= 4.0:
            shapes = [ OscillatorShape(shape=OscillatorShapeEnum.TRIANGLE) , OscillatorShape(shape=OscillatorShapeEnum.SAWDOWN) ]
        elif osc_shape <= 5.0 - th_offset:
            shapes = [ OscillatorShape(shape=OscillatorShapeEnum.SAWDOWN) , OscillatorShape(shape=OscillatorShapeEnum.TRIANGLE) ]
        elif osc_shape <= 5.0 + th_offset:
            shapes = [ OscillatorShape(shape=OscillatorShapeEnum.SAWDOWN) ]
        elif osc_shape <= 6.0:
            shapes = [ OscillatorShape(shape=OscillatorShapeEnum.SAWDOWN) , OscillatorShape(shape=OscillatorShapeEnum.PULSE) ]
        elif osc_shape <= 7.0 - th_offset:
            shapes = [ OscillatorShape(shape=OscillatorShapeEnum.PULSE) , OscillatorShape(shape=OscillatorShapeEnum.SAWDOWN) ]
        elif osc_shape <= 7.0 + th_offset:
            shapes = [ OscillatorShape(shape=OscillatorShapeEnum.PULSE)]
        elif osc_shape <= 8.0:
            shapes = [ OscillatorShape(shape=OscillatorShapeEnum.PULSE) , OscillatorShape(shape=OscillatorShapeEnum.PULSE_THIN)]
        elif osc_shape <= 9.0 - th_offset:
            shapes = [ OscillatorShape(shape=OscillatorShapeEnum.PULSE_THIN) , OscillatorShape(shape=OscillatorShapeEnum.PULSE)]
        elif osc_shape >= 9.0 - th_offset:
            shapes = [ OscillatorShape(shape=OscillatorShapeEnum.PULSE_THIN)]

        return shapes
    
    def _get_osc_shapes_eco(self,params:dict,i:int) -> List[OscillatorShape]:
        shapes = []
        osc_shape = params[f"osc_shape{i}"]["value"]
        osc_shape = float(osc_shape)
        if i==1:
            if osc_shape == 1.0:
                shapes = [ OscillatorShape(shape=OscillatorShapeEnum.TRIANGLE) ]
            elif osc_shape == 2.0:
                shapes = [ OscillatorShape(shape=OscillatorShapeEnum.SAWDOWN) ]
            elif osc_shape == 3.0:
                shapes = [ OscillatorShape(shape=OscillatorShapeEnum.PULSE) ]
            elif osc_shape == 4.0:
                shapes = [ OscillatorShape(shape=OscillatorShapeEnum.NOISE) ]
        elif i==2:
            if osc_shape == 1.0:
                shapes = [ OscillatorShape(shape=OscillatorShapeEnum.SAWDOWN) ]
            elif osc_shape == 2.0:
                shapes = [ OscillatorShape(shape=OscillatorShapeEnum.PULSE) ]
            elif osc_shape == 3.0:
                shapes = [ OscillatorShape(shape=OscillatorShapeEnum.PULSE_THIN) ]
            elif osc_shape == 4.0:
                shapes = None # ring mod
        return shapes
    
    def _get_osc_volume(self,params:dict,i_vco:int) -> float:
        return params[f"osc_volume{i_vco}"]["raw_value"]
    
    def _get_osc_shapes_additive(self,params,i_vco:int) -> List[OscillatorShape]:
        shapes = []
        triangle = params[f"osc_triangle{i_vco}on"]["raw_value"]
        if triangle == 1.0:
            shapes.append( OscillatorShape(shape=OscillatorShapeEnum.TRIANGLE) )
        saw = params[f"osc_saw{i_vco}on"]["raw_value"]
        if saw == 1.0:
            shapes.append( OscillatorShape(shape=OscillatorShapeEnum.SAWUP) )
        if i_vco==1:
            pwm = params[f"osc_pwm{i_vco}on"]["raw_value"]
            if pwm == 1.0:
                shapes.append( OscillatorShape(shape=OscillatorShapeEnum.PULSE) )
            noise = params[f"osc_noise{i_vco}on"]["raw_value"]
            if noise == 1.0:
                shapes.append( OscillatorShape(shape=OscillatorShapeEnum.NOISE) )
        if i_vco==2:
            pulse = params[f"osc_pulse{i_vco}on"]["raw_value"]
            if pulse == 1.0:
                shapes.append( OscillatorShape(shape=OscillatorShapeEnum.PULSE) )
            sine = params[f"osc_sine{i_vco}on"]["raw_value"]
            if sine == 1.0:
                shapes.append( OscillatorShape(shape=OscillatorShapeEnum.SINE) )
        return shapes
    
    def _get_osc_volume_simple(self,params,i_vco:int) -> float:
        mix = params['osc_oscmix']['raw_value']
        if i_vco==1:
            return 1.0 - mix
        elif i_vco ==2:
            return mix 
    
    def _get_osc_shapes_digital(self,params:dict,i_vco:int) -> List[OscillatorShape]:
        shapes = []
        osc_shape = params[f"osc_digitaltype{i}"]["value"]
        osc_shape = int(osc_shape)
        if osc_shape == 1:
            shapes = [ OscillatorShape(shape=OscillatorShapeEnum.SAWMULTI) ]
        elif osc_shape == 2:
            shapes = [ OscillatorShape(shape=OscillatorShapeEnum.TRISHAPED) ]
        elif osc_shape == 3:
            shapes = [ OscillatorShape(shape=OscillatorShapeEnum.NOISE) ]
        elif osc_shape == 4:
            shapes = [ OscillatorShape(shape=OscillatorShapeEnum.FEEDBACK) ]
        elif osc_shape == 5:
            shapes = [ OscillatorShape(shape=OscillatorShapeEnum.PULSE) ]
        elif osc_shape == 6:
            shapes = [ OscillatorShape(shape=OscillatorShapeEnum.SAWTOOTH) ]
        elif osc_shape == 7:
            shapes = [ OscillatorShape(shape=OscillatorShapeEnum.TRIANGLE) ]

        return shapes

############################################################################################################
#
# Filters section
#
############################################################################################################        

    def _get_filters(self,params):

        filters = []

        model_hpf = params['hpf_model']['value']

        return None 
