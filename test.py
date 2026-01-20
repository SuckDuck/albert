import numpy as np
import simpleaudio as sa

def beep(freq=500, duration=0.08, volume=0.3, fs=44100):
    t = np.linspace(0, duration, int(fs*duration), False)
    wave = np.sin(freq * t * 2*np.pi)
    audio = (wave * (2**15 - 1) * volume).astype(np.int16)
    sa.play_buffer(audio, 1, 2, fs)

beep()