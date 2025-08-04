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
from pipes import quote
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
from engine.mobile import ADBPhoneController
import os
from engine.helper import extract_yt_term, remove_words
from engine.command import speak
from engine.config import ASSISTANT_NAME



con = sqlite3.connect("jarvis.db")
cursor = con.cursor()

@eel.expose
def playAssistantSound():
    music_dir = "www\\assets\\audio\\game-start-317318.mp3"
    playsound(music_dir)






def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query = query.lower().strip()
    app_name = query

    if app_name != "":
        try:
            # Check in system file command DB
            cursor.execute('SELECT path FROM sys_command WHERE name = ?', (app_name,))
            results = cursor.fetchall()

            if results:
                path = results[0][0]
                if path.endswith(".exe") and os.path.exists(path):
                    speak("Opening " + app_name)
                    os.startfile(path)
                else:
                    # It might be a system protocol like "start calculator:"
                    speak("Opening " + app_name)
                    os.system(f'start {path}')
            else:
                # Check in web commands
                cursor.execute('SELECT url FROM web_command WHERE name = ?', (app_name,))
                results = cursor.fetchall()

                if results:
                    speak("Opening " + app_name)
                    webbrowser.open(results[0][0])
                else:
                    # Fallback for system apps like "start whatsapp:"
                    speak("Opening " + app_name)
                    os.system(f'start {app_name}:')
        except Exception as e:
            speak("Something went wrong")
            print("Error:", e)



       

def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing "+search_term+" on YouTube")
    kit.playonyt(search_term)


def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
       
        # pre trained keywords    
        porcupine=pvporcupine.create(keywords=["jarvis","alexa"]) 
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index>=0:
                print("hotword detected")

                # pressing shorcut key win+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
                
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()



# find contacts
def findContact(query):
    
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])

        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0

def shutdown():
    import sys
    speak("ok bye we will meet again")
    eel.close_window()
    sys.exit(0)

import pyautogui
import time

def whatsApp(mobile_no, message, flag, name):
    """
    Automate WhatsApp actions using image recognition instead of tab navigation
    
    Args:
        mobile_no (str): Phone number with country code
        message (str): Message to send
        flag (str): 'message', 'call', or 'video'
        name (str): Contact name for confirmation message
    """
    
    # Define button image paths - store your PNG files in an 'images' folder
    button_images = {
        'send': 'engine\\send_icon.png',
        'call': 'engine\\call_icon.png', 
        'video': 'engine\\video_icon.png'
      # if you want to add photo functionality
    }
    
    # Set action-specific parameters
    if flag == 'message':
        target_button = 'send'
        jarvis_message = f"Message sent successfully to {name}"
        
    elif flag == 'call':
        target_button = 'call'
        message = ''  # No message needed for calls
        jarvis_message = f"Calling {name}"
        
    elif flag == 'video':
        target_button = 'video'
        message = ''  # No message needed for video calls
        jarvis_message = f"Starting video call with {name}"
        
    else:
        print(f"Invalid flag: {flag}. Use 'message', 'call', or 'video'")
        return

    try:
        # Encode the message for URL
        encoded_message = quote(message)
        print(f"Encoded message: {encoded_message}")
        
        # Construct the WhatsApp URL
        whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"
        full_command = f'start "" "{whatsapp_url}"'
        
        # Open WhatsApp
        subprocess.run(full_command, shell=True)
        time.sleep(5)  # Wait for WhatsApp to load
        
        # Wait a bit more for the chat to fully load
        time.sleep(2)
        
        # Check if button image file exists
        button_path = button_images[target_button]
        if not os.path.exists(button_path):
            print(f"Button image not found: {button_path}")
            print("Please ensure you have the required PNG files in the images folder")
            return
        
        # Try to locate and click the button
        button_location = None
        max_attempts = 10
        
        for attempt in range(max_attempts):
            try:
                button_location = pyautogui.locateOnScreen(button_path, confidence=0.8)
                if button_location:
                    break
            except pyautogui.ImageNotFoundException:
                pass
            
            time.sleep(1)  # Wait 1 second between attempts
            print(f"Attempt {attempt + 1}: Looking for {target_button} button...")
        
        if button_location:
            # Click the button
            button_center = pyautogui.center(button_location)
            pyautogui.click(button_center)
            print(f"Successfully clicked {target_button} button")
            
            # Call the speak function (assuming it exists)
            try:
                speak(jarvis_message)
            except NameError:
                print(jarvis_message)  # Fallback if speak function not available
                
        else:
            print(f"Could not find {target_button} button after {max_attempts} attempts")
            print("Please check if:")
            print("1. WhatsApp is properly loaded")
            print("2. The button image PNG matches the current WhatsApp interface")
            print("3. The chat window is visible and active")
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# chat bot 
from groq import Groq
from dotenv import load_dotenv
import os
from engine.config import ASSISTANT_NAME

# Load environment variables
load_dotenv()

# Set up Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def chatBot(query):
    try:
        # Groq API call
        response = client.chat.completions.create(
            model="llama3-8b-8192",  # or "mixtral-8x7b-32768" or "llama3-70b-8192"
            messages=[
                {"role": "system", "content": f"You are {ASSISTANT_NAME}, a helpful AI assistant."},
                {"role": "user", "content": query}
            ],
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            stream=False
        )
        
        reply = response.choices[0].message.content
        print(reply)
        speak(reply)
        eel.DisplayMessage(reply)  # Assuming eel is used for UI
        return reply
        
    except Exception as e:
        print(f"Error: {e}")
        return None
# android automation

def makeCall(name, mobileNo):
    mobileNo = mobileNo.replace(" ", "")
    speak("Opening dialer for " + name)
    
    # Use ACTION_DIAL instead - no permission required
    command = 'adb shell am start -a android.intent.action.DIAL -d tel:' + mobileNo
    os.system(command)


# to send message
def sendMessage(message, mobileNo, name):
    speak("Sending message to " + name)
    
    # Clean the mobile number
    mobileNo = mobileNo.replace(" ", "").replace("-", "")
    
    # Use SMS intent - works with any SMS app
    command = f'adb shell am start -a android.intent.action.SENDTO -d sms:{mobileNo} --es sms_body "{message}"'
    
    result = os.system(command)
    
    if result == 0:
        speak(f"Message prepared for {name}. Please tap send.")
    else:
        speak("Failed to open messaging app")




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

#chatbot 


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
from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())
import requests
def getWeather(query):
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        speak("Weather API key not found. Please check your .env file.")
        return
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


    