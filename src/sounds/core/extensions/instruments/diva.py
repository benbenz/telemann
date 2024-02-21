
from .base import InstrumentExtension , OscShape
from pedalboard import AudioProcessorParameter, ExternalPlugin
from sounds.models import SoundSource 
from typing import List


VOL_THRESH = 0.05 


class DivaExtension(InstrumentExtension):

    def generate_text(self,sound_info):
        return "not implemented"

    def arp_off(self, instrument)->float:
        return instrument.parameters['onoff'].raw_value

    def arp_set(self, instrument, value: float):
        instrument.parameters['onoff'].raw_value = value

    def analyze_sound(self, source:SoundSource, instrument:ExternalPlugin, sound_info:dict):

        params = sound_info['parameters']

        sound_info['analysis']['oscs'] = self._get_oscs(params)


    def _get_oscs(self,params:dict):
        oscs = []
        model = params['model']['value'] #instrument.parameters['model'].string_value
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
        mix = params['oscmix']['raw_value']
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
        pulse_shape = params[f"pulseshape"]["value"]
        saw_shape = params[f"sawshape"]["value"]
        sub_shape = params[f"suboscshape"]["value"]
        if pulse_shape != "off":
            oscs.append({
                "shapes":[OscShape.PULSE] ,
                "volume": 1.0 ,
                "sub":False
            })
        if saw_shape != "off":
            oscs.append({
                "shapes":[OscShape.SAWTOOTH] ,
                "volume": 1.0,
                "sub":False
            })
        if sub_shape != "off":
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
                            "volume" : self._get_osc_volume(params,i_vco),
                            "sub":False
                        }
                    )
        return oscs     

    
    def _get_osc_shapes_continuous(self,params:dict,i:int) -> List[OscShape]:
        shapes = []
        osc_shape = params[f"shape{i}"]["value"]
        osc_shape = float(osc_shape)
        if osc_shape == 1.0:
            shapes = [ OscShape.SAWUP ]
        elif osc_shape <= 1.5:
            shapes = [ OscShape.SAWUP , OscShape.TRIANGLE ]
        elif osc_shape <= 2.5:
            shapes = [ OscShape.TRIANGLE , OscShape.SAWUP ]
        elif osc_shape <= 3.0:
            shapes = [ OscShape.TRIANGLE ]
        elif osc_shape <= 3.5:
            shapes = [ OscShape.TRIANGLE , OscShape.SAWDOWN ]
        elif osc_shape <= 4.5:
            shapes = [ OscShape.SAWDOWN , OscShape.TRIANGLE ]
        elif osc_shape <= 5.5:
            shapes = [ OscShape.SAWDOWN ]
        elif osc_shape <= 5.5:
            shapes = [ OscShape.SAWDOWN , OscShape.SQUARE]
        elif osc_shape <= 6.5:
            shapes = [ OscShape.SQUARE , OscShape.SAWDOWN ]
        elif osc_shape < 9.0:
            shapes = [ OscShape.SQUARE]
        elif osc_shape == 9.0:
            shapes = [ OscShape.PULSE_THIN]

        return shapes
    
    def _get_osc_shapes_eco(self,params:dict,i:int) -> List[OscShape]:
        shapes = []
        osc_shape = params[f"shape{i}"]["value"]
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
        return params[f"volume{i_vco}"]["raw_value"]
    
    def _get_osc_shapes_additive(self,params,i_vco:int) -> List[OscShape]:
        shapes = []
        triangle = params[f"triangle{i_vco}on"]["raw_value"]
        if triangle == 1.0:
            shapes.append( OscShape.TRIANGLE )
        saw = params[f"saw{i_vco}on"]["raw_value"]
        if saw == 1.0:
            shapes.append( OscShape.SAWUP )
        if i_vco==1:
            pwm = params[f"pwm{i_vco}on"]["raw_value"]
            if pwm == 1.0:
                shapes.append( OscShape.PULSE )
            noise = params[f"noise{i_vco}on"]["raw_value"]
            if noise == 1.0:
                shapes.append( OscShape.NOISE )
        if i_vco==2:
            pulse = params[f"pulse{i_vco}on"]["raw_value"]
            if pulse == 1.0:
                shapes.append( OscShape.PULSE )
            sine = params[f"sine{i_vco}on"]["raw_value"]
            if sine == 1.0:
                shapes.append( OscShape.SINE )
        return shapes
    
    def _get_osc_volume_simple(self,params,i_vco:int) -> float:
        mix = params['oscmix']['raw_value']
        if i_vco==1:
            return 1.0 - mix
        elif i_vco ==2:
            return mix 


