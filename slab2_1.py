# 1. Voice-Activated Personal Assistant 

import speech_recognition as sr
import pyttsx3
import requests
import time

engine = pyttsx3.init()

NEWS_API_KEY = "YOUR_NEWS_API_KEY"
WEATHER_API_KEY = "YOUR_OPENWEATHER_API_KEY"


def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()


def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print("You:", command)
        return command.lower()

    except sr.UnknownValueError:
        speak("Sorry, I could not understand.")
        return ""

    except sr.RequestError:
        speak("Speech recognition service is unavailable.")
        return ""


def get_weather(city):
    url = (
        f"https://api.openweathermap.org/data/2.5/weather?"
        f"q={city}&appid={WEATHER_API_KEY}&units=metric"
    )

    try:
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 200:
            speak("City not found.")
            return

        temperature = data["main"]["temp"]
        description = data["weather"][0]["description"]

        speak(
            f"The weather in {city} is {description} "
            f"with temperature {temperature} degree Celsius."
        )

    except:
        speak("Unable to get weather information.")


def get_news():
    url = (
        f"https://newsapi.org/v2/top-headlines?"
        f"country=in&apiKey={NEWS_API_KEY}"
    )

    try:
        response = requests.get(url)
        data = response.json()

        articles = data.get("articles", [])

        if len(articles) == 0:
            speak("No news found.")
            return

        speak("Here are the top 5 news headlines.")

        for i, article in enumerate(articles[:5], start=1):
            title = article.get("title", "No title")
            speak(f"Headline {i}: {title}")

    except:
        speak("Unable to fetch news.")


def set_reminder(seconds, message):
    speak(f"Reminder set for {seconds} seconds.")
    time.sleep(seconds)
    speak(f"Reminder: {message}")


speak("Hello! I am your personal assistant.")

while True:
    command = listen()

    if command == "":
        continue

    elif "weather" in command:
        speak("Please say the city name.")
        city = listen()

        if city != "":
            get_weather(city)

    elif "news" in command:
        get_news()

    elif "reminder" in command:
        speak("After how many seconds?")

        seconds_text = listen()

        try:
            seconds = int(seconds_text)

            speak("What should I remind you?")
            reminder_message = listen()

            if reminder_message != "":
                set_reminder(seconds, reminder_message)

        except ValueError:
            speak("Please say a valid number.")

    elif "exit" in command or "stop" in command or "bye" in command:
        speak("Goodbye!")
        break

    else:
        speak("Sorry, I don't understand that command.")