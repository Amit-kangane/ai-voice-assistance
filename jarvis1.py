import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import datetime
import time
import os
import pyautogui
import webbrowser
import threading
import tkinter as tk
from tkinter import scrolledtext, Label
from PIL import Image, ImageTk
import openai
import requests

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id) 

def speak(text):
    """Speaks out the given text and displays it in the GUI."""
    engine.say(text)
    engine.runAndWait()
    update_gui(f"JARVIS: {text}\n")

# Initialize speech recognition
def take_command():
    """Listens for user commands and returns the recognized text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        update_gui("Listening...\n")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        update_gui("Recognizing...\n")
        command = recognizer.recognize_google(audio, language="en-IN")
        update_gui(f"You said: {command}\n")
        return command.lower()
    except Exception as e:
        update_gui("Sorry, I didn't understand that.\n")
        return ""

 

def run_jarvis():
    """Continuously listens for and executes commands."""
    while True:
        command = take_command()
        if not command:
            continue
        
        if "play" in command:
            song = command.replace("play", "").strip()
            speak(f"Playing {song}")
            pywhatkit.playonyt(song)

        elif "time" in command:
            time_now = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The time is {time_now}")

        elif "who is" in command:
            person = command.replace("who is", "").strip()
            try:
                info = wikipedia.summary(person, sentences=2)
                speak(info)
            except wikipedia.exceptions.DisambiguationError:
                speak("There are multiple results. Please be more specific.")
            except wikipedia.exceptions.PageError:
                speak("Sorry, I couldn't find any information.")

        elif "open" in command:
            app = command.replace("open", "").strip()
            speak(f"Opening {app}")
            
            if "youtube" in app:
                webbrowser.open("https://www.youtube.com")
            elif "google" in app:
                webbrowser.open("https://www.google.com")
            elif "chat gpt" in app or "chat" in app:
                webbrowser.open("https://chatgpt.com/")
            else:
                os.system(f"start {app}")

        elif "search" in command:
            query = command.replace("search", "").strip()
            speak(f"Searching for {query}")
            pywhatkit.search(query)

         

        elif "exit" in command or "stop" in command:
            speak("Goodbye!")
            time.sleep(5)
            root.quit()
            break

        else:
            speak("Sorry, I don't understand that command.")

def start_jarvis():
    """Runs JARVIS in a separate thread to keep the GUI responsive."""
    threading.Thread(target=run_jarvis, daemon=True).start()

def update_gui(text):
    """Updates the GUI output box with text."""
    output_box.insert(tk.END, text)
    output_box.see(tk.END)

# Create GUI window
root = tk.Tk()
root.title("JARVIS AI Assistant")
root.geometry("500x500")
root.configure(bg="black")

# Output display box
output_box = scrolledtext.ScrolledText(root, width=60, height=15, bg="black", fg="lime", font=("Courier", 10))
output_box.pack(pady=10)

# Image display label
image_label = Label(root, bg="black")
image_label.pack(pady=5)

# Start button
start_button = tk.Button(root, text="Start JARVIS", command=start_jarvis, bg="green", fg="white", font=("Arial", 12))
start_button.pack(pady=5)

# Stop button
stop_button = tk.Button(root, text="Exit", command=root.quit, bg="red", fg="white", font=("Arial", 12))
stop_button.pack(pady=5)

speak("Hello, I am JARVIS. Click the Start button to begin.")
root.mainloop()
