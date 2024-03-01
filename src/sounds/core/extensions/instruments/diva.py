
from .base import InstrumentExtension
from pedalboard import AudioProcessorParameter, ExternalPlugin
from sounds.models import SoundSource 
from typing import List , NoReturn
from ..schema import *

THRESH = 0.05 

class DivaExtension(InstrumentExtension):

    def arp_disable(self, instrument):     
        self.arp_set(instrument,0.0)

    def arp_is_on(self, instrument)->bool:     
        return self.arp_get(instrument)==1.0

    def arp_get(self, instrument)->float|List[float]:     
        if 'arp_onoff' in instrument.parameters: # VST plugin
            return instrument.parameters['arp_onoff'].raw_value
        elif 'arpeggiator_onoff' in instrument.parameters: # AudioUnit
            return instrument.parameters['arpeggiator_onoff'].raw_value

    def arp_set(self, instrument, value: float|List[float]):
        if 'arp_onoff' in instrument.parameters: # VST plugin
            instrument.parameters['arp_onoff'].raw_value = value
        elif 'arpeggiator_onoff' in instrument.parameters: # AudioUnit
            instrument.parameters['arpeggiator_onoff'].raw_value = value

    def analyze_sound(self, parameters:dict) -> SoundToneDescription:

        # create the modulation matrix
        mod_matrix = ModulationMatrix()

        # retrieve basic oscillator information
        oscs = self._get_oscs(parameters,mod_matrix)

        # get the filters
        filters = self._get_filters(parameters,mod_matrix)

        return SoundToneDescription(
            oscillators=oscs,
            filters=filters,
            mod_matrix=mod_matrix
        )



############################################################################################################
#
# OSC section
#
############################################################################################################        

    def _get_oscs(self,params:dict,mod_matrix:ModulationMatrix)->List[Oscillator]:
        oscs = []
        model = params['osc_model']['value'] #instrument.parameters['model'].string_value
        if model == '0': #'Triple VCO':
            oscs = self._get_oscs_triple(params)
            self._add_oscs_mod_triple(params,mod_matrix)
        elif model == '1': #'Dual VCO':
            oscs = self._get_oscs_dual(params)
            self._add_oscs_mod_dual(params,mod_matrix)
        elif model == '2': #'DCO':
            oscs = self._get_oscs_dco(params)
            self._add_oscs_mod_dco(params,mod_matrix)            
        elif model == '3': #'Dual VCO Eco':
            oscs = self._get_oscs_eco(params)
            self._add_oscs_mod_eco(params,mod_matrix)            
        elif model == '4': #'Digital':
            oscs = self._get_oscs_digital(params)
            self._add_oscs_mod_digital(params,mod_matrix)            
        return oscs


    def _get_oscs_triple(self,params:dict)->List[Oscillator]:
        oscs = []
        for i in range(3):
            i_vco = i+1
            vol = self._get_osc_volume(params,i_vco)
            tune_coarse = self._get_osc_tune_coarse(params,i_vco)
            tune_fine = self._get_osc_tune_fine(params,i_vco)
            if vol > THRESH:
                oscs.append(Oscillator(shapes=self._get_osc_shapes_continuous(params,i_vco),
                               sub=False,
                               volume=vol,
                               tune_coarse=tune_coarse,
                               tune_fine=tune_fine
                               ))
        
        return oscs 
    
    def _get_oscs_dual(self,params:dict)->List[Oscillator]:
        oscs = []
        mix = params['osc_oscmix']['raw_value']
        if mix < 1.0 - THRESH : # OSC1 has significant volume
            oscs.append(Oscillator(shapes=self._get_osc_shapes_additive(params,1),
                               volume=self._get_osc_volume_simple(params,1),
                                sub=False))
        if mix > THRESH : # OSC2 has significant volume
            tune_coarse = self._get_osc_tune_coarse(params,2)
            tune_fine = self._get_osc_tune_fine(params,2)
            oscs.append(Oscillator(shapes=self._get_osc_shapes_additive(params,2),
                               volume=self._get_osc_volume_simple(params,2),
                                sub=False,
                                tune_coarse=tune_coarse,
                                tune_fine=tune_fine))
        return oscs     
    
    def _get_oscs_dco(self,params:dict) -> List[Oscillator] :
        oscs = []
        pulse_shape = params[f"osc_pulseshape"]["value"]
        saw_shape = params[f"osc_sawshape"]["value"]
        sub_shape = params[f"osc_suboscshape"]["value"]
        sub_vol = params[f"osc_volume3"]["raw_value"]
        tune_coarse = self._get_osc_tune_coarse(params,1)
        if pulse_shape != "0":
            pulsewidth = self._get_osc_pwm_width(params)
            oscs.append(Oscillator(shapes=[OscillatorShape(waveform=WaveformEnum.PULSE,volume=1.0,width=pulsewidth)],
                                volume=1.0,
                                sub=False,
                                tune_coarse=tune_coarse))
        if saw_shape != "0":
            oscs.append(Oscillator(shapes=[OscillatorShape(waveform=WaveformEnum.SAWTOOTH,volume=1.0)],
                                volume=1.0,
                                sub=False,
                                tune_coarse=tune_coarse))
        if sub_vol > THRESH:
            oscs.append(Oscillator(shapes=[OscillatorShape(waveform=WaveformEnum.PULSE,volume=1.0)],
                                volume=sub_vol,
                                sub=True,
                                tune_coarse=tune_coarse))
        return oscs
    
    def _get_oscs_eco(self,params:dict) -> List[Oscillator] :
        oscs = []
        for i in range(2):
            i_vco = i+1
            vol = self._get_osc_volume(params,i_vco)
            tune_coarse = self._get_osc_tune_coarse(params,1) if i_vco==2 else None
            tune_fine = self._get_osc_tune_fine(params,1) if i_vco==2 else None
            if vol > THRESH: 
                shapes = self._get_osc_shapes_eco(params,i_vco)
                if shapes is not None:
                    oscs.append(
                        Oscillator(shapes=shapes,
                                   volume=vol,
                                   sub=False,
                                   tune_coarse=tune_coarse,
                                   tune_fine=tune_fine)
                    )
        return oscs     
    
    def _get_oscs_digital(self,params:dict) -> List[Oscillator]:
        oscs = []
        for i in range(2):
            i_vco = i+1
            vol = self._get_osc_volume_simple(params,i_vco)
            tune_coarse = self._get_osc_tune_coarse(params,i_vco)
            tune_fine = self._get_osc_tune_fine(params,i_vco) if i_vco == 2 else None
            detune = params["osc_pulsewidth"]["value"] if i_vco == 1 else params["osc_digitalshape3"]["value"]
            if vol > THRESH: 
                shapes = self._get_osc_shapes_digital(params,i_vco)
                if shapes is not None:
                    oscs.append(
                            Oscillator(shapes=shapes,
                                       volume=vol,
                                       sub=False,
                                       tune_coarse=tune_coarse,
                                       tune_fine=tune_fine,
                                       detune=detune)
                    )
        return oscs        

    
    def _get_osc_shapes_continuous(self,params:dict,i:int) -> List[OscillatorShape]:
        shapes = []
        osc_shape = params[f"osc_shape{i}"]["value"]
        osc_shape = float(osc_shape)
        if osc_shape <= 1.0 + THRESH:
            shapes = [ OscillatorShape(waveform=WaveformEnum.SAWUP,volume=1.0) ]
        elif osc_shape <= 2.0:
            vol1 = ( 3.0 - osc_shape ) / 2
            vol2 = ( osc_shape - 1.0 ) / 2
            shapes = [ OscillatorShape(waveform=WaveformEnum.SAWUP, volume=vol1) , OscillatorShape(waveform=WaveformEnum.TRIANGLE, volume=vol2) ]
        elif osc_shape <= 3.0 - THRESH:
            vol1 = ( 3.0 - osc_shape ) / 2
            vol2 = ( osc_shape - 1.0 ) / 2
            shapes = [ OscillatorShape(waveform=WaveformEnum.TRIANGLE, volume=vol2) , OscillatorShape(waveform=WaveformEnum.SAWUP, volume=vol1) ]
        elif osc_shape <= 3.0 + THRESH:
            shapes = [ OscillatorShape(waveform=WaveformEnum.TRIANGLE, volume=1.0) ]
        elif osc_shape <= 4.0:
            vol1 = ( 5.0 - osc_shape ) / 2
            vol2 = ( osc_shape - 3.0 ) / 2
            shapes = [ OscillatorShape(waveform=WaveformEnum.TRIANGLE, volume=vol1) , OscillatorShape(waveform=WaveformEnum.SAWDOWN, volume=vol2) ]
        elif osc_shape <= 5.0 - THRESH:
            vol1 = ( 5.0 - osc_shape ) / 2
            vol2 = ( osc_shape - 3.0 ) / 2
            shapes = [ OscillatorShape(waveform=WaveformEnum.SAWDOWN, volume=vol2) , OscillatorShape(waveform=WaveformEnum.TRIANGLE, volume=vol1) ]
        elif osc_shape <= 5.0 + THRESH:
            shapes = [ OscillatorShape(waveform=WaveformEnum.SAWDOWN, volume=1.0) ]
        elif osc_shape <= 6.0:
            vol1 = ( 7.0 - osc_shape ) / 2
            vol2 = ( osc_shape - 5.0 ) / 2
            shapes = [ OscillatorShape(waveform=WaveformEnum.SAWDOWN, volume=vol1) , OscillatorShape(waveform=WaveformEnum.PULSE, volume=vol2) ]
        elif osc_shape <= 7.0 - THRESH:
            vol1 = ( 7.0 - osc_shape ) / 2
            vol2 = ( osc_shape - 5.0 ) / 2
            shapes = [ OscillatorShape(waveform=WaveformEnum.PULSE, volume=vol2) , OscillatorShape(waveform=WaveformEnum.SAWDOWN, volume=vol1) ]
        elif osc_shape <= 7.0 + THRESH:
            shapes = [ OscillatorShape(waveform=WaveformEnum.PULSE, volume=1.0)]
        elif osc_shape <= 8.0:
            vol1 = ( 9.0 - osc_shape ) / 2
            vol2 = ( osc_shape - 7.0 ) / 2
            shapes = [ OscillatorShape(waveform=WaveformEnum.PULSE, volume=vol1) , OscillatorShape(waveform=WaveformEnum.PULSE_THIN, volume=vol2)]
        elif osc_shape <= 9.0 - THRESH:
            vol1 = ( 9.0 - osc_shape ) / 2
            vol2 = ( osc_shape - 7.0 ) / 2
            shapes = [ OscillatorShape(waveform=WaveformEnum.PULSE_THIN, volume=vol2) , OscillatorShape(waveform=WaveformEnum.PULSE, volume=vol1)]
        elif osc_shape >= 9.0 - THRESH:
            shapes = [ OscillatorShape(waveform=WaveformEnum.PULSE_THIN,volume=1.0)]

        return shapes
    
    def _get_osc_shapes_eco(self,params:dict,i:int) -> List[OscillatorShape]:
        shapes = []
        osc_shape = params[f"osc_ecowave{i}"]["value"]
        osc_shape = float(osc_shape)
        if i==1:
            if osc_shape == 1.0:
                shapes = [ OscillatorShape(waveform=WaveformEnum.TRIANGLE, volume=1.0) ]
            elif osc_shape == 2.0:
                shapes = [ OscillatorShape(waveform=WaveformEnum.SAWDOWN, volume=1.0) ]
            elif osc_shape == 3.0:
                shapes = [ OscillatorShape(waveform=WaveformEnum.PULSE, volume=1.0) ]
            elif osc_shape == 4.0:
                shapes = [ OscillatorShape(waveform=WaveformEnum.NOISE, volume=1.0) ]
        elif i==2:
            if osc_shape == 1.0:
                shapes = [ OscillatorShape(waveform=WaveformEnum.SAWDOWN, volume=1.0) ]
            elif osc_shape == 2.0:
                shapes = [ OscillatorShape(waveform=WaveformEnum.PULSE, volume=1.0) ]
            elif osc_shape == 3.0:
                shapes = [ OscillatorShape(waveform=WaveformEnum.PULSE_THIN, volume=1.0) ]
            elif osc_shape == 4.0:
                shapes = [ OscillatorShape(waveform=WaveformEnum.SQUARE, volume=1.0) ] # ring mod. page 28 manual: SQUARE + RINGMOD
        return shapes
    
    def _get_osc_shapes_additive(self,params,i_vco:int) -> List[OscillatorShape]:
        shapes = []
        triangle = params[f"osc_triangle{i_vco}on"]["raw_value"]
        if triangle == 1.0:
            shapes.append( OscillatorShape(waveform=WaveformEnum.TRIANGLE,volume=1.0) )
        saw = params[f"osc_saw{i_vco}on"]["raw_value"]
        if saw == 1.0:
            shapes.append( OscillatorShape(waveform=WaveformEnum.SAWUP,volume=1.0) )
        pwm_select = params[f"osc_pwm2on"]["raw_value"]
        if i_vco==1:
            pwm = params[f"osc_pwm{i_vco}on"]["raw_value"]
            if pwm == 1.0:
                # check its width too
                if (i_vco==1 and (pwm_select == 0.0 or pwm_select == 1.0)) or (i_vco==2 and pwm_select == 1.0):
                    pulse_width = self._get_osc_pwm_width(params)
                else:
                    pulse_width = None
                shapes.append( OscillatorShape(waveform=WaveformEnum.PULSE,volume=1.0,width=pulse_width) )
            noise = params[f"osc_noise{i_vco}on"]["raw_value"]
            if noise == 1.0:
                shapes.append( OscillatorShape(waveform=WaveformEnum.NOISE,volume=1.0) )
        if i_vco==2:
            pulse = params[f"osc_pulse{i_vco}on"]["raw_value"]
            if pulse == 1.0:
                # check its width too
                if (i_vco==1 and (pwm_select == 0.0 or pwm_select == 1.0)) or (i_vco==2 and pwm_select == 1.0):
                    pulse_width = self._get_osc_pwm_width(params)
                else:
                    pulse_width = None
                shapes.append( OscillatorShape(waveform=WaveformEnum.PULSE,volume=1.0,width=pulse_width) )
            sine = params[f"osc_sine{i_vco}on"]["raw_value"]
            if sine == 1.0:
                shapes.append( OscillatorShape(waveform=WaveformEnum.SINE,volume=1.0) )
        return shapes
    
    def _get_osc_shapes_digital(self,params:dict,i_vco:int) -> List[OscillatorShape]:
        shapes = []
        osc_shape = params[f"osc_digitaltype{i}"]["value"]
        osc_shape = int(osc_shape)
        if osc_shape == 1:
            shapes = [ OscillatorShape(waveform=WaveformEnum.SAWMULTI,volume=1.0) ]
        elif osc_shape == 2:
            shapes = [ OscillatorShape(waveform=WaveformEnum.TRISHAPED,volume=1.0) ]
        elif osc_shape == 3:
            shapes = [ OscillatorShape(waveform=WaveformEnum.NOISE,volume=1.0) ]
        elif osc_shape == 4:
            shapes = [ OscillatorShape(waveform=WaveformEnum.FEEDBACK,volume=1.0) ]
        elif osc_shape == 5:
            shapes = [ OscillatorShape(waveform=WaveformEnum.PULSE,volume=1.0) ]
        elif osc_shape == 6:
            shapes = [ OscillatorShape(waveform=WaveformEnum.SAWTOOTH,volume=1.0) ]
        elif osc_shape == 7:
            shapes = [ OscillatorShape(waveform=WaveformEnum.TRIANGLE,volume=1.0) ]

        return shapes    
    
    def _get_osc_volume(self,params:dict,i_vco:int) -> float:
        return params[f"osc_volume{i_vco}"]["raw_value"]
        
    def _get_osc_tune_coarse(self,params:dict,i_vco:int) -> float:
        tune = float(params[f"osc_tune{i_vco}"]["value"])
        tune_coarse = round(tune / 12) * 12.0 
        return int(tune_coarse)

    def _get_osc_tune_fine(self,params:dict,i_vco:int) -> float:
        tune = float(params[f"osc_tune{i_vco}"]["value"])
        tune_coarse = round(tune / 12) * 12.0 
        sign = 1 if tune_coarse - tune >= 0 else -1
        return (tune - tune_coarse)*sign

    def _get_osc_volume_simple(self,params,i_vco:int) -> float:
        mix = params['osc_oscmix']['raw_value']
        if i_vco==1:
            return 1.0 - mix
        elif i_vco ==2:
            return mix 
        
    def _get_osc_pwm_width(self,params:dict) -> WaveformWidthEnum:
        pulsedwith = params[f"osc_pulsewidth"]["raw_value"]
        if pulsedwith < .10:
            return WaveformWidthEnum.NARROW
        elif pulsedwith < .40:
            return WaveformWidthEnum.THIN
        elif pulsedwith < .60:
            return WaveformWidthEnum.NORMAL
        elif pulsedwith < .90:
            return WaveformWidthEnum.WIDE
        elif pulsedwith < 1.0:
            return WaveformWidthEnum.VERY_WIDE
        elif pulsedwith == 1.0:
            return WaveformWidthEnum.SILENCE
        return None
    

############################################################################################################
#
# OSCs MOD section
#
############################################################################################################        
    
    # for now, this wont link the objects
    def _add_oscs_mod_triple(self,params:dict,mod_matrix:ModulationMatrix) -> NoReturn:

        # ORDER IS IMPORTANT ! The first mod may be composited with the oscillator declaration
        
        # check Sync
        self._check_oscs_sync(params,[2,3],mod_matrix)              

        # check FM mod
        self._check_oscs_fm(params,[2,3],mod_matrix)

        # check classic MOD routings
        self._check_oscs_mod_triple(params,mod_matrix)

    
    def _add_oscs_mod_dual(self,params:dict,mod_matrix:ModulationMatrix)-> NoReturn:

        # ORDER IS IMPORTANT ! The first mod may be composited with the oscillator declaration
        
        # check pwm mod
        pwm_select = params[f"osc_pwm2on"]["raw_value"]
        pulse1 = params[f"osc_pwm1on"]["raw_value"]
        pulse2 = params[f"osc_pulse2on"]["raw_value"]
        oscs_is = []
        if (pwm_select == 0.0 or pwm_select == 1.0) and pulse1==1.0:
            oscs_is.append(1)
        if pwm_select == 1.0 and pulse2==1.0:
            oscs_is.append(2)
        self._check_oscs_pwm(params,oscs_is,mod_matrix)

        # check sync mod
        self._check_oscs_sync(params,[2],mod_matrix)

        # check FM / CrossMod
        self._check_oscs_fm(params,[2],mod_matrix,save_as=ModulationDestParam.CROSS_MOD)

        # check FM / CrossMod modulation
        self._check_oscs_fm_mod(params,[2],mod_matrix,save_as=ModulationDestParam.CROSS_MOD_AMOUNT)

        # check main modulation
        self._check_oscs_dual_mod(params,mod_matrix)

    
    def _add_oscs_mod_dco(self,params:dict,mod_matrix:ModulationMatrix)-> NoReturn:
        pass
        #CURRENTLY WORKING on PWMMODDEPTH    

    def _add_oscs_mod_eco(self,params:dict,mod_matrix:ModulationMatrix)-> NoReturn:
        pass   

    def _add_oscs_mod_digital(self,params:dict,mod_matrix:ModulationMatrix)-> NoReturn:
        pass   

    def _check_oscs_mod_triple(self,params:dict,mod_matrix:ModulationMatrix)->NoReturn:
        for i in range(3):
            vco_i = i+1
            mod_tune = params[f"osc_tunemodosc{vco_i}"]["value"]
            mod_level = params[f"osc_tune1moddepth"]["raw_value"]
            if mod_tune == "1" and mod_level>0.0:
                source_id = self._identify_mod_source_id(params,"osc_tune1modsrc")
                if source_id is not None:
                    modulation = Modulation(
                                            source_id=source_id,
                                            dest_id=ModulationDestID[f"OSC{vco_i}"],
                                            dest_param=ModulationDestParam.PITCH,
                                            depth=mod_level
                                            )
                    mod_matrix.add_modulation(modulation)
            mod_shape = params[f"osc_shapemodosc{vco_i}"]["value"]
            mod_level = params[f"osc_shapedepth"]["raw_value"]
            if mod_shape == "1" and mod_level>0.0:
                source_id = self._identify_mod_source_id(params,"osc_tune1modsrc")
                if source_id is not None:
                    modulation = Modulation(
                                            source_id=source_id,
                                            dest_id=ModulationDestID[f"OSC{vco_i}"],
                                            dest_param=ModulationDestParam.SHAPE,
                                            depth=mod_level
                                            )
                    mod_matrix.add_modulation(modulation)              

    def _check_oscs_pwm(self,params:dict,vco_is:list,mod_matrix:ModulationMatrix)->NoReturn:
        for i_vco in vco_is:
            moddepth = float(params[f"osc_pwmoddepth"]["value"])
            source_id = self._identify_mod_source_id(params,"osc_pwmodsrc")
            if moddepth != 0.0 and source_id is not None:
                modulation = Modulation(
                    source_id=source_id,
                    dest_id=ModulationDestID[f"OSC{i_vco}"],
                    dest_param=ModulationDestParam.PWM,
                    depth=moddepth
                )
                mod_matrix.add_modulation(modulation)

    def _check_oscs_sync(self,params:dict,vco_is:list,mod_matrix:ModulationMatrix)-> NoReturn:
        # check SYNC
        for vco_i in vco_is:
            mod_sync = params[f"osc_sync{vco_i}"]["value"]
            if mod_sync == "1":
                modulation = Modulation(
                                        source_id=ModulationSourceID.OSC1,
                                        dest_id=ModulationDestID[f"OSC{vco_i}"],
                                        dest_param=ModulationDestParam.SYNC_HARD,
                                        depth=1.0
                                        )
                mod_matrix.add_modulation(modulation)    

    def _check_oscs_fm(self,params:dict,vco_is:list,mod_matrix:ModulationMatrix,save_as:ModulationDestParam=ModulationDestParam.FM)->NoReturn:
        mod_fm = float(params[f"osc_fm"]["value"])
        # lets not use a threshold, FM is very sensitive
        if mod_fm > 0.0:
            for vco_i in vco_is:
                modulation = Modulation(
                                        source_id=ModulationSourceID.OSC1,
                                        dest_id=ModulationDestID[f"OSC{vco_i}"],
                                        dest_param=save_as,
                                        depth=mod_fm
                                        )
                mod_matrix.add_modulation(modulation)   

    def _check_oscs_fm_mod(self,params:dict,vco_is:list,mod_matrix:ModulationMatrix,save_as:ModulationDestParam=ModulationDestParam.FM_AMOUNT)->NoReturn:
        mod_fm = float(params[f"osc_fmmoddepth"]["value"])
        fm_mod_src_id = self._identify_mod_source_id(params,"osc_fmmodsrc")
        # lets not use a threshold, FM is very sensitive
        if mod_fm > 0.0 and fm_mod_src_id is not None:
            for vco_i in vco_is:
                modulation = Modulation(
                                        source_id=fm_mod_src_id,
                                        dest_id=ModulationDestID[f"OSC{vco_i}"],
                                        dest_param=save_as,
                                        depth=mod_fm
                                        )
                mod_matrix.add_modulation(modulation)                         

    def _check_oscs_dual_mod(self,params:dict,mod_matrix:ModulationMatrix) -> NoReturn:
        # TuneModMod: 0 = 1, 1 = both , 2 = 2 , 3 = split
        tunemod_mode = params["osc_tunemodmode"]["value"]
        sources = {
            1 : self._identify_mod_source_id(params,"osc_tune1modsrc") ,
            2 : self._identify_mod_source_id(params,"osc_tune2modsrc")
        }
        depths = {
            1 : float(params["osc_tune1moddepth"]["value"]) ,
            2 : float(params["osc_tune2moddepth"]["value"])
        }
        mod_map = dict()
        match tunemod_mode:
            case "0":
                mod_map[1] = [1]
                mod_map[2] = [1]
            case "1":
                mod_map[1] = [1,2]
                mod_map[2] = [1,2]
            case "2":
                mod_map[1] = [2]
                mod_map[2] = [2]
            case "3":
                mod_map[1] = [1]
                mod_map[2] = [2]
        
        for src_i,dest_js in mod_map.items():
            for dest_j in dest_js:
                source_id = sources[src_i]
                depth = depths[src_i]
                if source_id is None or depth==0.0:
                    continue
                modulation = Modulation(
                                source_id=source_id,
                                dest_id=ModulationDestID[f"OSC{dest_j}"],
                                dest_param=ModulationDestParam.PITCH,
                                depth=depth
                            )
                mod_matrix.add_modulation(modulation)

    def _identify_mod_source_id(self,params:dict,param_name:str) -> ModulationSourceID:
        mod_source = params[param_name]["value"]
        mod_sources_dict = {
            '0' : None ,
            '6' : ModulationSourceID.VELOCITY ,
            '7' : ModulationSourceID.AFTERTOUCH ,
            '8' : ModulationSourceID.KEYBOARD ,
            '9' : ModulationSourceID.KEYBOARD ,
            '14' : ModulationSourceID.ENV1 ,
            '15' : ModulationSourceID.ENV2 ,
            '16' : ModulationSourceID.LFO1 ,
            '17' : ModulationSourceID.LFO2 
        }

        mod_source_id = mod_sources_dict.get(mod_source,ModulationSourceID.OTHER)

        return mod_source_id 
    
############################################################################################################
#
# Filters section
#
############################################################################################################        

    def _get_filters(self,params:dict,mod_matrix:ModulationMatrix):

        filters = []

        model_hpf = params['hpf_model']['value']

        return filters 
