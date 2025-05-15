import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import pywhatkit
import pyjokes
import requests
import psutil

# Initialize the voice engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    print("Thronex:", text)
    engine.say(text)
    engine.runAndWait()

def wish_user():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning, Kalyan!")
    elif 12 <= hour < 18:
        speak("Good Afternoon, Kalyan!")
    else:
        speak("Good Evening, Kalyan!")
    speak("I am Thronex. How may I assist you today?")

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        command = r.recognize_google(audio, language='en-in')
        print(f"You said: {command}\n")
    except Exception as e:
        print("Sorry, I didn't catch that.")
        return "None"
    return command.lower()

def tell_joke():
    joke = pyjokes.get_joke()
    speak(joke)

def get_news():
    try:
        url = "https://newsapi.org/v2/top-headlines?language=en&apiKey=5820c6361d1743caa4e18e0958c08ac0"
        response = requests.get(url)
        data = response.json()

        # print("News API Response:", data)  # DEBUG: print entire response

        if data.get("status") != "ok":
            speak(f"News API error: {data.get('message', 'Unknown error')}")
            return

        articles = data.get("articles", [])[:5]
        if not articles:
            speak("No news articles found.")
            return

        speak("Here are the top news headlines:")
        for article in articles:
            speak(article["title"])

    except Exception as e:
        print("News error:", e)
        speak("Sorry, I couldn’t fetch the news.")

def get_weather():
    city = "Bangalore"  # Change or make dynamic
    api_key = "8b0f4876914cd0c3a4efa0974ae9cdf8"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        temp = data['main']['temp']
        desc = data['weather'][0]['description']
        speak(f"The temperature in {city} is {temp}°C with {desc}")
    except:
        speak("Unable to fetch weather details.")

def get_location():
    try:
        ip_info = requests.get("https://ipinfo.io/json").json()
        city = ip_info['city']
        region = ip_info['region']
        speak(f"You are currently in {city}, {region}.")
    except:
        speak("Sorry, I couldn't fetch your location.")

def battery_status():
    battery = psutil.sensors_battery()
    print("Battery object:", battery)
    if battery is None:
        print("No battery found.")
        speak("Battery information is not available.")
    else:
        percent = battery.percent
        print(f"Battery percent: {percent}")
        speak(f"The battery is at {percent} percent.")


def open_app(app_name):
    import os
    if "notepad" in app_name:
        os.system("notepad")
    elif "calculator" in app_name:
        os.system("calc")
    else:
        speak("I don't know how to open that application yet.")

def set_reminder():
    speak("What should I remind you about?")
    reminder = take_command()
    speak("In how many seconds?")
    seconds = int(take_command())
    speak(f"Okay, I will remind you to {reminder} in {seconds} seconds.")

    import time
    time.sleep(seconds)
    speak(f"Reminder: {reminder}")

def execute_command(command):
    if 'wikipedia' in command:
        speak('Searching Wikipedia...')
        query = command.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        speak(results)

    elif 'open youtube' in command:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube")

    elif 'open google' in command:
        webbrowser.open("https://www.google.com")
        speak("Opening Google")

    elif 'coding' in command:
        webbrowser.open("https://leetcode.com/problemset/")
        speak("Opening Leetcode")

    elif 'time' in command:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {strTime}")

    elif 'play' in command:
        song = command.replace('play', '')
        speak(f"Playing {song} on YouTube")
        pywhatkit.playonyt(song)

    elif 'joke' in command:
        tell_joke()

    elif 'news' in command:
        get_news()

    elif 'weather' in command:
        get_weather()

    elif 'location' in command:
        get_location()

    elif 'battery' in command:
        battery_status()

    elif 'open' in command:
        open_app(command)

    elif 'remind me' in command:
        set_reminder()

    elif 'who are you' in command or 'what are you' in command:
        speak("I am Thronex, your royal AI assistant, created to serve and assist Kalyan.")
        speak(
            "I obey your commands — whether it's playing music, fetching the latest headlines, or finding answers from the web.")
        speak("With the wisdom of the cloud and the power of code, I exist to make your digital reign effortless.")
        speak("Long live the King!")

    elif 'exit' in command or 'quit' in command or 'end' in command or 'stop' in command or 'bye' in command or 'tata' in command:
        speak("It was a pleasure talking to you Kalyan! 👋 ")
        exit()

    else:
        speak("I can’t do that yet. But I’m learning every day!")

# Main function
if __name__ == "__main__":
    wish_user()
    while True:
        command = take_command()
        if command != "None":
            execute_command(command)