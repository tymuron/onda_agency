import base64
import os
from openai import OpenAI
import logging

logger = logging.getLogger(__name__)

class VisionAgent:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None
            logger.warning("VisionAgent initialized without API key. Using mock mode.")

    def analyze_image(self, image_data: str):
        """
        Analyzes a base64 encoded image using GPT-4o Vision.
        """
        logger.info("Analyzing uploaded image...")
        
        # Ensure image_data has the correct prefix if missing (though frontend usually sends it)
        if "," in image_data:
            header, encoded = image_data.split(",", 1)
        else:
            encoded = image_data
            header = "data:image/jpeg;base64"

        if self.client:
            try:
                prompt = """
                Look at this image. It is likely a business document (receipt, invoice, spreadsheet) or a UI screenshot.
                
                Extract the key data into a structured JSON format.
                1. "type": Identify the document type (e.g., "Receipt", "Spreadsheet", "Website UI").
                2. "data": Key values extracted (e.g., total amount, date, key metrics).
                3. "insight": One business insight or anomaly detected.
                """
                
                response = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"{header},{encoded}"
                                    },
                                },
                            ],
                        }
                    ],
                    response_format={ "type": "json_object" },
                    max_tokens=500,
                )
                return response.choices[0].message.content
            except Exception as e:
                logger.error(f"Vision analysis failed: {e}")
                return self._get_mock_response()
        else:
            return self._get_mock_response()

    def _get_mock_response(self):
        """Fallback mock response"""
        import json
        return json.dumps({
            "type": "Receipt (Mock Analysis)",
            "data": {
                "Merchant": "Office Supplies Co.",
                "Date": "2023-11-24",
                "Total": "$145.20",
                "Items": ["Printer Paper", "Ink Cartridges"]
            },
            "insight": "This expense category is 15% higher than last month's average."
        })
