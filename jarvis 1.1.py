import os
import random
import datetime
import wikipedia
import webbrowser
import requests
import threading
from gtts import gTTS
from playsound import playsound
import time
import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr

user_name = "Minhaj"
listening = False

music = {
    "zehra": "https://www.youtube.com/watch?v=-xSEVqi_jVk",
    "believer": "https://www.youtube.com/watch?v=7wtfhZwyrcc",
    "faded": "https://www.youtube.com/watch?v=60ItHLz5WEA"
}

def speak(text):
    try:
        filename = f"voice_{random.randint(1, 100000)}.mp3"
        tts = gTTS(text=text, lang='en')
        tts.save(filename)
        playsound(filename)
        os.remove(filename)
    except Exception as e:
        output.insert(tk.END, f"\n[Error in speak()] {e}\n")

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        greeting = "Good Morning!"
    elif hour < 18:
        greeting = "Good Afternoon!"
    else:
        greeting = "Good Evening!"
    speak(greeting + " I am Jarvis. Say 'Jarvis' to activate me.")
    output.insert(tk.END, f"{greeting} I am Jarvis. Say 'Jarvis' to activate me.\n")

def get_weather(city):
    try:
        api_key = "f42b0d0e2a808c697e0fccf5f4c400c7"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        res = requests.get(url).json()
        if res["cod"] == 200:
            temp = res["main"]["temp"]
            desc = res["weather"][0]["description"]
            return f"The temperature in {city} is {temp}°C with {desc}."
        else:
            return "City not found."
    except:
        return "Unable to fetch weather."

def tell_joke():
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Parallel lines have so much in common... it’s a shame they’ll never meet.",
        "I told my computer I needed a break, and it said: No problem — I’ll go to sleep!",
        "Why did the computer catch a cold? Because it had too many bugs."
    ]
    joke = random.choice(jokes)
    speak(joke)
    output.insert(tk.END, f"{joke}\n")

def calculator(expr):
    try:
        result = eval(expr)
        speak(f"The result is {result}")
        output.insert(tk.END, f"Result: {result}\n")
    except:
        speak("Sorry, I couldn't calculate that.")
        output.insert(tk.END, "Sorry, I couldn't calculate that.\n")

def tell_day():
    day = datetime.datetime.today().strftime("%A")
    speak(f"Today is {day}")
    output.insert(tk.END, f"Day: {day}\n")

def listen_voice(timeout=8, phrase_time_limit=6):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        output.insert(tk.END, "🎤 Listening...\n")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            query = recognizer.recognize_google(audio).lower()
            output.insert(tk.END, f"\n>>> {query}\n")
            return query
        except sr.WaitTimeoutError:
            output.insert(tk.END, "No voice input detected.\n")
        except sr.UnknownValueError:
            output.insert(tk.END, "Sorry, I didn't catch that.\n")
        except sr.RequestError:
            output.insert(tk.END, "Voice service is unavailable.\n")
        except Exception as e:
            output.insert(tk.END, f"\n[Error] {e}\n")
    return ""

def voice_thread():
    threading.Thread(target=jarvis_loop).start()

def jarvis_loop():
    global listening
    while True:
        if not listening:
            query = listen_voice(timeout=8, phrase_time_limit=4)
            if "jarvis" in query:
                speak("Yes, I am listening...")
                output.insert(tk.END, "🟢 Wake word detected: JARVIS\n")
                listening = True
        else:
            command = listen_voice(timeout=10, phrase_time_limit=7)
            if command:
                if any(x in command for x in ["exit", "quit", "bye"]):
                    speak("Goodbye! Have a nice day.")
                    root.destroy()
                    break
                process_command(command)

def process_command(query):
    global user_name

    if "my name is" in query:
        user_name = query.replace("my name is", "").strip()
        speak(f"Nice to meet you, {user_name}!")

    elif "what is my name" in query:
        speak(f"Your name is {user_name}")

    elif "wikipedia" in query:
        speak("Searching Wikipedia...")
        query = query.replace("wikipedia", "")
        try:
            result = wikipedia.summary(query, sentences=2)
            output.insert(tk.END, result + "\n")
            speak(result)
        except:
            speak("No result found.")

    elif "open" in query:
        sites = {
            "youtube": "https://www.youtube.com",
            "google": "https://www.google.com",
            "linkedin": "https://www.linkedin.com",
            "instagram": "https://www.instagram.com",
        }
        for key in sites:
            if key in query:
                webbrowser.open(sites[key])
                speak(f"Opening {key.capitalize()}")
                return

    elif "play" in query:
        song_name = query.replace("play", "").strip()
        if song_name in music:
            speak(f"Playing {song_name}")
            webbrowser.open(music[song_name])
        else:
            speak("Sorry, I couldn't find that song.")

    elif "search" in query:
        search = query.replace("search", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={search}")
        speak(f"Searching Google for {search}")

    elif "time" in query:
        now = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {now}")
        output.insert(tk.END, f"Time: {now}\n")

    elif "date" in query:
        today = datetime.date.today().strftime("%B %d, %Y")
        speak(f"Today's date is {today}")
        output.insert(tk.END, f"Date: {today}\n")

    elif "day" in query:
        tell_day()

    elif "weather in" in query:
        city = query.replace("weather in", "").strip()
        weather = get_weather(city)
        speak(weather)
        output.insert(tk.END, weather + "\n")

    elif "joke" in query:
        tell_joke()

    elif "calculate" in query:
        expr = query.replace("calculate", "").strip()
        calculator(expr)

    else:
        speak("Sorry, I didn't understand that.")
        output.insert(tk.END, "Sorry, I didn't understand that.\n")

# GUI
root = tk.Tk()
root.title("JARVIS 1.1 - Always Listening After Wake Word")
root.state("zoomed")
root.config(bg="#0f172a")

heading = tk.Label(root, text="🎙️ JARVIS 1.1 - Voice Assistant", font=("Segoe UI", 26, "bold"), bg="#0f172a", fg="#38bdf8")
heading.pack(pady=15)

output = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Consolas", 14), height=20, bg="#1e293b", fg="white")
output.pack(padx=20, pady=10, expand=True, fill=tk.BOTH)

mic_button = tk.Button(root, text="🎤 Start Listening", command=voice_thread, font=("Arial", 16), bg="#4ade80", fg="black")
mic_button.pack(pady=10)

root.after(1000, wishMe)
root.mainloop()