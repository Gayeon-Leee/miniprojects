# pip install pyttsx3
import pyttsx3

tts = pyttsx3.init()
voice = tts.getProperty('voices')
tts.setProperty('voice', voice[17].id)
tts.say('안녕하세요')
tts.runAndWait()