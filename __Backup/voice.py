import pyttsx3
import threading

def _speak(text):

    try:

        engine = pyttsx3.init()

        engine.say(text)

        engine.runAndWait()

        engine.stop()

    except Exception as e:

        print("VOICE ERROR =", e)

def speak(text):

    threading.Thread(
        target=_speak,
        args=(text,),
        daemon=True
    ).start()