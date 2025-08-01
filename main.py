import os
import eel
import subprocess

from engine.features import *
from engine.command import *
from engine.auth import recoganize
from engine.auth.sample import capture_face_images
from engine.auth.trainer import train_classifier

def start():
    eel.init("www")

    playAssistantSound()

    @eel.expose
    def init():
        subprocess.call([r'device.bat'])
        eel.hideLoader()
        speak("Ready for Face Authentication")
        flag = recoganize.AuthenticateFace()
        if flag == 1:
            eel.hideFaceAuth()
            speak("Face Authentication Successful")
            eel.hideFaceAuthSuccess()
            speak(f"Hello, Welcome sir, How can I help you?")
            eel.hideStart()
            playAssistantSound()
        else:
            speak("Face Authentication Failed")

    @eel.expose
    def capture_face_for_training(name):
        try:
            names_path = "engine/auth/trainer/names.txt"
            if not os.path.exists(names_path):
                with open(names_path, "w"): pass

            with open(names_path, "r") as f:
                existing_names = [line.strip() for line in f.readlines()]

            if name in existing_names:
                face_id = existing_names.index(name) + 1
            else:
                existing_names.append(name)
                face_id = len(existing_names)
                with open(names_path, "w") as f:
                    f.write("\n".join(existing_names))

            capture_face_images(face_id)
            train_classifier()
            return f"Face registered for {name} with ID {face_id}."

        except Exception as e:
            return f"Error: {str(e)}"

    os.system('start msedge.exe --app="http://localhost:8000/index.html"')
    eel.start('index.html', mode=None, host='localhost', block=True)
