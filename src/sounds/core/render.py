from pedalboard import load_plugin
from mido import Message 

# Load a VST3 or Audio Unit plugin from a known path on disk:
instrument = load_plugin("/Library/Audio/Plug-Ins/VST3/SynthMaster2.vst3")

print(instrument.parameters.keys())

# Render some audio by passing MIDI to an instrument:
sample_rate = 44100
audio = instrument(
  [Message("note_on", note=60), Message("note_off", note=60, time=5)],
  duration=5, # seconds
  sample_rate=sample_rate,
)

#Content-Type: audio/pcm;rate=48000;encoding=float;bits=32
