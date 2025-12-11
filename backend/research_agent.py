import requests
from bs4 import BeautifulSoup
import os
from openai import OpenAI
import logging

logger = logging.getLogger(__name__)

class ResearchAgent:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None
            logger.warning("ResearchAgent initialized without API key. Using mock mode.")

    def analyze_url(self, url: str):
        """
        Scrapes the given URL and uses LLM to provide marketing improvements.
        """
        logger.info(f"Researching URL: {url}")
        
        # 1. Scrape Content
        try:
            # Add headers to mimic a browser
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            if not url.startswith('http'):
                url = 'https://' + url
                
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract key elements
            title = soup.title.string if soup.title else "No title found"
            meta_desc = ""
            meta_tag = soup.find('meta', attrs={'name': 'description'})
            if meta_tag:
                meta_desc = meta_tag.get('content', '')
                
            # Get main text content (limit to first 2000 chars to save tokens)
            text_content = soup.get_text(separator=' ', strip=True)[:2000]
            
            scraped_data = {
                "title": title,
                "description": meta_desc,
                "content_snippet": text_content
            }
            
        except Exception as e:
            logger.error(f"Scraping failed: {e}")
            return {
                "error": f"Could not access {url}. Please check the URL and try again.",
                "details": str(e)
            }

        # 2. Analyze with LLM (or Mock)
        if self.client:
            try:
                prompt = f"""
                Analyze this website content for a business owner.
                URL: {url}
                Title: {scraped_data['title']}
                Description: {scraped_data['description']}
                Content Snippet: {scraped_data['content_snippet']}

                Provide a structured critique in JSON format with:
                1. "score": A score from 0-100 based on CRO (Conversion Rate Optimization).
                2. "summary": A 1-sentence summary of what the site does.
                3. "improvements": A list of 3 specific, actionable marketing improvements.
                4. "quick_win": One specific automation idea for this business.
                """
                
                completion = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are a world-class digital marketing expert and automation consultant."},
                        {"role": "user", "content": prompt}
                    ],
                    response_format={ "type": "json_object" }
                )
                return completion.choices[0].message.content
            except Exception as e:
                logger.error(f"LLM analysis failed: {e}")
                return self.mock_response(url)
        else:
            return self.mock_response(url)

    def mock_response(self, url="example.com"):
        """Fallback mock response for demos without API keys"""
        import json
        return json.dumps({
            "score": 72,
            "summary": f"A business website at {url} that could use better value propositions.",
            "improvements": [
                "Add a clear Call-to-Action (CTA) above the fold.",
                "Improve page load speed (images seem large).",
                "Add social proof or testimonials to build trust."
            ],
            "quick_win": "Implement an automated chatbot to capture leads 24/7."
        })
