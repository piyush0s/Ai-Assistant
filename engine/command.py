import pyttsx3
import speech_recognition as sr
import eel
import time
from engine.mobile_command import handle_mobile_command

def jarvisCommand(query):
    # your other commands...

    if any(kw in query for kw in ["on mobile", "in mobile", "phone"]):
        handle_mobile_command(query)

def speak(text):
    text = str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices') 
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 174)

   
    eel.DisplayMessage(text)

    time.sleep(0.5)

    
    engine.say(text)
    engine.runAndWait()

   
    time.sleep(0.5)
    
    # Now show the response in chat
    eel.receiverText(text)

    # Hide the SiriWave and show default idle state
    eel.ShowHood()
    

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('listening....')
        eel.DisplayMessage('listening....')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, 10, 6)

    try:
        print('recognizing')
        eel.DisplayMessage('recognizing....')
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)
    except Exception as e:
        return ""
    return query.lower()

@eel.expose
def allCommands(message=1):
    if message == 1:
        query = takecommand()
        print(query)
        eel.senderText(query)
    else:
        query = message
        eel.senderText(query)

    try:
         
        
        if "open" in query:
            from engine.features import openCommand
            openCommand(query)

        elif "on youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)

        elif "play" in query and "spotify" in query:
            from engine.features import playSpotifySong
            playSpotifySong(query)

        elif "create password" in query or "generate password" in query:
            from engine.features import createPassword
            createPassword()
            
        elif "what can you do" in query or "list your features" in query:
            speak("Here are some things I can do: open apps, play music, search Google or YouTube, tell jokes, check weather, take screenshots, book cabs, send messages and much more.")


        elif "search" in query and "on google" in query:
            from engine.features import searchGoogle
            searchGoogle(query)

        elif "screenshot" in query:
            from engine.features import takeScreenshot
            takeScreenshot()

        elif "calculate" in query:
            from engine.features import calculateExpression
            calculateExpression(query)

        elif "toss a coin" in query:
            from engine.features import tossCoin
            tossCoin()

        elif "roll a dice" in query:
            from engine.features import rollDice
            rollDice()

        elif "what's the time" in query or "what's the date" in query:
            from engine.features import tellDateTime
            tellDateTime()

        elif "check internet" in query:
            from engine.features import checkInternet
            checkInternet()

        elif "tell me a joke" in query:
            from engine.features import tellJoke
            tellJoke()

        elif "weather in" in query:
            from engine.features import getWeather
            city = query.split("in")[-1].strip()
            getWeather(city)

        

        elif "news" in query:
            from engine.features import getNews
            getNews()
        elif "book a cab" in query or "book a ride" in query:
            from engine.features import book_cab
            book_cab(query)

        elif "send message" in query or "phone call" in query or "video call" in query:
            from engine.features import findContact, whatsApp, makeCall, sendMessage
            contact_no, name = findContact(query)
            if(contact_no != 0):
                speak("Which mode you want to use whatsapp or mobile")
                preferance = takecommand()
                print(preferance)

                if "mobile" in preferance:
                    if "send message" in query or "send sms" in query: 
                        speak("what message to send")
                        message = takecommand()
                        sendMessage(message, contact_no, name)
                    elif "phone call" in query:
                        makeCall(name, contact_no)
                    else:
                        speak("please try again")
                elif "whatsapp" in preferance:
                    message = ""
                    if "send message" in query:
                        message = 'message'
                        speak("what message to send")
                        query = takecommand()
                    elif "phone call" in query:
                        message = 'call'
                    else:
                        message = 'video call'
                    whatsApp(contact_no, query, message, name)

        else:
            from engine.features import chatBot
            chatBot(query)

    except:
        print("error")

    eel.ShowHood()