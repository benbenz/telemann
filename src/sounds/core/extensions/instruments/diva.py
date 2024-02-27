
from .base import InstrumentExtension , OscShape
from pedalboard import AudioProcessorParameter, ExternalPlugin
from sounds.models import SoundSource 
from typing import List


VOL_THRESH = 0.05 


class DivaExtension(InstrumentExtension):

    def generate_text(self,sound_info):
        return "not implemented"

    def arp_off(self, instrument)->float:
        if 'arp_onoff' in instrument.parameters: # VST plugin
            return instrument.parameters['arp_onoff'].raw_value
        elif 'arpeggiator_onoff' in instrument.parameters: # AudioUnit
            return instrument.parameters['arpeggiator_onoff'].raw_value
        return None

    def arp_set(self, instrument, value: float):
        if 'arp_onoff' in instrument.parameters: # VST plugin
            instrument.parameters['arp_onoff'].raw_value = value
        elif 'arpeggiator_onoff' in instrument.parameters: # AudioUnit
            instrument.parameters['arpeggiator_onoff'].raw_value = value

    def analyze_sound(self, source:SoundSource, instrument:ExternalPlugin, sound_info:dict):

        params = sound_info['parameters']

        sound_info['analysis']['oscs'] = self._get_oscs(params)

        sound_info['analysis']['filters'] = self._get_filters(params)

        sound_info['analysis']['envs'] = dict()

        sound_info['analysis']['mod'] = dict()

############################################################################################################
#
# OSC section
#
############################################################################################################        

    def _get_oscs(self,params:dict):
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



    def _get_oscs_triple(self,params:dict,count:int):
        oscs = []
        for i in range(count):
            i_vco = i+1
            vol = self._get_osc_volume(params,i_vco)
            if vol > VOL_THRESH:
                oscs.append(
                    {
                        "shapes" : self._get_osc_shapes_continuous(params,i_vco) ,
                        "volume" : vol ,
                        "sub":False
                    }
                )
        return oscs 
    
    def _get_oscs_dual(self,params:dict):
        oscs = []
        mix = params['osc_oscmix']['raw_value']
        if mix < 1.0 - VOL_THRESH : # OSC1 has significatn volume
            oscs.append(
                {
                    "shapes" : self._get_osc_shapes_additive(params,1) ,
                    "volume" : self._get_osc_volume_simple(params,1),
                    "sub":False
                }
            )
        if mix > VOL_THRESH : # OSC2 has significatn volume
            oscs.append(
                {
                    "shapes" : self._get_osc_shapes_additive(params,2) ,
                    "volume" : self._get_osc_volume_simple(params,2),
                    "sub":False
                }
            )

        return oscs     
    
    def _get_oscs_dco(self,params:dict):
        oscs = []
        pulse_shape = params[f"osc_pulseshape"]["value"]
        saw_shape = params[f"osc_sawshape"]["value"]
        sub_shape = params[f"osc_suboscshape"]["value"]
        if pulse_shape != "0":
            oscs.append({
                "shapes":[OscShape.PULSE] ,
                "volume": 1.0 ,
                "sub":False
            })
        if saw_shape != "0":
            oscs.append({
                "shapes":[OscShape.SAWTOOTH] ,
                "volume": 1.0,
                "sub":False
            })
        if sub_shape != "0":
            oscs.append({
                "shapes":[OscShape.SAWTOOTH] ,
                "volume": params[f"volume3"]["raw_value"],
                "sub":True
            })

        return oscs
    
    def _get_oscs_eco(self,params:dict,count:int):
        oscs = []
        for i in range(count):
            i_vco = i+1
            vol = self._get_osc_volume(params,i_vco)
            if vol > VOL_THRESH: 
                shapes = self._get_osc_shapes_eco(params,i_vco)
                if shapes is not None:
                    oscs.append(
                        {
                            "shapes" : shapes ,
                            "volume" : vol ,
                            "sub":False
                        }
                    )
        return oscs     

    
    def _get_osc_shapes_continuous(self,params:dict,i:int) -> List[OscShape]:
        shapes = []
        osc_shape = params[f"osc_shape{i}"]["value"]
        osc_shape = float(osc_shape)
        th_offset = 0.2
        if osc_shape <= 1.0 + th_offset:
            shapes = [ OscShape.SAWUP ]
        elif osc_shape <= 2.0:
            shapes = [ OscShape.SAWUP , OscShape.TRIANGLE ]
        elif osc_shape <= 3.0 - th_offset:
            shapes = [ OscShape.TRIANGLE , OscShape.SAWUP ]
        elif osc_shape <= 3.0 + th_offset:
            shapes = [ OscShape.TRIANGLE ]
        elif osc_shape <= 4.0:
            shapes = [ OscShape.TRIANGLE , OscShape.SAWDOWN ]
        elif osc_shape <= 5.0 - th_offset:
            shapes = [ OscShape.SAWDOWN , OscShape.TRIANGLE ]
        elif osc_shape <= 5.0 + th_offset:
            shapes = [ OscShape.SAWDOWN ]
        elif osc_shape <= 6.0:
            shapes = [ OscShape.SAWDOWN , OscShape.PULSE]
        elif osc_shape <= 7.0 - th_offset:
            shapes = [ OscShape.PULSE , OscShape.SAWDOWN ]
        elif osc_shape <= 7.0 + th_offset:
            shapes = [ OscShape.PULSE]
        elif osc_shape <= 8.0:
            shapes = [ OscShape.PULSE , OscShape.PULSE_THIN]
        elif osc_shape <= 9.0 - th_offset:
            shapes = [ OscShape.PULSE_THIN , OscShape.PULSE]
        elif osc_shape >= 9.0 - th_offset:
            shapes = [ OscShape.PULSE_THIN]

        return shapes
    
    def _get_osc_shapes_eco(self,params:dict,i:int) -> List[OscShape]:
        shapes = []
        osc_shape = params[f"osc_shape{i}"]["value"]
        osc_shape = float(osc_shape)
        if i==1:
            if osc_shape == 1.0:
                shapes = [ OscShape.TRIANGLE ]
            elif osc_shape == 2.0:
                shapes = [ OscShape.SAWDOWN ]
            elif osc_shape == 3.0:
                shapes = [ OscShape.PULSE ]
            elif osc_shape == 4.0:
                shapes = [ OscShape.NOISE ]
        elif i==2:
            if osc_shape == 1.0:
                shapes = [ OscShape.SAWDOWN ]
            elif osc_shape == 2.0:
                shapes = [ OscShape.PULSE ]
            elif osc_shape == 3.0:
                shapes = [ OscShape.PULSE_THIN ]
            elif osc_shape == 4.0:
                shapes = None # ring mod
        return shapes    
    
    def _get_osc_volume(self,params:dict,i_vco:int) -> float:
        return params[f"osc_volume{i_vco}"]["raw_value"]
    
    def _get_osc_shapes_additive(self,params,i_vco:int) -> List[OscShape]:
        shapes = []
        triangle = params[f"osc_triangle{i_vco}on"]["raw_value"]
        if triangle == 1.0:
            shapes.append( OscShape.TRIANGLE )
        saw = params[f"osc_saw{i_vco}on"]["raw_value"]
        if saw == 1.0:
            shapes.append( OscShape.SAWUP )
        if i_vco==1:
            pwm = params[f"osc_pwm{i_vco}on"]["raw_value"]
            if pwm == 1.0:
                shapes.append( OscShape.PULSE )
            noise = params[f"osc_noise{i_vco}on"]["raw_value"]
            if noise == 1.0:
                shapes.append( OscShape.NOISE )
        if i_vco==2:
            pulse = params[f"osc_pulse{i_vco}on"]["raw_value"]
            if pulse == 1.0:
                shapes.append( OscShape.PULSE )
            sine = params[f"osc_sine{i_vco}on"]["raw_value"]
            if sine == 1.0:
                shapes.append( OscShape.SINE )
        return shapes
    
    def _get_osc_volume_simple(self,params,i_vco:int) -> float:
        mix = params['osc_oscmix']['raw_value']
        if i_vco==1:
            return 1.0 - mix
        elif i_vco ==2:
            return mix 
        

    def _get_oscs_digital(self,params:dict,count:int):
        oscs = []
        for i in range(count):
            i_vco = i+1
            vol = self._get_osc_volume_simple(params,i_vco)
            if vol > VOL_THRESH: 
                shapes = self._get_osc_shapes_digital(params,i_vco)
                if shapes is not None:
                    oscs.append(
                        {
                            "shapes" : shapes ,
                            "volume" : vol , 
                            "sub":False
                        }
                    )
        return oscs    
    
    def _get_osc_shapes_digital(self,params:dict,i_vco:int):
        shapes = []
        osc_shape = params[f"osc_digitaltype{i}"]["value"]
        osc_shape = int(osc_shape)
        if osc_shape == 1:
            shapes = [ OscShape.SAWMULTI ]
        elif osc_shape == 2:
            shapes = [ OscShape.TRISHAPED ]
        elif osc_shape == 3:
            shapes = [ OscShape.NOISE ]
        elif osc_shape == 4:
            shapes = [ OscShape.FEEDBACK ]
        elif osc_shape == 5:
            shapes = [ OscShape.PULSE ]
        elif osc_shape == 6:
            shapes = [ OscShape.SAWTOOTH ]
        elif osc_shape == 7:
            shapes = [ OscShape.TRIANGLE ]

        return shapes          

############################################################################################################
#
# Filters section
#
############################################################################################################        

    def _get_filters(self,params):

        filters = []

        model_hpf = params['hpf_model']['value']

        return filters 
