import imaplib
import email
import os
import re
import requests
import logging
from email.header import decode_header
from apscheduler.schedulers.blocking import BlockingScheduler
from dotenv import load_dotenv
from clickup_service import ClickUpService

# Load environment variables
load_dotenv()

clickup = ClickUpService()
LIST_ID = os.getenv("CLICKUP_LIST_ID")

# Configure logging for professional debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EmailParser:
    def __init__(self):
        self.user = os.getenv("GMAIL_USER")
        self.password = os.getenv("GMAIL_APP_PASSWORD")
        self.server = "imap.gmail.com"
        self.connection = None
        # Regex focused on capturing links from posts or reels
        self.url_pattern = r'(https?://(?:www\.)?instagram\.com/(?:reels?|p)/[a-zA-Z0-9_-]+)'
    
    def connect(self):
        """Establishes the IMAP connection."""
        try:
            logger.info("🔌 Connecting to Gmail via IMAP...")
            self.connection = imaplib.IMAP4_SSL(self.server)
            self.connection.login(self.user, self.password)
            self.connection.select("inbox")
            logger.info("✅ Connected to Gmail successfully.")
            return True
        except Exception as e:
            logger.error(f"❌ IMAP Connection Error: {e}")
            return False
    
    def check_connection(self):
        """Checks if the connection is still alive, reconnects if not."""
        try:
            self.connection.noop()
        except Exception:
            logger.warning("⚠️ Connection lost. Attempting to reconnect...")
            self.connect()

    def get_latest_insta_url(self):
        """Searches for UNSEEN emails and extracts the first Instagram URL found."""
        if not self.connection:
            if not self.connect():
                return None
            
        self.check_connection()

        try:
            # Search for UNSEEN (unread) emails
            status, messages = self.connection.search(None, 'UNSEEN')
            
            if status != 'OK' or not messages[0]:
                return None

            logger.info("📩 New email detected! Processing content...")

            email_ids = messages[0].split()
            latest_email_id = email_ids[-1]

            res, msg_data = self.connection.fetch(latest_email_id, '(RFC822)')
            
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    body = ""

                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            if content_type in ["text/plain", "text/html"]:
                                try:
                                    part_body = part.get_payload(decode=True).decode()
                                    body += part_body
                                except:
                                    pass
                    else:
                        body = msg.get_payload(decode=True).decode()

                    # Search for the URL in the body
                    match = re.search(self.url_pattern, body)
                    if match:
                        instagram_url = match.group(0)
                        logger.info(f"🎯 Instagram URL found: {instagram_url}")
                        return instagram_url
            
            logger.warning("⚠️ Email processed, but no Instagram URL was found.")
            return None

        except Exception as e:
            logger.error(f"❌ Error while fetching emails: {e}")
            return None

    def logout(self):
        """Safely closes the connection."""
        if self.connection:
            try:
                self.connection.close()
                self.connection.logout()
                logger.info("🚪 Logged out from Gmail.")
            except:
                pass

# ==========================================
# EXECUTION BLOCK (ORCHESTRATION TRIGGER)
# ==========================================

# Orquestração em automação é o arranjo, sequenciamento e gerenciamento coordenado de múltiplas tarefas automatizadas individuais em um fluxo de trabalho contínuo de ponta a ponta.

# Initialize the global parser instance
parser = EmailParser()


def run_automation_check():
    """
    Checks for new emails and triggers the API (app.py) if a URL is found.
    """
    url = parser.get_latest_insta_url()

    if url:
        logger.info(f"🚀 TRIGGERING PIPELINE FOR: {url}")

        # ---------------------------------------------------------
        # CONFIGURATION FOR RAILWAY vs LOCALHOST
        # ---------------------------------------------------------
        api_endpoint = os.getenv("API_URL", "http://localhost:5500/process-video")
        logger.info(f"✅ Sent for processing URL: {url}")

        try:
            # CORREÇÃO: Enviamos apenas a URL. O app.py vai gerar o task_id lá no final!
            response = requests.post(api_endpoint, json={"url": url}, timeout=30)

            if response.status_code == 200:
                logger.info(f"✅ Pipeline triggered successfully! Server Response: {response.json()}")
            else:
                logger.error(f"⚠️ Orchestrator Error ({response.status_code}): {response.text}")

        except requests.exceptions.ConnectionError:
            logger.error(f"❌ Connection Failed: Could not reach {api_endpoint}. Is the API running?")
        except Exception as e:
            logger.error(f"❌ Unexpected error during trigger: {e}")


if __name__ == "__main__":
    logger.info("⏳ Starting Email Polling Service (Checking every 30 seconds)...")
    
    # 1. Connect to Gmail
    if parser.connect():
        # 2. Setup Scheduler
        scheduler = BlockingScheduler()
        scheduler.add_job(run_automation_check, 'interval', seconds=30)
        
        try:
            # 3. Start the infinite loop
            scheduler.start() 
        except (KeyboardInterrupt, SystemExit):
            logger.info("🛑 Service stopped by user.")
            parser.logout()
    else:
        logger.error("🚫 critical error: Could not connect to Gmail. Check credentials.")