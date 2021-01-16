import sounddevice as sd
import soundfile as sf
from scipy.io.wavfile import write

filename = "output.wav"
fs = 44100  # Sample rate
seconds = 10  # Duration of recording

def play():
    data, fs = sf.read(filename, dtype="float32")
    sd.play(data, fs)
    status = sd.wait()

def record():
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()  # Wait until recording is finished
    write(filename, fs, myrecording)  # Save as WAV file 

record()
play()