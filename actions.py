# Custom actions (GPT, Database, API, Voice)
import sqlite3
import openai
import requests
from google.cloud import speech, texttospeech
from rasa_sdk import Action
from rasa_sdk.executor import CollectingDispatcher

# GPT Integration
openai.api_key = "your_openai_api_key"  # Replace with your OpenAI API key

class ActionGPTResponse(Action):
    def name(self) -> str:
        return "action_gpt_response"

    def run(self, dispatcher: CollectingDispatcher, tracker, domain):
        user_query = tracker.latest_message['text']

        # OpenAI GPT API call
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Answer the following: {user_query}",
            max_tokens=150
        )
        gpt_response = response.choices[0].text.strip()

        dispatcher.utter_message(text=gpt_response)
        return []

# SQLite Database FAQ Integration
class ActionFetchFAQ(Action):
    def name(self) -> str:
        return "action_fetch_faq"

    def run(self, dispatcher: CollectingDispatcher, tracker, domain):
        user_query = tracker.latest_message['text']
        connection = sqlite3.connect('faq.db')
        cursor = connection.cursor()
        cursor.execute("SELECT answer FROM faq WHERE question LIKE ?", ('%' + user_query + '%',))
        result = cursor.fetchone()

        if result:
            dispatcher.utter_message(text=result[0])
        else:
            dispatcher.utter_message(text="Sorry, I couldn't find an answer to your question.")
        connection.close()
        return []

# Weather API Integration
class ActionFetchWeather(Action):
    def name(self) -> str:
        return "action_fetch_weather"

    def run(self, dispatcher, tracker, domain):
        location = tracker.get_slot('location')
        api_key = 'your_openweather_api_key'  # Replace with your OpenWeather API key
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            temp = data['main']['temp']
            description = data['weather'][0]['description']
            dispatcher.utter_message(text=f"The temperature in {location} is {temp}°C with {description}.")
        else:
            dispatcher.utter_message(text="I couldn't find the weather for that location.")
        return []

# Voice Interaction (STT and TTS)
class ActionVoiceInteraction(Action):
    def name(self) -> str:
        return "action_voice_interaction"

    def run(self, dispatcher, tracker, domain):
        def speech_to_text(audio_path):
            client = speech.SpeechClient()
            with open(audio_path, 'rb') as audio_file:
                audio = speech.RecognitionAudio(content=audio_file.read())
            config = speech.RecognitionConfig(encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16, sample_rate_hertz=16000, language_code="en-US")
            response = client.recognize(config=config, audio=audio)
            return response.results[0].alternatives[0].transcript

        def text_to_speech(text, output_file_path):
            client = texttospeech.TextToSpeechClient()
            synthesis_input = texttospeech.SynthesisInput(text=text)
            voice = texttospeech.VoiceSelectionParams(language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
            audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
            response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
            with open(output_file_path, "wb") as out:
                out.write(response.audio_content)

        # Example of calling STT and TTS
        user_text = speech_to_text('path_to_audio.wav')
        bot_response = f"You said: {user_text}"
        text_to_speech(bot_response, 'path_to_response.mp3')

        dispatcher.utter_message(text=bot_response)
        return []
