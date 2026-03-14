from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
import os
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ContactRequest(BaseModel):
    name: str
    email: str
    type: str
    message: str


@app.post("/api/contact")
async def contact(request: ContactRequest):
    logger.info(f"Contact form submission: {request.name} ({request.email})")
    
    # Send email notification using Resend
    try:
        import resend
        resend.api_key = os.getenv("RESEND_API_KEY")
        notification_email = os.getenv("NOTIFICATION_EMAIL")
        
        if not resend.api_key or not notification_email:
            logger.error("Contact form is not configured. Missing RESEND_API_KEY or NOTIFICATION_EMAIL.")
            raise HTTPException(status_code=503, detail="Contact form is temporarily unavailable.")

        # Send notification to you
        resend.Emails.send({
            "from": "Onda Website <onboarding@resend.dev>",
            "to": notification_email,
            "reply_to": request.email,
            "subject": f"New Contact Form Submission from {request.name}",
            "html": f"""
            <h2>New Contact Form Submission</h2>
            <p><strong>Name:</strong> {request.name}</p>
            <p><strong>Email:</strong> {request.email}</p>
            <p><strong>Looking to build:</strong> {request.type}</p>
            <p><strong>Message:</strong></p>
            <p>{request.message}</p>
            <hr>
            <p><em>Reply directly to {request.email} to get in touch with them.</em></p>
            """
        })
        logger.info(f"Email notification sent to {notification_email}")
    except Exception as e:
        logger.error(f"Failed to send email notification: {e}")
        raise HTTPException(status_code=500, detail="Failed to send message. Please try again later.")
    
    return {"status": "success", "message": "Message received"}

@app.get("/api/health")
async def health_check():
    """Simple health check to verify backend is running"""
    return {"status": "ok", "service": "onda-backend", "version": "1.0.0"}

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
