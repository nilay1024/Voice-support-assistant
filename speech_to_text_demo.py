import speech_recognition as sr 
from googletrans import Translator

translator = Translator()
  
AUDIO_FILE = ("example1.wav") 
  
# use the audio file as the audio source 
  
r = sr.Recognizer() 
  
with sr.AudioFile(AUDIO_FILE) as source: 
    #reads the audio file. Here we use record instead of 
    #listen 
    audio = r.record(source)   
  
try: 
    text = r.recognize_google(audio, language="hi-IN")
    # print("The audio file contains: " + text))
    print(text)
    print(translator.translate(text))
  
except sr.UnknownValueError: 
    print("Google Speech Recognition could not understand audio") 
  
except sr.RequestError as e: 
    print("Could not request results from Google Speech  Recognition service; {0}".format(e))
