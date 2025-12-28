import logging
import json
# from huggingface_hub import InferenceClient  # ⛔ Disabled temporarily

from app.core.config import settings

logger = logging.getLogger(__name__)


class LLMService:
    def __init__(self):
        """
        In production, this will initialize the Hugging Face client.

        Temporarily disabled because:
        - Free HF Inference API does not reliably support instruct/chat models
        - Causes runtime failures (model_not_supported / StopIteration)
        """

        # 🔴 REAL CLIENT (enable when HF/OpenAI model is stable)
        # self.client = InferenceClient(
        #     model=settings.HF_MODEL_ID,
        #     token=settings.HF_API_TOKEN,
        # )

        pass  # Mock mode does not need a client

    def analyze_contract_text(self, text: str) -> dict:
        """
        Analyze contract text and return structured risk data.

        TEMPORARY MOCK IMPLEMENTATION
        ------------------------------
        This mock allows:
        - Background tasks to complete
        - DB writes to succeed
        - API to remain non-blocking
        - System to be demoed and tested

        Swap this with real LLM call when provider is available.
        """

        logger.info("Running contract analysis (MOCK MODE)")

        # ✅ MOCK RESPONSE (deterministic, stable)
        return {
            "risk_score": 42,
            "summary": (
                "The contract contains standard clauses with moderate risk. "
                "Termination and liability provisions should be reviewed."
            ),
            "high_risk_clauses": [
                "Termination without notice",
                "Unlimited liability",
            ],
        }

        # 🔴 REAL IMPLEMENTATION (KEEP FOR LATER)
        # ---------------------------------------
        # prompt = f"""
        # You are a senior legal counsel.
        #
        # Analyze the following contract and return ONLY valid JSON
        # with this exact structure:
        #
        # {{
        #   "risk_score": number,
        #   "summary": string,
        #   "high_risk_clauses": array of strings
        # }}
        #
        # Rules:
        # - No explanations
        # - No markdown
        # - No extra text
        #
        # Contract text:
        # {text}
        # """
        #
        # response = self.client.text_generation(
        #     prompt,
        #     max_new_tokens=512,
        #     temperature=0.2,
        #     do_sample=False,
        # )
        #
        # logger.info("Raw AI response received")
        #
        # try:
        #     result = json.loads(response)
        # except json.JSONDecodeError:
        #     logger.error(f"Invalid JSON returned by AI:\n{response}")
        #     raise ValueError("AI returned invalid JSON")
        #
        # logger.info("AI analysis completed successfully")
        # return result
