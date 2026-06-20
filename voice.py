import pyttsx3

def speak(text, voice="Female"):

    try:

        print("SPEAK STARTED")

        engine = pyttsx3.init()

        voices = engine.getProperty("voices")

        if voice == "Male":
            engine.setProperty(
                "voice",
                voices[0].id
            )

        else:
            engine.setProperty(
                "voice",
                voices[1].id
            )

        print("SAYING =", text)

        engine.say(text)
        engine.runAndWait()

        print("SPEAK FINISHED")

    except Exception as e:

        print("VOICE ERROR =", e)