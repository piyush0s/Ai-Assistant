

import subprocess
import time
import json
import os
from typing import Dict, List, Optional

class ADBPhoneController:
    def __init__(self, device_id: Optional[str] = None):
        """
        Initialize ADB Phone Controller
        
        Args:
            device_id (str, optional): Specific device ID if multiple devices connected
        """
        self.device_id = device_id
        self.device_cmd = f"-s {device_id}" if device_id else ""
        
        # Common app package names - you can customize these
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
        """Execute ADB command and return output"""
        try:
            full_command = f"adb {self.device_cmd} {command}"
            result = subprocess.run(full_command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                print(f"ADB Error: {result.stderr}")
                return ""
        except Exception as e:
            print(f"Command execution error: {e}")
            return ""
    
    def check_adb_connection(self) -> bool:
        """Check if ADB is connected to device"""
        result = self.run_adb_command("devices")
        if "device" in result and "offline" not in result:
            print("✓ ADB connected successfully")
            return True
        else:
            print("✗ No device connected or ADB not working")
            return False
    
    def open_app(self, app_name: str) -> bool:
        """
        Open an app on the phone
        
        Args:
            app_name (str): App name from the predefined list or package name
        
        Returns:
            bool: True if successful, False otherwise
        """
        # Check if it's a predefined app name
        if app_name.lower() in self.app_packages:
            package_name = self.app_packages[app_name.lower()]
        else:
            # Assume it's already a package name
            package_name = app_name
        
        print(f"Opening {app_name}...")
        
        # Use monkey command to launch app
        command = f"shell monkey -p {package_name} -c android.intent.category.LAUNCHER 1"
        result = self.run_adb_command(command)
        
        if "Events injected" in result:
            print(f"✓ Successfully opened {app_name}")
            return True
        else:
            # Try alternative method using am start
            command = f"shell am start -n {package_name}/.MainActivity"
            result = self.run_adb_command(command)
            if "Starting" in result:
                print(f"✓ Successfully opened {app_name}")
                return True
            else:
                print(f"✗ Failed to open {app_name}")
                return False
    
    def open_camera(self) -> bool:
        """Open camera app with specific camera intents"""
        print("Opening camera...")
        
        # Try multiple methods to open camera
        methods = [
            "shell am start -a android.media.action.IMAGE_CAPTURE",
            "shell am start -a android.intent.action.CAMERA_BUTTON",
            f"shell monkey -p {self.app_packages['camera']} 1"
        ]
        
        for method in methods:
            result = self.run_adb_command(method)
            if "Starting" in result or "Events injected" in result:
                print("✓ Camera opened successfully")
                return True
        
        print("✗ Failed to open camera")
        return False
    
    def take_photo(self) -> bool:
        """Take a photo using camera"""
        print("Taking photo...")
        
        # Simulate camera shutter button press
        commands = [
            "shell input keyevent KEYCODE_CAMERA",  # Hardware camera button
            "shell input keyevent KEYCODE_VOLUME_DOWN",  # Volume down as shutter
            "shell input tap 540 1800"  # Tap center-bottom (typical shutter location)
        ]
        
        for command in commands:
            result = self.run_adb_command(command)
            time.sleep(1)
        
        print("✓ Photo capture attempted")
        return True
    
    def start_video_recording(self) -> bool:
        """Start video recording"""
        print("Starting video recording...")
        
        # Open camera first
        self.open_camera()
        time.sleep(2)
        
        # Switch to video mode and start recording
        commands = [
            "shell input swipe 540 960 540 1200",  # Swipe to video mode
            "shell input tap 540 1800",  # Tap record button
        ]
        
        for command in commands:
            self.run_adb_command(command)
            time.sleep(1)
        
        print("✓ Video recording started")
        return True
    
    def stop_video_recording(self) -> bool:
        """Stop video recording"""
        print("Stopping video recording...")
        self.run_adb_command("shell input tap 540 1800")  # Tap stop button
        print("✓ Video recording stopped")
        return True
    
    def get_installed_apps(self) -> List[str]:
        """Get list of all installed apps"""
        print("Getting installed apps...")
        result = self.run_adb_command("shell pm list packages")
        
        if result:
            packages = [line.replace("package:", "") for line in result.split("\n") if line.startswith("package:")]
            print(f"Found {len(packages)} installed apps")
            return packages
        return []
    
    def find_app_package(self, app_name: str) -> Optional[str]:
        """Find package name for an app by searching installed apps"""
        installed_apps = self.get_installed_apps()
        
        # Search for apps containing the name
        matches = [pkg for pkg in installed_apps if app_name.lower() in pkg.lower()]
        
        if matches:
            print(f"Found packages for '{app_name}': {matches}")
            return matches[0]  # Return first match
        else:
            print(f"No package found for '{app_name}'")
            return None
    
    def close_app(self, app_name: str) -> bool:
        """Close/force stop an app"""
        if app_name.lower() in self.app_packages:
            package_name = self.app_packages[app_name.lower()]
        else:
            package_name = app_name
        
        print(f"Closing {app_name}...")
        result = self.run_adb_command(f"shell am force-stop {package_name}")
        print(f"✓ {app_name} closed")
        return True
    
    def go_home(self) -> bool:
        """Go to home screen"""
        print("Going to home screen...")
        self.run_adb_command("shell input keyevent KEYCODE_HOME")
        print("✓ Returned to home screen")
        return True
    
    def go_back(self) -> bool:
        """Press back button"""
        print("Pressing back button...")
        self.run_adb_command("shell input keyevent KEYCODE_BACK")
        return True
    
    def open_recent_apps(self) -> bool:
        """Open recent apps screen"""
        print("Opening recent apps...")
        self.run_adb_command("shell input keyevent KEYCODE_APP_SWITCH")
        return True
    
    def unlock_phone(self, pin: Optional[str] = None) -> bool:
        """Unlock phone (wake up and optionally enter PIN)"""
        print("Unlocking phone...")
        
        # Wake up the screen
        self.run_adb_command("shell input keyevent KEYCODE_WAKEUP")
        time.sleep(1)
        
        # Swipe up to unlock (works for most lock screens)
        self.run_adb_command("shell input swipe 540 1800 540 800")
        time.sleep(1)
        
        # Enter PIN if provided
        if pin:
            for digit in pin:
                self.run_adb_command(f"shell input text {digit}")
                time.sleep(0.2)
            self.run_adb_command("shell input keyevent KEYCODE_ENTER")
        
        print("✓ Phone unlock attempted")
        return True
    
    def get_device_info(self) -> Dict[str, str]:
        """Get device information"""
        info = {}
        commands = {
            'model': 'shell getprop ro.product.model',
            'brand': 'shell getprop ro.product.brand',
            'version': 'shell getprop ro.build.version.release',
            'sdk': 'shell getprop ro.build.version.sdk',
            'battery': 'shell dumpsys battery | grep level'
        }
        
        for key, command in commands.items():
            result = self.run_adb_command(command)
            info[key] = result
        
        return info

# Voice command integration functions
def speak(message: str):
    """Text-to-speech function (placeholder - implement with your TTS system)"""
    print(f"Speaking: {message}")
    # Add your actual TTS implementation here

def open_phone_app(app_name: str, controller: ADBPhoneController):
    """Voice command function to open apps"""
    if controller.check_adb_connection():
        if controller.open_app(app_name):
            speak(f"Opening {app_name} on your phone")
        else:
            # Try to find the app package
            package = controller.find_app_package(app_name)
            if package:
                controller.open_app(package)
                speak(f"Opening {app_name} on your phone")
            else:
                speak(f"Could not find {app_name} on your phone")
    else:
        speak("Phone not connected via ADB")

def open_camera_command(controller: ADBPhoneController):
    """Voice command to open camera"""
    if controller.check_adb_connection():
        if controller.open_camera():
            speak("Camera opened on your phone")
        else:
            speak("Failed to open camera")
    else:
        speak("Phone not connected via ADB")

def take_photo_command(controller: ADBPhoneController):
    """Voice command to take photo"""
    if controller.check_adb_connection():
        controller.take_photo()
        speak("Photo taken")
    else:
        speak("Phone not connected via ADB")