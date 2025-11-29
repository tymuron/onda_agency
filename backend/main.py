from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from research_agent import ResearchAgent
from vision_agent import VisionAgent
from copywriter_agent import CopywriterAgent
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ... (imports remain same)

app = FastAPI()

# CORS Configuration (Keep as is)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Agents
research_agent = ResearchAgent(api_key=os.getenv("OPENAI_API_KEY"))
vision_agent = VisionAgent(api_key=os.getenv("OPENAI_API_KEY"))
copywriter_agent = CopywriterAgent(api_key=os.getenv("OPENAI_API_KEY"))

class ContactRequest(BaseModel):
    name: str
    email: str
    type: str
    message: str

class ResearchRequest(BaseModel):
    url: str

class VisionRequest(BaseModel):
    image: str # Base64 string

class CopywriterRequest(BaseModel):
    business_name: str
    description: str

# Serve Static Files
# Mount the 'frontend' directory to serve static assets (css, js, images)
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
app.mount("/static", StaticFiles(directory=frontend_path), name="static")
app.mount("/assets", StaticFiles(directory=os.path.join(frontend_path, "assets")), name="assets")

# Serve HTML files directly from root
@app.get("/")
async def read_root():
    return FileResponse(os.path.join(frontend_path, "index.html"))

@app.get("/{filename}.html")
async def read_html(filename: str):
    file_path = os.path.join(frontend_path, f"{filename}.html")
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="File not found")

@app.get("/portfolio/{filename}.html")
async def read_portfolio_html(filename: str):
    file_path = os.path.join(frontend_path, "portfolio", f"{filename}.html")
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="File not found")

# Serve other static files at root level if needed (like logo.png)
@app.get("/{filename}.png")
async def read_image(filename: str):
    file_path = os.path.join(frontend_path, f"{filename}.png")
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="File not found")

@app.post("/api/research")
async def research_site(request: ResearchRequest):
    logger.info(f"Research request for: {request.url}")
    try:
        result = research_agent.analyze_url(request.url)
        # If result is a string (JSON string from mock or LLM), parse it to ensure valid JSON response
        import json
        if isinstance(result, str):
            try:
                return json.loads(result)
            except:
                return {"raw_result": result}
        return result
    except Exception as e:
        logger.error(f"Error in research: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/vision")
async def analyze_vision(request: VisionRequest):
    logger.info(f"Vision request received")
    try:
        result = vision_agent.analyze_image(request.image)
        import json
        if isinstance(result, str):
            try:
                return json.loads(result)
            except:
                return {"raw_result": result}
        return result
    except Exception as e:
        logger.error(f"Error in vision: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/copywriter")
async def run_copywriter(request: CopywriterRequest):
    logger.info(f"Copywriter request: {request.business_name}")
    try:
        result = copywriter_agent.generate_copy(request.business_name, request.description)
        return result
    except Exception as e:
        logger.error(f"Error in copywriter: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/contact")
async def contact(request: ContactRequest):
    logger.info(f"Contact form submission: {request.name} ({request.email})")
    
    # Send email notification using Resend
    try:
        import resend
        resend.api_key = os.getenv("RESEND_API_KEY")
        notification_email = os.getenv("NOTIFICATION_EMAIL")
        
        if resend.api_key and notification_email:
            # Send notification to you
            resend.Emails.send({
                "from": "Onda Website <onboarding@resend.dev>",
                "to": notification_email,
                "subject": f"New Contact Form Submission from {request.name}",
                "html": f"""
                <h2>New Contact Form Submission</h2>
                <p><strong>Name:</strong> {request.name}</p>
                <p><strong>Email:</strong> {request.email}</p>
                <p><strong>Looking to build:</strong> {request.type}</p>
                <p><strong>Message:</strong></p>
                <p>{request.message}</p>
                <hr>
                <p><em>Reply directly to {request.email} to get in touch with them!</em></p>
                """
            })
            logger.info(f"Email notification sent to {notification_email}")
    except Exception as e:
        logger.error(f"Failed to send email notification: {e}")
        # Continue anyway - don't fail the request if email fails
    
    return {"status": "success", "message": "Message received"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
