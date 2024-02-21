import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert
from sounds.models import SoundSource

def get_envelope(source:SoundSource,audio):
    t = np.arange( audio.shape[1] ) / source.audio_device_samplerate
    analytic_signal = hilbert(audio[0])
    amplitude_envelope = np.abs(analytic_signal)
    return amplitude_envelope
    # fig, (ax0) = plt.subplots(nrows=1)
    # ax0.plot(t, audio[0], label='signal')
    # ax0.plot(t, amplitude_envelope, label='envelope')
    # ax0.set_xlabel("time in seconds")
    # ax0.legend()    
    # fig.tight_layout()