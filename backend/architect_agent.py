import os
import openai
from typing import Dict, Any

class ArchitectAgent:
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key) if api_key else None

    def generate_ui(self, prompt: str) -> Dict[str, Any]:
        """
        Generates HTML/Tailwind code based on a user prompt.
        """
        if not self.client:
            return {
                "html": f"""
                <div class="p-8 text-center border-2 border-dashed border-slate-700 rounded-xl">
                    <h3 class="text-xl font-bold text-white mb-2">Mock Mode: Architect Agent</h3>
                    <p class="text-slate-400 mb-4">I would generate a UI for: "{prompt}"</p>
                    <div class="bg-slate-800 p-4 rounded text-left font-mono text-xs text-green-400">
                        &lt;div class="bg-white p-6 rounded-lg shadow-lg"&gt;<br>
                        &nbsp;&nbsp;&lt;h1 class="text-2xl font-bold"&gt;Hello World&lt;/h1&gt;<br>
                        &lt;/div&gt;
                    </div>
                </div>
                """
            }

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": """You are an expert Frontend Engineer and UI Designer. 
                    Your task is to generate production-ready HTML code using Tailwind CSS based on the user's request.
                    
                    RULES:
                    1. Return ONLY the raw HTML code. Do not include markdown backticks (```html) or explanations.
                    2. Use Tailwind CSS for all styling.
                    3. Make it look modern, premium, and beautiful (glassmorphism, gradients, rounded corners).
                    4. The code will be injected into a small preview container, so ensure it is RESPONSIVE.
                       - Use `w-full` and `max-w-full` to prevent overflow.
                       - Use `flex-wrap` or `grid-cols-1` on small screens so it fits narrow spaces.
                       - Avoid fixed widths (like `w-[800px]`).
                    5. Use Lucide icons (<i> tags with data-lucide attribute) where appropriate.
                    6. Ensure text contrast is good (assume a dark background container, but you can set your own background).
                    """},
                    {"role": "user", "content": f"Build this UI component: {prompt}"}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            html_content = response.choices[0].message.content.strip()
            
            # Cleanup markdown if present
            if html_content.startswith("```html"):
                html_content = html_content[7:]
            if html_content.startswith("```"):
                html_content = html_content[3:]
            if html_content.endswith("```"):
                html_content = html_content[:-3]
                
            return {"html": html_content}

        except Exception as e:
            return {"error": str(e)}
