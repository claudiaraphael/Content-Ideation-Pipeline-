import os
import logging
from dotenv import load_dotenv  # Loads variables from .env file
from groq import Groq

# 1. Logger Configuration (Crucial for automation/debugging)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 2. Load environment variables
load_dotenv()

api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    logger.error("CRITICAL ERROR: GROQ_API_KEY not found in environment variables.")
    raise ValueError("API Key is missing")

client = Groq(api_key=api_key)

WHISPER_MODEL = "whisper-large-v3-turbo"
LLM_MODEL = "llama-3.3-70b-versatile"

def transcribe_audio(file_path: str, language: str = "pt") -> str:
    """
    Transcribes audio using Whisper and refines the text using Llama.
    
    Args:
        file_path (str): Path to the audio file.
        language (str): Language code (default: 'pt' for Portuguese, use 'en' for English).
        
    Returns:
        str: The refined transcript or an error message.
    """
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return f"Error: File {file_path} not found."

    logger.info(f"Starting transcription for: {file_path}")

    try:
        # Step A: Raw Transcription
        # Best Practice: Open file and pass the object directly to avoid loading large files into RAM
        with open(file_path, "rb") as file:
            logger.info("Sending audio to Whisper...")
            transcription = client.audio.transcriptions.create(
                file=(os.path.basename(file_path), file), # Pass file pointer
                model=WHISPER_MODEL,
                response_format="json",
                language=language
            )
        
        raw_text = transcription.text
        logger.info(f"Raw transcription completed ({len(raw_text)} chars).")

        # Step B: Refinement
        logger.info("Starting text refinement with Llama...")
        refined_transcript = refine_text_with_llm(raw_text)
        
        logger.info("Process finished successfully.")
        return refined_transcript

    except Exception as e:
        # This captures the full stack trace for debugging
        logger.exception("Failure during transcription process.")
        return f"An error occurred: {str(e)}"

def refine_text_with_llm(text: str) -> str:
    """
    Uses Llama to clean up the transcript, add punctuation, and improve flow.
    """
    if not text:
        return ""

    prompt = f"""
    You are an expert transcription editor. 
    Below is a raw transcript from an automation pipeline. 
    Please:
    1. Correct any obvious spelling errors.
    2. Add proper punctuation and paragraph breaks.
    3. Maintain the original tone and meaning.
    
    Raw Transcript:
    {text}
    """

    completion = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": "You format raw transcripts into clean, professional text."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1
    )
    
    return completion.choices[0].message.content

if __name__ == "__main__":

    from download_service import download_mp3
    

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
                transcript = transcribe_audio(mp3_path, language="en") # or 'en'
                
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