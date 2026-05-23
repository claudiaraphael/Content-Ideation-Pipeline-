import clickup
from flask import Flask, request, jsonify
import os
import logging
from dotenv import load_dotenv

# Service imports
from services.download_service import download_mp3
from services.transcript_service import transcribe_audio
from services.marketing_analysis import AnalystAgent 
from services.clickup_service import ClickUpService

# Logging Configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

app = Flask(__name__)

# Service Initialization
try:
    clickup_service = ClickUpService()
    analyst_agent = AnalystAgent() 
    logger.info("✅ External services initialized successfully.")
except Exception as e:
    logger.error(f"❌ Error initializing services: {e}")


@app.route("/")
def home():
    return jsonify({
        "status": "online", 
        "message": "Content Ideation Pipeline is Live 🚀"
    })

@app.route("/process-video", methods=["POST"])
def process_video():
    
    """
    Main Orchestrator:
    1. Download (yt-dlp)
    2. Transcription 
    3. Marketing Analysis 
    4. Update Task 
    """
    file_path = None
        
    data = request.json
    url = data.get("url")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    logger.info(f"🚀 Starting processing for URL: {url}")

    try:
        # --- STEP 1: Download Audio ---
        logger.info("⬇️ Downloading audio...")
        file_path = download_mp3(url)
        
        if not file_path or not os.path.exists(file_path):
            raise FileNotFoundError("Failed to download the audio file.")

        # --- STEP 2: Transcription ---
        logger.info("🎙️ Transcribing audio...")
        # Note: Set language to 'en' since the client is in the US
        transcript = transcribe_audio(file_path, language="en") 
        
        if not transcript or "Error" in transcript:
            raise Exception(f"Transcription failed: {transcript}")

        # --- STEP 3: Marketing Analysis ---
        logger.info("🧠 Generating marketing analysis...")
        analysis_report = analyst_agent.analyze_transcript(transcript)

        # --- STEP 4: CREATE TASK
        LIST_ID = os.getenv("CLICKUP_LIST_ID")
        task_id = clickup_service.create_task(list_id=LIST_ID, title=f"Analysis: {url}", description_markdown=analysis_report)

        logger.info("📝 Creating ClickUp Task with Markdown Report...")

        if task_id:
            logger.info(f"✅ Task created successfully! ID: {task_id}")

        # --- CLEANUP ---
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"🗑️ Temporary file removed: {file_path}")

        return jsonify({
            "status": "success",
            "task_id": task_id,
            "message": "Automation pipeline completed successfully!"
        })

    except Exception as e:
        logger.error(f"❌ CRITICAL ERROR in pipeline: {str(e)}")
        
        # Alert ClickUp about the failure if a task exists
        if task_id:
            error_msg = f"❌ **AUTOMATION FAILURE**\n\nAn error occurred during processing:\n`{str(e)}`"
            try:
                clickup_service.update_task(task_id, error_msg)
            except:
                pass

        # Cleanup on failure
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass

        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":

    DEBUG_MODE = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    app.run(host="0.0.0.0", port=5500, debug=DEBUG_MODE)