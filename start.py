import json
import pyaudio
from vosk import Model, KaldiRecognizer, SetLogLevel
import sys
import subprocess
import requests
import time
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
 
owm = OWM('f4f0bf47c7b91c42e07ddaf82d81a48b')
mgr = owm.weather_manager()

SetLogLevel(-1)
model = Model("/home/demon/Jarviz/voice_cc") # полный путь к модели
rec = KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paInt16, channels=1,
                rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()


def listen():
    while True:
        data = stream.read(4000, exception_on_overflow=False)

        if rec.AcceptWaveform(data) and len(data) > 0:
            answer = json.loads(rec.Result())
            if answer["text"]:
                yield answer["text"]

for text in listen():
    if "джарвис привет" in text:
        subprocess.run("echo Приветствую вас, мой господин! | RHVoice-test -p Aleksandr", shell=True)
    elif text == "джарвис музыка":
        subprocess.run("echo Приложение Яндекс.Музыка запущенно! | RHVoice-test -p Aleksandr", shell=True)
        subprocess.run("ymp")
    elif text == "джарвис погода":
        observation = mgr.weather_at_place('Orenburg,RU')
        w = observation.weather
        
        p = w.temperature('celsius')
        print(p)
        subprocess.run("echo В Александровке 20 градусов | RHVoice-test -p Aleksandr", shell=True)

    elif text == "джарвис спать":
        sys.exit()
    else:
        print(text)