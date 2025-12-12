import base64
import os
from openai import OpenAI
import logging
import json

logger = logging.getLogger(__name__)

class VisionAgent:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None
            logger.warning("VisionAgent initialized without API key. Using mock mode.")

    def analyze_image(self, base64_image: str, language: str = "en"):
        """
        Analyzes a base64 encoded image using GPT-4o Vision.
        """
        logger.info(f"Analyzing uploaded image... (Lang: {language})")
        
        # Ensure image_data has the correct prefix if missing (though frontend usually sends it)
        # Note: This logic was in the previous version but base64_image passed here is usually the full data URL
        # We will pass it directly to OpenAI which handles data:image/jpeg;base64,... correctly if formatted.

        if not self.client:
            return self.mock_response(language)

        try:
            lang_instruction = "Respond in English."
            if language == 'ru':
                lang_instruction = "Respond in Russian (Русский)."
            elif language == 'es':
                lang_instruction = "Respond in Spanish (Español)."

            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": f"Analyze this image as a business document or design asset. {lang_instruction} Return JSON with: 'type' (document type), 'data' (extracted key-value pairs), and 'insight' (one strategic business insight)."},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"{base64_image}"
                                }
                            }
                        ],
                    }
                ],
                max_tokens=500,
                response_format={ "type": "json_object" }
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            logger.error(f"Vision analysis failed: {e}")
            return self.mock_response(language)

    def mock_response(self, language="en"):
        if language == 'ru':
            return {
                "type": "Счет-фактура (Демо)",
                "data": {
                    "Итого": "$4,500.00",
                    "Дата": "2024-03-15",
                    "Поставщик": "Acme Corp"
                },
                "insight": "Обнаружены повторяющиеся расходы. Рекомендуется консолидация поставщиков."
            }
        elif language == 'es':
            return {
                "type": "Factura (Demo)",
                "data": {
                    "Total": "$4,500.00",
                    "Fecha": "2024-03-15",
                    "Proveedor": "Acme Corp"
                },
                "insight": "Gastos recurrentes detectados. Se recomienda la consolidación de proveedores."
            }

        return {
            "type": "Invoice (Demo)",
            "data": {
                "Total": "$4,500.00",
                "Date": "2024-03-15",
                "Vendor": "Acme Corp"
            },
            "insight": "Recurring expense detected. Vendor consolidation recommended."
        }
