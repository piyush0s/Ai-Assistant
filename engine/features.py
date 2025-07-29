import os
import re
import sqlite3
import struct
import subprocess
import time
import webbrowser
import random
import string
import datetime
import socket
import urllib.parse

import requests
import pyttsx3
import pyautogui
import pyperclip
import pyjokes
import eel
import pyaudio
import speech_recognition as sr
import pvporcupine
from playsound import playsound
from geopy.geocoders import Nominatim
import pywhatkit as kit
from dotenv import load_dotenv
load_dotenv()
import os

from engine.command import speak
from engine.config import ASSISTANT_NAME
from engine.helper import extract_yt_term, remove_words, replace_spaces_with_percent_s, goback, keyEvent, tapEvents, adbInput

# Database connection
con = sqlite3.connect("jarvis.db")
cursor = con.cursor()

# Exposed eel function
@eel.expose
def playAssistantSound():
    playsound("www/assets/audio/game-start-317318.mp3")

# Listen function

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
        try:
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
        except sr.RequestError:
            speak("Speech recognition service is unavailable.")
        return ""

# App launcher
def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "").replace("open", "").strip().lower()
    try:
        cursor.execute('SELECT path FROM sys_command WHERE name = ?', (query,))
        result = cursor.fetchone()
        if result:
            speak("Opening " + query)
            os.startfile(result[0])
            return

        cursor.execute('SELECT url FROM web_command WHERE name = ?', (query,))
        result = cursor.fetchone()
        if result:
            speak("Opening " + query)
            webbrowser.open(result[0])
            return

        speak("Opening " + query)
        os.system('start ' + query)
    except:
        speak("Something went wrong while trying to open it.")

# YouTube

def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing " + search_term + " on YouTube")
    kit.playonyt(search_term)

# Hotword detection
def hotword():
    porcupine = None
    paud = None
    audio_stream = None
    try:
        porcupine = pvporcupine.create(keywords=["jarvis", "alexa"])
        paud = pyaudio.PyAudio()
        audio_stream = paud.open(rate=porcupine.sample_rate, channels=1, format=pyaudio.paInt16, input=True, frames_per_buffer=porcupine.frame_length)
        while True:
            keyword = audio_stream.read(porcupine.frame_length)
            keyword = struct.unpack_from("h" * porcupine.frame_length, keyword)
            if porcupine.process(keyword) >= 0:
                pyautogui.keyDown("win")
                pyautogui.press("j")
                time.sleep(2)
                pyautogui.keyUp("win")
    except:
        speak("Error with hotword detection")
    finally:
        if porcupine:
            porcupine.delete()
        if audio_stream:
            audio_stream.close()
        if paud:
            paud.terminate()

# Contact Finder
def findContact(query):
    query = remove_words(query, [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']).strip().lower()
    try:
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        result = cursor.fetchone()
        if result:
            mobile = result[0]
            return ('+91' + mobile if not mobile.startswith('+91') else mobile), query
    except:
        pass
    speak('Not found in contacts')
    return 0, 0

# WhatsApp communication
def whatsApp(mobile_no, message, flag, name):
    tab_map = {'message': 17, 'call': 13, 'video': 12}
    tab_count = tab_map.get(flag, 17)
    jarvis_message = {
        'message': f"Message sent successfully to {name}",
        'call': f"Calling {name}",
        'video': f"Starting video call with {name}"
    }.get(flag, "Action done")

    encoded_msg = urllib.parse.quote(message)
    url = f"whatsapp://send?phone={mobile_no}&text={encoded_msg}"
    subprocess.run(f'start "" "{url}"', shell=True)

    time.sleep(5)
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(1)
    for _ in range(tab_count):
        pyautogui.press('tab')
        time.sleep(0.05)
    pyautogui.press('enter')
    if flag == 'message':
        pyautogui.write(message)
        pyautogui.press('enter')
    speak(jarvis_message)

# OpenRouter ChatBot
import openai
from dotenv import load_dotenv
load_dotenv()
import os
openai.api_key = os.getenv("OPENROUTER_API_KEY")
openai.api_base = "https://openrouter.ai/api/v1"

def chatBot(query):
    response = openai.ChatCompletion.create(
        model="meta-llama/llama-3-8b-instruct",
        messages=[{"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": query}]
    )
    reply = response['choices'][0]['message']['content']
    print(reply)
    speak(reply)
    return reply

# Mobile Calls and SMS (ADB)
def makeCall(name, mobileNo):
    speak("Calling " + name)
    os.system(f'adb shell am start -a android.intent.action.CALL -d tel:{mobileNo.strip()}')

def sendMessage(message, mobileNo, name):
    message = replace_spaces_with_percent_s(message)
    mobileNo = replace_spaces_with_percent_s(mobileNo)
    speak("Sending message")
    goback(4)
    time.sleep(1)
    keyEvent(3)
    time.sleep(1)
    tapEvents(540, 2220)
    time.sleep(1)
    tapEvents(950, 1800)
    time.sleep(1)
    adbInput(mobileNo)
    time.sleep(1)
    tapEvents(500, 600)
    time.sleep(1)
    tapEvents(500, 2200)
    time.sleep(1)
    adbInput(message)
    time.sleep(1)
    tapEvents(980, 2150)
    speak("Message sent successfully to " + name)

import os

def open_app(app_name):
    apps = {
    # Social & Communication
    "whatsapp": "com.whatsapp",
    "linkedin": "com.linkedin.android",
    "instagram": "com.instagram.android",
    "telegram": "org.telegram.messenger",
    "facebook": "com.facebook.katana",
    "messenger": "com.facebook.orca",
    "twitter": "com.twitter.android",
    "gmail": "com.google.android.gm",
    "messages": "com.google.android.apps.messaging",
    "snapchat": "com.snapchat.android",

    # Entertainment & Media
    "youtube": "com.google.android.youtube",
    "youtube music": "com.google.android.apps.youtube.music",
    "spotify": "com.spotify.music",
    "netflix": "com.netflix.mediaclient",
    "mx player": "com.mxtech.videoplayer.ad",
    "hotstar": "in.startv.hotstar",
    "prime video": "com.amazon.avod.thirdpartyclient",

    # AI & Tools
    "chatgpt": "com.openai.chatgpt",
    "gemini": "com.google.android.apps.bard",
    "notion": "notion.id",
    "zomato": "com.application.zomato",
    "amazon": "in.amazon.mShop.android.shopping",
    "flipkart": "com.flipkart.android",
    "paytm": "net.one97.paytm",
    "phonepe": "com.phonepe.app",
    "camera": "com.android.camera",
    "calculator": "com.android.calculator2",
    "files": "com.google.android.apps.nbu.files",
    "settings": "com.android.settings",

    # Google & Browsing
    "chrome": "com.android.chrome",
    "google": "com.google.android.googlequicksearchbox",
    "photos": "com.google.android.apps.photos",
    "maps": "com.google.android.apps.maps",
    "calendar": "com.google.android.calendar",
    "drive": "com.google.android.apps.docs",
    "play store": "com.android.vending",
}


    if app_name in apps:
        package = apps[app_name]
        os.system(f"adb shell monkey -p {package} -c android.intent.category.LAUNCHER 1")
    else:
        print(f"App '{app_name}' not configured.")

def go_home():
    os.system("adb shell input keyevent 3")
    
def search_in_chrome(query):
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    os.system(f'adb shell am start -a android.intent.action.VIEW -d "{search_url}" com.android.chrome')

def take_screenshot():
    os.system("adb shell screencap -p /sdcard/screen.png")
    os.system("adb pull /sdcard/screen.png ./screen.png")

def increase_volume():
    os.system("adb shell input keyevent 24")

def decrease_volume():
    os.system("adb shell input keyevent 25")

def open_settings():
    os.system("adb shell am start -a android.settings.SETTINGS")

def toggle_wifi():
    os.system("adb shell svc wifi enable")  # or disable

def toggle_bluetooth():
    os.system("adb shell service call bluetooth_manager 6")  # Toggle state

def play_pause_music():
    os.system("adb shell input keyevent 85")

def next_song():
    os.system("adb shell input keyevent 87")

def previous_song():
    os.system("adb shell input keyevent 88")

# Password Generator
def createPassword(length=12, copy_to_clipboard=True):
    length = max(6, length)
    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(chars) for _ in range(length))
    if copy_to_clipboard:
        pyperclip.copy(password)
    speak("Here is your password")
    print(f"Generated Password: {password}")
    return password

# Spotify

def playSpotifySong(query):
    song_name = remove_words(query, [ASSISTANT_NAME, "play", "on", "spotify", "music", "song"]).strip()
    if song_name:
        speak(f"Searching {song_name} on Spotify")
        os.system(f'start spotify:search:{urllib.parse.quote(song_name)}')
    else:
        speak("Please tell me the name of the song to play on Spotify.")

# Google search
def searchGoogle(query):
    q = query.replace("search", "").replace("on google", "").strip()
    url = f"https://www.google.com/search?q={q.replace(' ', '+')}"
    speak(f"Searching {q} on Google")
    webbrowser.open(url)

# Screenshot
def takeScreenshot():
    time.sleep(4)
    pyautogui.screenshot("screenshot.png")
    speak("Screenshot saved successfully")

# Math calculation
def calculateExpression(query):
    try:
        expression = query.replace("calculate", "").strip()
        result = eval(expression)
        speak(f"The answer is {result}")
    except:
        speak("Sorry, I couldn't calculate that.")

# Toss and dice
def tossCoin():
    speak(f"It's {random.choice(['Heads', 'Tails'])}")

def rollDice():
    speak(f"You rolled a {random.randint(1, 6)}")

# Time and date
def tellDateTime():
    now = datetime.datetime.now()
    speak(f"Today is {now.strftime('%A, %B %d, %Y')} and the time is {now.strftime('%I:%M %p')}")

# Internet connection check
def checkInternet():
    try:
        socket.create_connection(("www.google.com", 80))
        speak("Internet is connected")
    except OSError:
        speak("No internet connection")

# Jokes
def tellJoke():
    speak(pyjokes.get_joke())

# Weather
def getWeather(query):
    api_key = os.getenv("WEATHER_API_KEY")
    for word in ["what", "is", "the", "weather", "in", "like", "tell", ASSISTANT_NAME]:
        query = query.replace(word, "")
    city = query.strip() or "Delhi"
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
    try:
        data = requests.get(url).json()
        speak(f"Currently in {city}, it is {data['current']['temp_c']} degrees and {data['current']['condition']['text']}")
    except:
        speak("Sorry, I couldn't fetch the weather information.")

# News
def getNews():
    speak("Fetching top headlines")
    url = "https://newsapi.org/v2/top-headlines?country=in&apiKey=os.getenv('NEWS_API_KEY')"
    try:
        news = requests.get(url).json()
        for i, article in enumerate(news["articles"][:5]):
            speak(f"Headline {i+1}: {article['title']}")
    except:
        speak("Failed to fetch news.")

# Coordinates
def get_coordinates(location):
    geolocator = Nominatim(user_agent="jarvis_cab_locator")
    loc = geolocator.geocode(location)
    return (loc.latitude, loc.longitude) if loc else (None, None)

# Cab booking
def book_cab():
    speak("Which platform do you want to use: Ola, Uber, or Rapido?")
    platform = listen().lower()
    speak("Please tell me your pickup location.")
    pickup = listen()
    speak("Now tell me your drop location.")
    drop = listen()

    pickup_lat, pickup_long = get_coordinates(pickup)
    drop_lat, drop_long = get_coordinates(drop)

    if None in (pickup_lat, drop_lat):
        speak("Sorry, I couldn't find the coordinates.")
        return

    if platform == "uber":
        url = f"https://m.uber.com/ul/?action=setPickup&pickup[latitude]={pickup_lat}&pickup[longitude]={pickup_long}&dropoff[latitude]={drop_lat}&dropoff[longitude]={drop_long}&dropoff[nickname]={urllib.parse.quote(drop)}"
    elif platform == "ola":
        url = f"https://book.olacabs.com/?pickup={urllib.parse.quote(pickup)}&drop={urllib.parse.quote(drop)}"
    elif platform == "rapido":
        url = f"https://rapido.bike/app/book?pickup={urllib.parse.quote(pickup)}&drop={urllib.parse.quote(drop)}"
    else:
        speak("Sorry, this platform is not supported.")
        return

    speak(f"Opening {platform} booking page for you.")
    webbrowser.open(url)
