from sounddevice import query_devices
from pedalboard import load_plugin
from mido import Message 
from ..models import SoundGenerator
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
        (AudioInterface.INTERNAL_CAPTURE,AudioInterface.INTERNAL_CAPTURE)
    ])
    for device in devices:
        # this is an input
        if device['max_input_channels']>0:
            result.append(
                (device['name'],device['name'])
            )
    return result 


def render_audio(generator:SoundGenerator,
           bank:int|None=None,
           program:int|None=None,
           length:int|None=None):
  
  if length is None:
    length = 7 # 4 seconds

  # Render some audio by passing MIDI to an instrument:
  sample_rate = generator.audio_device_samplerate
  
  if generator.type == SoundGenerator.Type.INSTRUMENT:

    if SoundsConfig.PLUGINS_CACHE.get(generator.name):
       instrument = SoundsConfig.PLUGINS_CACHE.get(generator.name)
       print("Got instrument from cache")
    else:
        # Load a VST3 or Audio Unit plugin from a known path on disk:
        instrument = load_plugin(generator.file_path)
        SoundsConfig.PLUGINS_CACHE[generator.name] = instrument

    #print(instrument.parameters.keys())

    audio = instrument(
      [Message("note_on", note=60), Message("note_off", note=60, time=length)],
      duration=length, # seconds
      sample_rate=sample_rate,
    )

    return audio
  
def convert_to_16bits(audio):
    scaled_array = 32768 * audio
    return scaled_array.astype(np.int16,order='C')

def convert_to_wav(audio,framerate,convertto16bits=True):
    bIO = io.BytesIO()
    if convertto16bits:
       audio = convert_to_16bits(audio)
    C , N = audio.shape
    audio_interleaved = np.ndarray(shape=(N,C),dtype=audio.dtype)
    for c in range(C):
       for s in range(N):
          audio_interleaved[s][c] = audio[c][s]
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
   