import subprocess
import time
from typing import Dict, List, Optional

class ADBPhoneController:
    def __init__(self, device_id: Optional[str] = None):
        self.device_id = device_id
        self.device_cmd = f"-s {device_id}" if device_id else ""

        self.app_packages = {
            'camera': 'com.android.camera',
            'gallery': 'com.google.android.apps.photos',
            'phone': 'com.google.android.dialer',
            'messages': 'com.google.android.apps.messaging',
            'contacts': 'com.google.android.contacts',
            'calculator': 'com.google.android.calculator',
            'clock': 'com.google.android.deskclock',
            'calendar': 'com.google.android.calendar',
            'maps': 'com.google.android.apps.maps',
            'youtube': 'com.google.android.youtube',
            'gmail': 'com.google.android.gm',
            'chrome': 'com.android.chrome',
            'play_store': 'com.android.vending',
            'settings': 'com.android.settings',
            'whatsapp': 'com.whatsapp',
            'instagram': 'com.instagram.android',
            'facebook': 'com.facebook.katana',
            'twitter': 'com.twitter.android',
            'spotify': 'com.spotify.music',
            'netflix': 'com.netflix.mediaclient'
        }

    def run_adb_command(self, command: str) -> str:
        try:
            full_command = f"adb {self.device_cmd} {command}"
            print(f"Running ADB Command: {full_command}")
            result = subprocess.run(full_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            if result.returncode == 0:
                print(f"ADB Output: {result.stdout.strip()}")
                return result.stdout.strip()
            else:
                print(f"ADB Error: {result.stderr.strip()}")
                return ""
        except Exception as e:
            print(f"Command execution error: {e}")
            return ""

    def check_adb_connection(self) -> bool:
        result = self.run_adb_command("devices")
        if "device" in result and "offline" not in result:
            print("✓ ADB connected successfully")
            return True
        else:
            print("✗ No device connected or ADB not working")
            return False

    def open_app(self, app_name: str) -> bool:
        if app_name.lower() in self.app_packages:
            package_name = self.app_packages[app_name.lower()]
        else:
            package_name = app_name

        print(f"Trying to open app: {package_name}")
        command = f"shell monkey -p {package_name} -c android.intent.category.LAUNCHER 1"
        result = self.run_adb_command(command)

        if "Events injected" in result:
            print(f"✓ Successfully opened {app_name}")
            return True
        else:
            print(f"✗ Failed to open {app_name} via monkey")
            return False

    def close_app(self, app_name: str) -> bool:
        if app_name.lower() in self.app_packages:
            package_name = self.app_packages[app_name.lower()]
        else:
            package_name = app_name

        print(f"Closing {app_name}...")
        result = self.run_adb_command(f"shell am force-stop {package_name}")
        print(f"✓ {app_name} closed")
        return True

    def open_camera(self) -> bool:
        print("Opening camera...")
        result = self.run_adb_command("shell am start -a android.media.action.IMAGE_CAPTURE")
        if "Starting" in result:
            print("✓ Camera opened successfully")
            return True
        print("✗ Failed to open camera")
        return False

    def take_photo(self) -> bool:
        print("Taking photo...")
        self.run_adb_command("shell input keyevent KEYCODE_CAMERA")
        print("✓ Photo capture attempted")
        return True

    def start_video_recording(self) -> bool:
        print("Starting video recording...")
        self.open_camera()
        time.sleep(2)
        self.run_adb_command("shell input tap 540 1800")  # Tap record button
        print("✓ Video recording started")
        return True

    def stop_video_recording(self) -> bool:
        print("Stopping video recording...")
        self.run_adb_command("shell input tap 540 1800")  # Tap stop button
        print("✓ Video recording stopped")
        return True

    def unlock_phone(self, pin: Optional[str] = None) -> bool:
        print("Unlocking phone...")
        self.run_adb_command("shell input keyevent KEYCODE_WAKEUP")
        time.sleep(1)
        self.run_adb_command("shell input swipe 540 1800 540 800")
        time.sleep(1)
        if pin:
            for digit in pin:
                self.run_adb_command(f"shell input text {digit}")
                time.sleep(0.2)
            self.run_adb_command("shell input keyevent KEYCODE_ENTER")
        print("✓ Phone unlock attempted")
        return True

    def go_home(self) -> bool:
        self.run_adb_command("shell input keyevent KEYCODE_HOME")
        print("✓ Returned to home screen")
        return True

    def go_back(self) -> bool:
        self.run_adb_command("shell input keyevent KEYCODE_BACK")
        print("✓ Went back")
        return True

    def open_recent_apps(self) -> bool:
        self.run_adb_command("shell input keyevent KEYCODE_APP_SWITCH")
        print("✓ Opened recent apps")
        return True

    def get_device_info(self) -> Dict[str, str]:
        info = {}
        commands = {
            'model': 'shell getprop ro.product.model',
            'brand': 'shell getprop ro.product.brand',
            'version': 'shell getprop ro.build.version.release',
            'sdk': 'shell getprop ro.build.version.sdk',
            'battery': 'shell dumpsys battery | grep level'
        }
        for key, cmd in commands.items():
            info[key] = self.run_adb_command(cmd)
        return info
