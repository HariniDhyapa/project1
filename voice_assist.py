import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import random
import pyjokes
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 170) 

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("Hello How can I assist you today?")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source) 
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')  
        print(f"User said: {query}\n")
        return query.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Could you repeat?")
        return "None"
    except sr.RequestError:
        speak("Network error. Please check your internet connection.")
        return "None"

def executeCommand(query):
    if 'wikipedia' in query:
        speak('Searching Wikipedia...')
        query = query.replace("wikipedia", "")
        try:
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia:")
            print(results)
            speak(results)
        except wikipedia.exceptions.DisambiguationError as e:
            speak("Multiple results found, please be more specific.")
        except wikipedia.exceptions.PageError:
            speak("Sorry, no relevant page found.")

    elif 'open youtube' in query:
        webbrowser.open("https://www.youtube.com")

    elif 'open google' in query:
        webbrowser.open("https://www.google.com")

    elif 'open stack overflow' in query:
        webbrowser.open("https://stackoverflow.com")

    elif 'play music' in query:
        music_dir = ''
        if os.path.exists(music_dir):
            songs = os.listdir(music_dir)
            if songs:
                random_song = random.choice(songs)
                print(f"Playing: {random_song}")
                os.startfile(os.path.join(music_dir, random_song))
                speak(f"Playing {random_song}")
            else:
                speak("No music files found in the directory.")
        else:
            speak("Music directory not found.")

    elif 'the time' in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {strTime}")

    elif 'tell me a joke' in query:
        joke = pyjokes.get_joke()
        print(joke)
        speak(joke)

    elif 'shutdown' in query or 'shut down' in query:
        speak("Are you sure you want to shut down the system?")
        confirmation = takeCommand()
        if 'yes' in confirmation:
            speak("Shutting down the system.")
            os.system("shutdown /s /t 5")
        else:
            speak("Shutdown aborted.")

    elif 'exit' in query or 'quit' in query:
        speak("Goodbye! Have a great day.")
        exit()

    else:
        speak("Sorry, I didn't understand that command.")

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand()
        if query != "None":
            executeCommand(query)
