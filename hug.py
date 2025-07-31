from openai import OpenAI
from dotenv import load_dotenv
import os
from engine.config import ASSISTANT_NAME
# # Load environment variables
# load_dotenv()

# Set up OpenAI client for version 1.98.0
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

def speak(text):
    """Add your text-to-speech implementation here"""
    # Example using pyttsx3:
    # import pyttsx3
    # engine = pyttsx3.init()
    # engine.say(text)
    # engine.runAndWait()
    pass

def chatBot(query):
    try:
        # Modern API call for OpenAI library version 1.x
        response = client.chat.completions.create(
            model="meta-llama/llama-3-8b-instruct",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": query}
            ]
        )
        
        reply = response.choices[0].message.content
        print(reply)
        speak(reply)
        return reply
        
    except Exception as e:
        print(f"Error: {e}")
        return None

# Test the function
if __name__ == "__main__":
    # Make sure to test with a simple query
    result = chatBot("Hello, how are you?")
    print(f"Function returned: {result}")


# from dotenv import load_dotenv,find_dotenv
# load_dotenv(find_dotenv())
# import requests
# def getWeather(query):
#     api_key = os.getenv("WEATHER_API_KEY")
#     if not api_key:
#         speak("Weather API key not found. Please check your .env file.")
#         return
#     for word in ["what", "is", "the", "weather", "in", "like", "tell", ASSISTANT_NAME]:
#         query = query.replace(word, "")
#     city = query.strip() or "Delhi"
#     url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
#     try:
#         data = requests.get(url).json()
#         speak(f"Currently in {city}, it is {data['current']['temp_c']} degrees and {data['current']['condition']['text']}")
#     except:
#         speak("Sorry, I couldn't fetch the weather information.")


# getWeather("what is the weather in Delhi")  # Example usage