from sounddevice import query_devices
from pedalboard import load_plugin
from mido import Message 
from ..models import SoundSource
import io
import numpy as np
import wave
from enum import StrEnum , auto
from sounds.apps import SoundsConfig
from pedalboard.io import AudioFile

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


def render_audio(source:SoundSource,
           bank_msb:int|None=None,
           bank_lsb:int|None=None,
           program:int|None=None,
           length:int|None=None):
  
  if length is None:
    length = 60 # 4 seconds

  # Render some audio by passing MIDI to an instrument:
  sample_rate = source.audio_device_samplerate
  
  if source.type == SoundSource.Type.INSTRUMENT:

    instrument_info = None

    print(SoundsConfig.PLUGINS_CACHE)

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
            "rendering":True
        }
        SoundsConfig.PLUGINS_CACHE[source.file_path].append(instrument_info)
        print("Loaded instrument")

    instrument = instrument_info['instrument']

    #print(instrument.parameters.keys())
        
    # this is also the opportunity to change the program here with minimal data
    # Bank Select MSB
    pgm_events = []
    pgm_events.append( Message('control_change', control=0, value=bank_msb,time=0) )
    if bank_lsb is not None:
       pgm_events.append(Message('control_change', control=32, value=bank_lsb,time=0.05))
    pgm_events.append(Message('program_change', program=program,time=0.1) )
        
    # necessary to avoid locks on future rendering?
    # this doesnt resolve the issue when runserver reloads because of source changes
    # but this helps with the lock that was happening on the 3rd play ...
    # also the opportunity to change the program here ...
    instrument([*pgm_events,],duration=0.5,sample_rate=sample_rate)

    print("Loaded Preset")

    # instrument([msg_bmsb,msg_blsb,msg_pgm],duration=0.4,sample_rate=sample_rate)
    audio = instrument(
      [ 
         Message("note_on", note=60,time=0), Message("note_off", note=60, time=length)],
      duration=length, # seconds
      sample_rate=sample_rate,
    )

    # audio = instrument(
    #   [Message("note_on", note=60), Message("note_off", note=60, time=length)],
    #   duration=length, # seconds
    #   sample_rate=sample_rate,
    # )

    print("Rendered")

    instrument_info['rendering'] = False

    return audio
  
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
   