import subprocess
import requests
import time
import os

OLLAMA_PATH = r"C:\Users\mahimaratnari\AppData\Local\Programs\Ollama\ollama.exe"

def ensure_ollama():

    try:
        requests.get(
            "http://127.0.0.1:11434",
            timeout=2
        )

        print("✅ Ollama already running")
        return

    except:
        print("⚡ Starting Ollama...")

    if os.path.exists(OLLAMA_PATH):

        subprocess.Popen(
            [OLLAMA_PATH, "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        time.sleep(5)

        print("✅ Ollama started")

    else:

        print("❌ Ollama not found")