import logging
import json
from huggingface_hub import InferenceClient

from app.core.config import settings

logger = logging.getLogger(__name__)


class LLMService:
    def __init__(self):
        self.client = InferenceClient(
            model=settings.HF_MODEL_ID,
            token=settings.HF_API_TOKEN
        )

    def analyze_contract_text(self, text: str) -> dict:
        logger.info("Starting Hugging Face AI analysis")

        prompt = f"""
You are a senior legal counsel.

Analyze the following contract text and return ONLY valid JSON
with this exact structure:

{{
  "risk_score": number (0-100),
  "summary": string,
  "high_risk_clauses": array of strings
}}

Rules:
- No explanations
- No markdown
- No extra text

Contract text:
{text}
"""

        response = self.client.text_generation(
            prompt,
            max_new_tokens=512,
            temperature=0.2,
            do_sample=False
        )

        logger.info("Raw AI response received")

        try:
            result = json.loads(response)
        except json.JSONDecodeError:
            logger.error("Invalid JSON returned by AI")
            raise ValueError("AI returned invalid JSON")

        logger.info("AI analysis completed successfully")
        return result
