from sounddevice import query_devices
from pedalboard import load_plugin
from mido import Message 
from ..models import SoundSource
import io
import numpy as np
import wave
import math
import re
from enum import StrEnum , auto
from sounds.apps import SoundsConfig
from pedalboard.io import AudioFile
from pedalboard._pedalboard import get_text_for_raw_value
from .midi import get_midi_pattern , get_midi_program_key, MIDIPattern
from .signal import get_envelope
from importlib import import_module
import inspect
from .extensions.instruments.base import InstrumentExtension
from PIL import Image

class AudioInterface(StrEnum):
    NONE = "---------"
    INTERNAL_CAPTURE = "Internal Capture"

def get_audio_input_interfaces():
    devices = query_devices()
    result = list()
    result.extend([
        (None,AudioInterface.NONE),
        (AudioInterface.INTERNAL_CAPTURE.lower(),AudioInterface.INTERNAL_CAPTURE)
    ])
    for device in devices:
        # this is an input
        if device['max_input_channels']>0:
            result.append(
                (device['name'],device['name'])
            )
    return result 


def get_intrument_info(source:SoundSource):
    instrument_info = None
    if SoundsConfig.PLUGINS_CACHE.get(source.file_path):
        for instr_info in SoundsConfig.PLUGINS_CACHE.get(source.file_path):
            if not instr_info['rendering']:
                instrument_info = instr_info
                print("Got instrument from cache")
                break
    if instrument_info is None:
        # Load a VST3 or Audio Unit plugin from a known path on disk:
        instrument = load_plugin(source.file_path)
        if not source.file_path in SoundsConfig.PLUGINS_CACHE:
            SoundsConfig.PLUGINS_CACHE[source.file_path] = []      
        instrument_info = {
            "instrument":instrument,
            "rendering":True,
            "programs_info":dict(),
            "extension":get_instrument_extension(source)
        }
        SoundsConfig.PLUGINS_CACHE[source.file_path].append(instrument_info)
        print("Loaded instrument")
    
    return instrument_info


def convert_parameters(instrument):
    result = dict()
    params = instrument.parameters
    for param_name,param in params.items():
        # cpp_parameter = param.__get_cpp_parameter()
        # x_text_value = get_text_for_raw_value(cpp_parameter,  param.raw_value, False)
        result[param.python_name] = {
            'label' : param.label ,
            'raw_value' : param.raw_value ,
            'value' : param.string_value ,
            'range' : param.range ,
            # 'text' : param.get_text_for_raw_value(param.raw_value)
        }
    return result 

def render_audio(source:SoundSource,
           bank_msb:int|None=None,
           bank_lsb:int|None=None,
           program:int|None=None,
           pattern:MIDIPattern|None=None,
           length:int|None=None,
           save_parameters=True):
  
  # Render some audio by passing MIDI to an instrument:
  sample_rate = source.audio_device_samplerate

  if source.type == SoundSource.Type.INSTRUMENT:

    instrument_info = None
    preset_offset = 2

    instrument_info = get_intrument_info(source)

    instrument = instrument_info['instrument']

    #print(instrument.parameters.keys())
        
    # this is also the opportunity to change the program here with minimal data
    # Bank Select MSB
    pgm_events = []
    pgm_events.append( Message('control_change', control=0, value=bank_msb,time=0) )
    if source.midi_bank_use_lsb:
       pgm_events.append(Message('control_change', control=32, value=bank_lsb,time=0.4))
    pgm_events.append(Message('program_change', program=program,time=0.8) )
        
    # necessary to avoid locks on future rendering?
    # this doesnt resolve the issue when runserver reloads because of source changes
    # but this helps with the lock that was happening on the 3rd play ...
    # also the opportunity to change the program here ...
    # NO NEED: this seems to be better now and this slows down a lot the rendering of Synthmaster ...
    # instrument([*pgm_events,],duration=0.5,sample_rate=sample_rate)
    #print("Loaded Preset")

    # instrument([msg_bmsb,msg_blsb,msg_pgm],duration=0.4,sample_rate=sample_rate)
    notes , length_p = get_midi_pattern(source=source,pattern=pattern,preset_offset=preset_offset)

    if length is None:
        length = length_p 

    audio = instrument(
      [ *pgm_events,
        *notes],
      duration=preset_offset+length+2, # preset_offset + length seconds + 2 seconds for release
      sample_rate=sample_rate,
    )

    # audio = instrument(
    #   [Message("note_on", note=60), Message("note_off", note=60, time=length)],
    #   duration=length, # seconds
    #   sample_rate=sample_rate,
    # )

    print("Rendered")

    instrument_info['rendering'] = False

    # crop audio
    audio_start = math.floor( sample_rate * preset_offset )
    audio = audio[:,audio_start:]

    if save_parameters:    
        sound_key = get_midi_program_key(bank_msb,bank_lsb,program)
        if sound_key in instrument_info['programs_info']:
            sound_info = instrument_info['programs_info'][sound_key]
            sound_info['parameters'] = convert_parameters(instrument)
        else:
            instrument_info['programs_info'][sound_key] = {
                'parameters' : convert_parameters(instrument) ,
            }

    return audio
  
def analyze_audio(source:SoundSource,audio,sound_info):
    if 'analysis' not in sound_info:
        sound_info['analysis'] = {}
    if 'envelope' not in sound_info['analysis']:
        env = get_envelope(source,audio)
        # do something with it ... determine 
        #@TODO
        print("\n\n\n\n\n\nIMPLEMENTATION NEEDED FOR analyze_audio\n\n\n\n\n\n\n\n")
  
def get_sound_analysis(source:SoundSource,
           bank_msb:int|None=None,
           bank_lsb:int|None=None,
           program:int|None=None):
    
    pattern = MIDIPattern.SUSTAINED_MIDDLE_C
    instrument_info = get_intrument_info(source)
    instrument = instrument_info['instrument']
    instrExtension : InstrumentExtension = instrument_info["extension"]

    sound_key = get_midi_program_key(bank_msb,bank_lsb,program)
    
    # that should always be here
    sound_info = instrument_info['programs_info'][sound_key]

    if 'analysis' not in sound_info:
        sound_info['analysis'] = dict()

    # perform the analysis based on the preset/tone
    instrExtension.analyze_sound(source,instrument,sound_info)

    # if we have missing information, lets move to an audio analysis
    if 'envs' not in sound_info['analysis']:

        arp_old_value = instrExtension.arp_off(instrument)

        audio_4_analysis = render_audio(source=source,
                            bank_msb=bank_msb,
                            bank_lsb=bank_lsb,
                            program=program,
                            pattern=pattern,
                            length=2,
                            save_parameters=False) # do not save the parameters as we altered the sound ! They shoul be already there from the rendering that occured before
        
        instrExtension.arp_set(instrument,arp_old_value)    
        analyze_audio(source,audio_4_analysis,sound_info)
    
    if instrExtension:
        sound_info['description_tech'] = instrExtension.generate_text(sound_info)
    else:
        sound_info['description_tech'] = None

    sound_info['program_name'] = instrument.current_program_name

    if source.parameters and 'midi' in source.parameters and 'program_name_ignore' in source.parameters['midi']:
         sound_info['program_name'] = re.sub(source.parameters['midi']['program_name_ignore'],'',sound_info['program_name'])

    return sound_info

def get_image_data(source:SoundSource,
           bank_msb:int|None=None,
           bank_lsb:int|None=None,
           program:int|None=None):
    
    instrument_info = get_intrument_info(source)
    instrument = instrument_info['instrument']

    try:
        image_data = instrument.capture()
        im = Image.fromarray(image_data)
        rgb_image = im.convert('RGB')
        rgb_image.save("your_file.jpeg")

        return image_data.tolist()
    except Exception as e:
        print(f"RENDERING ERROR:{str(e)}")

    return None
  
def convert_to_16bits(audio):
    scaled_array = 32768 * audio
    return scaled_array.astype(np.int16,order='C')

def convert_to_wav(audio,framerate,convertto16bits=True):
    bIO = io.BytesIO()
    if convertto16bits:
       audio = convert_to_16bits(audio)
    C , N = audio.shape
    audio_interleaved = np.ndarray(shape=(N*C),dtype=audio.dtype)
    audio_interleaved[0::2] = audio[0]
    audio_interleaved[1::2] = audio[1]
    with wave.open(bIO, mode='wb') as wObj:
        wObj.setnchannels(C)
        wObj.setnframes(N)
        wObj.setframerate(framerate)
        wObj.setsampwidth(audio.itemsize)
        wObj.writeframes(audio_interleaved)
    bIO.seek(0)
    # with AudioFile(bIO,"w", format='wav', samplerate=framerate, num_channels=C, bit_depth=8*audio.itemsize) as f:
    #    f.write(audio)
    return bIO
   

def get_instrument_extension(source:SoundSource):
    if not source.extension:
        return None
    try:
        module_name = f"sounds.core.extensions.{source.extension}"
        module = import_module(module_name)
        classes = []
        for _, member in inspect.getmembers(module):
            if inspect.isclass(member):
                # Check if the class is defined in this module
                if member.__module__ == module_name:
                    classes.append(member)

        # Handle the case where there's exactly one class
        if len(classes) == 1:
            return classes[0]()
        elif len(classes) > 1:
            print("SELECTING THE LAST CLASS OF THE MODULE")
            return classes[-1]()
        else:
            return None
    except ImportError:
        return None
    
