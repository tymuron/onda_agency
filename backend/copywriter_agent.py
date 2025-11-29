import os
from openai import OpenAI
import logging
import json

logger = logging.getLogger(__name__)

class CopywriterAgent:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None
            logger.warning("CopywriterAgent initialized without API key. Using mock mode.")

    def generate_copy(self, business_name: str, description: str, language: str = "en"):
        """
        Generates marketing copy for a business based on its name and description.
        """
        logger.info(f"Generating copy for: {business_name} in {language}")

        if self.client:
            try:
                prompt = f"""
                You are an expert copywriter. Write high-converting website copy for this business.
                
                Business Name: {business_name}
                Description: {description}
                Target Language: {language}

                Return a JSON object with:
                1. "headline": A punchy, benefit-driven H1 headline (max 8 words).
                2. "subheadline": A persuasive H2 subheadline (max 15 words).
                3. "benefits": A list of 3 short, punchy key benefits (max 6 words each).
                4. "cta": A strong Call to Action button text.

                Ensure the response is in {language}.
                """
                
                completion = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are a world-class copywriter."},
                        {"role": "user", "content": prompt}
                    ],
                    response_format={ "type": "json_object" }
                )
                return json.loads(completion.choices[0].message.content)
            except Exception as e:
                logger.error(f"LLM generation failed: {e}")
                return self._get_mock_response(business_name, language)
        else:
            return self._get_mock_response(business_name, language)

    def _get_mock_response(self, business_name, language="en"):
        """Fallback mock response"""
        if language == "ru":
            return {
                "headline": f"Лучшее от {business_name}",
                "subheadline": "Премиальное качество и отличный сервис.",
                "benefits": [
                    "Высокое качество",
                    "Поддержка 24/7",
                    "Гарантия результата"
                ],
                "cta": "Начать сейчас"
            }
        elif language == "es":
             return {
                "headline": f"Lo Mejor de {business_name}",
                "subheadline": "Servicios de calidad premium entregados con excelencia.",
                "benefits": [
                    "Calidad Inigualable",
                    "Soporte 24/7",
                    "Satisfacción Garantizada"
                ],
                "cta": "Empezar Hoy"
            }
        else:
            return {
                "headline": f"Experience the Best of {business_name}",
                "subheadline": "Premium quality services delivered with excellence and care.",
                "benefits": [
                    "Unmatched Quality",
                    "24/7 Customer Support",
                    "Satisfaction Guaranteed"
                ],
                "cta": "Get Started Today"
            }
