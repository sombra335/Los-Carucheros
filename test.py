import sounddevice as sd
import numpy as np

# Audio parameters
samplerate = 44100  # CD quality
blocksize = 1024    # Small block size for low latency

def callback(indata, outdata, frames, time, status):
    if status:
        print(status)
    # Invert the waveform
    outdata[:] = -indata

# Start real-time audio stream
with sd.Stream(callback=callback, samplerate=samplerate, blocksize=blocksize, channels=1):
    print("Running... Press Ctrl+C to stop.")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Stopped.")
