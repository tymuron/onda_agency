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
    language: str = "en"

# ... (rest of file)

@app.post("/api/research")
async def run_research(request: ResearchRequest):
    logger.info(f"Research request for: {request.url}")
    try:
        # Run the agent
        result = research_agent.audit_site(request.url)
        return result
    except Exception as e:
        logger.error(f"Error in research agent: {e}")
        # Return a mock response if it fails so the demo doesn't crash
        return research_agent.mock_response()

@app.post("/api/vision")
async def run_vision(request: VisionRequest):
    logger.info("Vision request received")
    try:
        result = vision_agent.analyze_image(request.image)
        return result
    except Exception as e:
        logger.error(f"Error in vision agent: {e}")
        return vision_agent.mock_response()

@app.post("/api/copywriter")
async def run_copywriter(request: CopywriterRequest):
    logger.info(f"Copywriter request: {request.business_name} ({request.language})")
    try:
        result = copywriter_agent.generate_copy(request.business_name, request.description, request.language)
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

# Mount frontend files
# We mount this LAST so it doesn't override the API routes
# Use absolute path to ensure it works regardless of where the script is run from
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
frontend_dir = os.path.join(BASE_DIR, "frontend")

app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
