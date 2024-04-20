import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 150)
text = "haw haw de karabaw haw haw de karabaw haw haw de karabaw haw haw de karabaw"
engine.say(text)
engine.runAndWait()