import pyttsx3
import speech_recognition as sr
import eel
import time
from engine.features import apps, open_app, search_in_chrome, go_home, take_screenshot, increase_volume, decrease_volume, toggle_wifi, toggle_bluetooth, play_pause_music, next_song


def speak(text):
    text = str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 174)
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()


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
    except Exception:
        return ""
    return query.lower()


@eel.expose
def allCommands(message=1):
    if message == 1:
        query = takecommand()
        eel.senderText(query)
    else:
        query = message.lower()
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

        # Mobile app control
        for app in apps:
            if f"open {app} on mobile" in query:
                open_app(app)
                break

        if "search" in query and "in chrome on mobile" in query:
            query_text = query.replace("search", "").replace("in chrome on mobile", "").strip()
            search_in_chrome(query_text)

        elif "home screen of mobile" in query:
            go_home()
        elif "volume up" in query:
            from engine.features import increase_volume
            increase_volume()
        elif "volume down" in query:
            decrease_volume()
        elif "wifi on" in query:
            toggle_wifi()
        elif "bluetooth toggle" in query:
            toggle_bluetooth()
        elif "next song" in query:
            next_song()
        elif "pause music " in query:
            play_pause_music()
        elif "open camera on mobile" in query:
            open_app("camera")

        elif "send message" in query or "phone call" in query or "video call" in query:
            from engine.features import findContact, whatsApp, makeCall, sendMessage
            contact_no, name = findContact(query)
            if contact_no:
                speak("Which mode you want to use whatsapp or mobile")
                preferance = takecommand()

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

    except Exception as e:
        print("error:", e)

    eel.ShowHood()
