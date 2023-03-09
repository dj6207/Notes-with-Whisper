import whisper
import pyaudio
import datetime
import os
import keyboard
import wave

WHISPER = whisper.load_model("small.en")
AUDIO = pyaudio.PyAudio()
CHUNK =  1024
AUDIO_FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
STREAM = AUDIO.open(format=AUDIO_FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
DATA = []
TRANSCRIPTION_PATH = "./transcription/"
AUDIO_PATH = "./audio/"
AUDIO_FILE_EXTENSION = ".wav"

def transcribe_audio():
    key = input("Type file path to transcribe or press r to record audio:")
    if (key == "r"):
        print("Press esc to stop recording")
        while True:
            record_audio(DATA, STREAM, CHUNK)
            if (keyboard.is_pressed("esc")):
                print("Recording stopped")
                break
        print("Generating audio file")
        audio_file = generate_audio_file(DATA)
    else:
        audio_file = key
    print("Generating transcript")
    transcription = generate_transcript(WHISPER, audio_file)
    print("Generating txt file")
    generate_txt(transcription, TRANSCRIPTION_PATH, audio_file)

def make_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

def record_audio(data, stream, chunk):
    data.append(stream.read(chunk))

def generate_audio_file(data):
    file_name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + AUDIO_FILE_EXTENSION
    wf = wave.open(AUDIO_PATH + file_name, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(2)
    wf.setframerate(RATE)
    wf.writeframes(b''.join(data))
    wf.close()
    return file_name

def generate_transcript(model, file):
    return model.transcribe(AUDIO_PATH + file)

def generate_txt(transcript, folder, file):
    today = datetime.datetime.today()
    report = f"REPORT\nFile name: {file}\nDate: {today}" \
         f"\nFile stored at: {os.path.join(folder, file)}.txt\n"
    report += transcript["text"]
    filepath = os.path.join(folder, file)
    text = open(filepath + ".txt","w")
    text.write(report)
    text.close()

if __name__ == "__main__":
    make_folder(TRANSCRIPTION_PATH)
    make_folder(AUDIO_PATH)
    transcribe_audio()