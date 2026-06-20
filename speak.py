import pyttsx3

engine = pyttsx3.init()

def speak(text, voice_type):

    if voice_type == "Off":
        return

    voices = engine.getProperty("voices")

    if voice_type == "Male":
        engine.setProperty(
            "voice",
            voices[0].id
        )

    else:
        engine.setProperty(
            "voice",
            voices[1].id
        )

    engine.say(text)
    engine.runAndWait()