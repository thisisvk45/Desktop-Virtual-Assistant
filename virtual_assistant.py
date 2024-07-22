import pyttsx3
import speech_recognition as sr
import datetime 
import os
import wikipedia
import pywhatkit
import pyautogui
import smtplib

# Initialize the speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wish_me():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am your assistant. Please tell me how I can help you.")

def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"You said: {query}\n")
    except Exception as e:
        print(f"Error: {e}")
        speak("Sorry, I didn't catch that. Please say that again.")
        return "none"
    return query.lower()

def send_email(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        # Login with your own email and password
        server.login('your-email@gmail.com', 'your-password')
        server.sendmail('your-email@gmail.com', to, content)
        server.close()
        speak("Email has been sent successfully.")
    except Exception as e:
        print(e)
        speak("Sorry, I am not able to send the email at the moment.")

if __name__ == '__main__':
    wish_me()
    while True:
        query = take_command()

        if 'wake up' in query:
            wish_me()

        elif 'time' in query:
            str_time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {str_time}")

        elif 'open microsoft edge' in query:
            speak("Opening Microsoft Edge")
            os.startfile("C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe")

        elif 'open brave' in query:
            speak("Opening Brave Browser")
            os.startfile("C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe")

        elif 'search' in query:
            query = query.replace("search", "")
            pywhatkit.search(query)
            speak("Here are the search results.")

        elif 'wikipedia' in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            speak(results)
            print(results)

        elif 'play' in query:
            query = query.replace("play", "")
            speak(f"Playing {query} on YouTube")
            pywhatkit.playonyt(query)

        elif 'type' in query:
            speak("What should I type?")
            while True:
                typing_command = take_command()
                if typing_command == "exit typing":
                    speak("Exiting typing mode.")
                    break
                else:
                    pyautogui.write(typing_command)

        elif 'send email' in query:
            try:
                speak("What should I say?")
                content = take_command()
                speak("Whom should I send it to?")
                to = "recipient@example.com"  # Replace with the recipient's email
                send_email(to, content)
            except Exception as e:
                print(e)
                speak("Sorry, I am not able to send the email at the moment.")

        elif 'exit' in query:
            speak("Goodbye! Have a great day.")
            break

        else:
            speak("I am sleeping.")
