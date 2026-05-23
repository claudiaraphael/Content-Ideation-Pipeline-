import os
import logging
from dotenv import load_dotenv  
from groq import Groq  

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AnalystAgent:
    def __init__(self):
        # Usamos a mesma chave da transcrição
        self.api_key = os.environ.get("GROQ_API_KEY")
        
        if not self.api_key:
            logger.error("GROQ_API_KEY is missing.")            
            raise ValueError("❌ GROQ_API_KEY not found.")
        
        self.client = Groq(api_key=self.api_key)
        # Modelo Llama 3 (Rápido, inteligente e estável)
        self.model_name = "llama-3.3-70b-versatile"

    def analyze_transcript(self, transcript_text: str) -> str:
        if not transcript_text.strip():
            return "⚠️ Error: Provided transcript is empty."

        logger.info("🧠 Starting strategic analysis with Groq (Llama 3)...")
        
        prompt = f"""
        ACT AS A SENIOR GROWTH MARKETING STRATEGIST.
        Analyze the video transcript and generate a high-impact report.
        Focus on virality, retention, and content repurposing.

        TRANSCRIPT: "{transcript_text}"

        OUTPUT FORMAT (Markdown):
        # 📊 Video Growth Audit
        ## 1. The Scorecard (0-10)
        * **Hook Strength:** [Score]/10 - *Why?*
        * **Value Delivery:** [Score]/10 - *Did it solve a problem?*
        * **Predicted Virality:** [Score]/10 - *Based on trend/relatability.*

        ## 2. Key Insights
        * **Core Hook Used:** * **Emotional Triggers:** ## 3. ♻️ Repurposing Ideas
        *Draft 3 content ideas based on this video.*
        """

        try:
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a marketing expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            return completion.choices[0].message.content
                 
        except Exception as e:
            logger.error(f"❌ Groq Analysis Error: {e}")
            return f"⚠️ Analysis failed via API. Error: {str(e)}"

# TESTING BLOCK
if __name__ == "__main__":
    mock_transcript = "Stop wasting money! Use automation to triple your sales."
    try:
        agent = AnalystAgent()
        print(agent.analyze_transcript(mock_transcript))
    except Exception as e:
        print(f"Error: {e}")