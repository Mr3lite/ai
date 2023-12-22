import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import pywhatkit
import pyautogui

# Code to initialize pyttsx3 and set voices

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning sir")
    elif 12 <= hour < 18:
        speak("Good Afternoon sir")
    else:
        speak("Good Evening sir")
    

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = r.listen(source)
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
            return query.lower()
        except sr.UnknownValueError:
            print("Say that again please...")
            return "None"
        except sr.RequestError:
            print("There was an error with the recognition service.")
            speak("There was an error with the recognition service.")
            return "None"
        except sr.WaitTimeoutError:
            print("Timeout error. No speech detected.")
            return "None"
        

def close_browser_tab():
    pyautogui.hotkey('ctrl', 'w')

def close_browser():
    pyautogui.hotkey('alt', 'f4')

def open_newtab():
    pyautogui.hotkey('ctrl', 't')


def execute_query(query, time_greeting):
    if 'wikipedia' in query:
        try:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)
        except wikipedia.exceptions.DisambiguationError as e:
            print("Multiple results found. Please be more specific.")
            speak("Multiple results found. Please be more specific.")
        except wikipedia.exceptions.PageError as e:
            print("Page not found on Wikipedia.")
            speak("Page not found on Wikipedia.")

    elif 'search on google' in query:
        # Extract the search query after "search on Google"
        search_query = query.split("search on google")[-1].strip()
        # If there's a query after "search on Google", perform the search
        if search_query:
            search_url = f"https://www.google.com/search?q={search_query}"
            webbrowser.open(search_url)
            
    elif 'open' in query:
        sites = [
            ["youtube", "https://www.youtube.com"],
            ["wikipedia", "https://www.wikipedia.com"],
            ["google", "https://www.google.com"],
            ["facebook", "https://www.facebook.com"],
            ["instagram", "https://www.instagram.com"],
            ["blogger", "https://www.blogger.com"],
            ["twitter", "https://www.x.com"],
            ["whatsapp", "https://web.whatsapp.com/"],
            ["github", "https://github.com/"],
            ["gmail", "https://gmail.com/"],
            # Add more websites as needed
        ]
        for site in sites:
            if f"open {site[0]}".lower() in query.lower():
                speak(f"Opening {site[0]}...")
                webbrowser.open(site[1])

    elif 'the time' in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"Sir, the time is {strTime}")
        speak(f"Sir, the time is {strTime}")

    elif 'jay shri ram' in query:
        print(f"jai shri ram")
        speak(f"jay shree raam")

    elif 'play song' in query:
        speak("Sure, what song would you like me to play?")
        song = takeCommand()
        if song != "None":
            speak(f"Playing {song} on YouTube")
            pywhatkit.playonyt(song)

        elif sr.UnknownValueError:
            print("Sorry, I didn't catch the song name. please say again")
            speak("Sorry, I didn't catch the song name. please say again")
            song = takeCommand()
            speak(f"Playing {song} on YouTube")
            pywhatkit.playonyt(song)

        else:
            speak("please say for play again")

    elif 'play on youtube' in query:
        speak("Sure, what would you like me to play?")
        vid = takeCommand()
        if vid != "None":
            speak(f"Playing {vid} on YouTube")
            pywhatkit.playonyt(vid)
        
        elif sr.UnknownValueError:
            print("Sorry, I didn't catch the video name.")
            speak("Sorry, I didn't catch the video name.")
            vid = takeCommand()
            speak(f"Playing {vid} on YouTube")
            pywhatkit.playonyt(vid)

        else:
            speak("please say for play again")

    elif 'close the song' in query:
        speak("Closing the song.")
        close_browser_tab()

    elif 'close the browser' in query:
        speak("Closing the browser.")
        close_browser()

    elif 'close the tab' in query:
        close_browser_tab()
    
    elif 'open New tab' in query:
        open_newtab()

    elif time_greeting:  # Check if a time-based greeting was detected
        speak("Please tell me how may I help you")

    elif 'shutdown' in query:
        speak("Shutting down.")
        exit()

    else:
        print("Command not recognized.")
        speak("Command not recognized.")

if _name_ == "_main_":
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    last_interaction_time = datetime.datetime.now()
    try:
        wishMe()
        while True:
            current_time = datetime.datetime.now()
            difference = (current_time - last_interaction_time).seconds

            if difference >= 30:  # Adjust the time limit as needed (60 seconds in this example)
                speak("I'm going to sleep now.")
                print("I'm going to sleep now.")
                break

            query = takeCommand()
            if query != "None":
                hour = current_time.hour
                time_greeting = False
                if 0 <= hour < 12:
                    time_greeting = 'good morning' in query.lower()
                elif 12 <= hour < 18:
                    time_greeting = 'good afternoon' in query.lower()
                else:
                    time_greeting = 'good evening' in query.lower()

                execute_query(query, time_greeting)
                last_interaction_time = datetime.datetime.now()
    except KeyboardInterrupt:
        print("Program interrupted by the user.")
