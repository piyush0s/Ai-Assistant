# engine/mobile_commands.py

from engine.mobile import ADBPhoneController
from command import speak

controller = ADBPhoneController()

def handle_mobile_command(query: str):
    if "open camera" in query:
        controller.open_camera()
        speak("Camera opened on mobile.")

    elif "take photo" in query:
        controller.take_photo()
        speak("Photo captured on mobile.")

    elif "start video recording" in query:
        controller.start_video_recording()
        speak("Started video recording on mobile.")

    elif "stop video recording" in query:
        controller.stop_video_recording()
        speak("Stopped video recording on mobile.")

    elif "unlock phone" in query:
        controller.unlock_phone()
        speak("Phone unlock attempted.")

    elif "go home" in query:
        controller.go_home()
        speak("Returned to home screen.")

    elif "go back" in query:
        controller.go_back()
        speak("Went back on mobile.")

    elif "recent apps" in query:
        controller.open_recent_apps()
        speak("Opened recent apps on phone.")

    elif "open" in query:
        app = query.split("open")[-1].strip()
        app = app.replace("on mobile", "").replace("in mobile", "").replace("phone", "").strip()
        controller.open_app(app)
        speak(f"{app} opened on mobile.")

    elif "close" in query:
        app = query.split("close")[-1].strip()
        app = app.replace("on mobile", "").replace("in mobile", "").replace("phone", "").strip()
        controller.close_app(app)
        speak(f"{app} closed on mobile.")

    elif "device info" in query or "phone info" in query:
        info = controller.get_device_info()
        for key, value in info.items():
            speak(f"{key}: {value}")

    else:
        speak("Sorry, I didn't understand the mobile command.")
