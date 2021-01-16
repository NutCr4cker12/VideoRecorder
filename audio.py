import pyaudio
import wave

chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 2
fs = 44100  # Record at 44100 samples per second
seconds = 10
filename = "output.wav"
device_index = 1

def play():
    wf = wave.open(filename)
    p = pyaudio.PyAudio()

    stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(),
                    rate = wf.getframerate(),
                    output=True)
    data = wf.readframes(chunk)

    while data != b'':
        stream.write(data)
        data = wf.readframes(chunk)

    stream.close()
    p.terminate()

def record():
    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print('Recording')
    device = p.get_device_info_by_index(device_index)
    # print(channels)
    is_input = device["maxInputChannels"] > 0
    channels = device["maxInputChannels"] if is_input else device["maxOutputChannels"]

    try:
        if is_input:
            stream = p.open(format=sample_format,
                            channels=channels,
                            rate=int(device["defaultSampleRate"]),
                            frames_per_buffer=chunk,
                            input=True,
                            input_device_index=device_index,
                            as_loopback = True)
        else:
            stream = p.open(format=sample_format,
                            channels=channels,
                            rate=int(device["defaultSampleRate"]),
                            frames_per_buffer=chunk,
                            output=True,
                            output_device_index=device_index,
                            as_loopback = True)
    except OSError:
        # if stream.is_active():
        #     stream.close()
        return
    frames = []  # Initialize array to store frames

    # Store data in chunks for 3 seconds
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream 
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    print('Finished recording')

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

# record()
# play()
p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    print(info)
    name = info["name"]
    if "WASAPI" in name:
        print("WASAPI FOUND IN ", i)
    else:
        print("---")