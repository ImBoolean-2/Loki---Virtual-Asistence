import speech_recognition as sr
import openai
import pyttsx3
from PyQt5.QtWidgets import QMainWindow

openai.api_key = "Key-Here"

class listen_user(QMainWindow):
    def __init__(self):
        super().__init__()
        self.engine = pyttsx3.init()

    def listen(self):
        r = sr.Recognizer()
        while True: 
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source)

            try:
                print("Recognizing...")
                query = r.recognize_google(audio, language='es-ES')
                print(f"User said: {query}\n")  # Imprime la consulta del usuario

                if "Hey Lucky" in query:
                    user_instruction = query.replace("Hey Lucky", "").strip()  
                    self.process_instruction(user_instruction)
                    break 
            except Exception:
                print("Podrias repetirlo...")
                ## test
                self.process_instruction(user_instruction)

    def process_instruction(self, user_instruction):
        # Usa la API de GPT-3 para responder
        response = openai.completions.create(
            model="gpt-3.5-turbo-0613",
            prompt=f"You are a helpful assistant. {user_instruction}",
            stream=False,
            max_tokens=150
        )
        response_text = response['choices'][0]['text'].strip()  # Usa 'response' en lugar de 'completion'
        
        # Imprime la respuesta en la consola
        print(response_text)
        
        # Habla la respuesta
        self.engine.say(response_text)
        self.engine.runAndWait()