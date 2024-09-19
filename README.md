# conversational-ai-bot-
 Conversational AI Bot: Advanced Project with GPT, Voice Support, and Database Integration
 # Conversational AI Bot

## Project Overview
This bot integrates Generative AI (GPT), Voice Support (Speech-to-Text and Text-to-Speech), a SQLite database for FAQs, and an OpenWeather API for real-time weather queries.

## Requirements
- Python 3.8+
- [Rasa](https://rasa.com/)
- OpenAI API Key
- Google Cloud Speech-to-Text and Text-to-Speech enabled
- OpenWeather API Key

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt

2. Set Up Environment Variables
OPENAI_API_KEY: OpenAI API key.
GOOGLE_APPLICATION_CREDENTIALS: Path of Google Cloud credentials JSON file.
3. Run Rasa
bash
Copy code
rasa train
rasa run actions &
rasa run
4. Testing Voice Features
You can test by passing audio files into the speech_to_text function and playing audio responses using text_to_speech.

yaml
Copy code

---

### **How to Run the Bot**

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-repo/conversational-ai-bot.git
   cd conversational-ai-bot
Install Dependencies

bash
Copy code
pip install -r requirements.txt
Configure API Keys Add your OpenAI, Google Cloud, and OpenWeather API keys.

Train and Run Rasa

bash
Copy code
rasa train
rasa run actions &
rasa run
