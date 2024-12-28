import os
import yaml
from dotenv import load_dotenv
from src.core.chat_manager import ChatManager
from src.llm.llama_cpp import LlamaCpp
from src.speech.text_to_speech import TextToSpeech
from src.speech.speech_to_text import SpeechToText

def load_config():
    with open("config/config.yaml", "r") as f:
        return yaml.safe_load(f)

def main():
    # Load environment variables and config
    load_dotenv()
    config = load_config()

    # Initialize components
    llm = LlamaCpp(
        server_url=config["llm"]["server_url"],
        max_tokens=config["llm"]["max_tokens"],
        temperature=config["llm"]["temperature"]
    )

    tts = TextToSpeech(
        azure_key=os.getenv("AZURE_SPEECH_KEY"),
        azure_region=config["speech"]["tts"]["region"],
        voice_name=config["speech"]["tts"]["voice_name"]
    )

    stt = SpeechToText(
        azure_key=os.getenv("AZURE_SPEECH_KEY"),
        azure_region=config["speech"]["stt"]["region"]
    )

    # Initialize chat manager
    chat_manager = ChatManager(llm, tts, stt)

    print("Voice chatbot initialized. Press Ctrl+C to exit.")
    
    try:
        while True:
            # Get voice input
            user_message = chat_manager.process_voice_input()
            print(f"You said: {user_message.content}")

            # Generate and play response
            response = chat_manager.generate_response(user_message)
            print(f"Assistant: {response.content}")
            
            # Audio response is automatically played by Azure SDK

    except KeyboardInterrupt:
        print("\nExiting...")

if __name__ == "__main__":
    main()