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
    query.lower()

    app_name = query.strip()

    if app_name != "":

        try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening "+query)
                    try:
                        os.system('start '+query)
                    except:
                        speak("not found")
        except:
            speak("some thing went wrong")

       

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

def whatsApp(mobile_no, message, flag, name):
    import time
    import pyautogui
    
    jarvis_message = {
        'message': f"Message sent successfully to {name}",
        'call': f"Calling {name}",
        'video': f"Starting video call with {name}"
    }.get(flag, "Action completed")

    try:
        speak(f"Opening WhatsApp for {name}")
        
        # Use Ctrl+F to search (more reliable)
        pyautogui.hotkey('ctrl', 'f')
        time.sleep(0.5)
        
        # Clear search and type name
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write(name)
        time.sleep(1)
        pyautogui.press('enter')  # Select contact
        time.sleep(1)
        
        if flag == 'message':
            # Press Tab to go to message input (usually 1-2 tabs from search)
            pyautogui.press('tab')  # Move to chat area
            time.sleep(0.2)
            pyautogui.press('tab')  # Move to message input
            time.sleep(0.2)
            
            pyautogui.write(message)
            pyautogui.press('enter')
            speak(jarvis_message)
            
        elif flag == 'call':
            # Navigate to call button (usually Shift+Tab from message input)
            pyautogui.hotkey('shift', 'tab')  # Go backwards to header
            time.sleep(0.2)
            pyautogui.hotkey('shift', 'tab')
            time.sleep(0.2)
            pyautogui.press('enter')  # Click call button
            speak(jarvis_message)
            
        elif flag == 'video':
            # Navigate to video call button
            pyautogui.hotkey('shift', 'tab')  # Go to header area
            time.sleep(0.2)
            pyautogui.press('tab')  # Move to video call
            time.sleep(0.2)
            pyautogui.press('enter')
            speak(jarvis_message)
            
    except Exception as e:
        print(f"Error: {e}")
        speak(f"Failed to complete WhatsApp {flag}")

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