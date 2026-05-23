import os
import requests
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ClickUpService:
    """
    Service to interact with ClickUp API.
    Can fetch task details and post updates/comments.
    """

    def __init__(self):
        """Initializes the client with API token from environment."""
        self.api_key = os.environ.get("CLICKUP_API_KEY")
        
        if not self.api_key:
            logger.error("❌ CLICKUP_API_KEY is missing from .env file.")
            raise ValueError("CLICKUP_API_KEY not found.")

        self.base_url = "https://api.clickup.com/api/v2"
        self.headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json"
        }

    def create_task(self, list_id: str, title: str, description_markdown: str = None) -> str:
        """Cria uma tarefa com a descricao em markdown e retorna o ID dela."""
        url = f"{self.base_url}/list/{list_id}/task"
        payload = {
            "name": title,
        }

        if description_markdown:
            payload["markdown_description"] = description_markdown

        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json().get("id")
        except Exception as e:
            logger.error(f"❌ Falha ao criar tarefa: {e}")
            return None
        
    def get_task(self, task_id: str) -> dict:
        """
        Fetches task details from ClickUp.
        """
        url = f"{self.base_url}/task/{task_id}"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()  # Raises error for 400/404/500 codes
            
            task_data = response.json()
            logger.info(f"✅ Successfully fetched task: {task_data.get('name')}")
            return task_data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error fetching task {task_id}: {e}")
            return {}

    def update_task(self, task_id: str, analysis_text: str, new_status: str = None):
        """
        1. Posts the analysis as a comment.
        2. Updates the task description interpreting Markdown.
        3. (Optional) Updates the task status.
        """
        # Part A: Post the Description
        url = f"{self.base_url}/task/{task_id}/"
        
        # Garante que o texto seja string
        if not analysis_text:
            analysis_text = "⚠️ No analysis generated."

        payload = {
            "markdown_content": analysis_text
        }

        if new_status:
            payload["status"] = new_status

        try:
            logger.info(f"📝 Updating description for task {task_id}...")
            
            # IMPORTANTE: PUT para atualizar a tarefa
            res = requests.put(url, headers=self.headers, json=payload)
            
            if not res.ok:
                logger.error(f"❌ ClickUp API Error: {res.text}")
                res.raise_for_status()

            logger.info(f"✅ Task description updated successfully.")
     
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error updating task {task_id}: {e}")
            raise e

# --- TESTING BLOCK ---
if __name__ == "__main__":
    # Replace this with a REAL task ID from your ClickUp (look at the URL)
    
    service = ClickUpService()
    
    # 1. Test Fetching
    task = service.get_task(TEST_TASK_ID)
    print(f"Task Name: {task.get('name')}")
    print(f"Description: {task.get('description')}")

    # 2. Test Updating (Uncomment to test writing a comment)
    # service.update_task(TEST_TASK_ID, "This is a test comment from Python!")