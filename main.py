import yaml
from src.llm.llama_cpp import LlamaCpp
from src.core.chat_manager import ChatManager
from src.speech.test_tts import TestTTS
from src.speech.test_stt import TestSTT

def load_config():
    with open("config/config.yaml", "r") as f:
        return yaml.safe_load(f)

def main():
    # Load config
    config = load_config()

    # Initialize components
    llm = LlamaCpp(
        server_url=config["llm"]["server_url"],
        max_tokens=config["llm"]["max_tokens"],
        temperature=config["llm"]["temperature"]
    )
    
    # Optional: Initialize test speech components
    tts = TestTTS()
    stt = TestSTT()

    # Initialize chat manager with all components
    chat_manager = ChatManager(llm, tts, stt)

    print("Chatbot initialized with test speech components. Type 'quit' to exit.")
    print("Type 'voice' to test STT or 'text' for keyboard input.")
    
    try:
        while True:
            # Get input mode
            mode = input("\nInput mode (voice/text/quit): ").strip().lower()
            
            if mode == 'quit':
                break
            
            if mode == 'voice':
                # Use STT
                print("Simulating voice input...")
                transcribed = stt.transcribe_audio()
                print(f"Transcribed: {transcribed}")
                response = chat_manager.get_response(transcribed)
            elif mode == 'text':
                # Get text input
                user_input = input("\nYou: ").strip()
                if user_input:
                    response = chat_manager.get_response(user_input)
            else:
                print("Invalid mode. Please choose 'voice', 'text', or 'quit'")
                continue
                
            # Show response
            print(f"\nAssistant: {response['text']}")
            if 'audio_path' in response:
                print(f"Audio response generated at: {response['audio_path']}")

    except KeyboardInterrupt:
        print("\nExiting...")

if __name__ == "__main__":
    main()