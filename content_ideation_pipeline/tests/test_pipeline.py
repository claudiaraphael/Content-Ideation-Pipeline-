# test_pipeline.py
import os
import sys

# Add the 'services' folder to the python path so imports work
sys.path.append(os.path.join(os.getcwd(), 'services'))

from services.download_service import download_mp3
from services.transcript_service import transcribe_audio
 

# URL to test (Use a Reel or TikTok URL here)
TEST_URL = input("Paste an Instagram Reel URL to test: ")

def run_test():
    print("--- 1. STARTING DOWNLOAD ---")
    try:
        # Step 1: Download
        mp3_path = download_mp3(TEST_URL)
        print(f"File saved at: {mp3_path}")
        
        # Step 2: Transcribe
        print("\n--- 2. STARTING TRANSCRIPTION ---")
        if os.path.exists(mp3_path):
            transcript = transcribe_audio(mp3_path, language="pt") # or 'en'
            
            print("\n--- 3. FINAL RESULT ---")
            print(transcript)
            
            # Optional: Cleanup
            # os.remove(mp3_path)
            # print("\n(Temporary file deleted)")
        else:
            print("Error: File was not found after download.")

    except Exception as e:
        print(f"Pipeline Failed: {e}")

if __name__ == "__main__":
    run_test()