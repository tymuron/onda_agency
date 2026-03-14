from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import html
import logging
import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env from backend/ so it works when run from project root (e.g. python backend/main.py)
_env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=_env_path)
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

        # Escape user input for safe HTML
        safe_name = html.escape(request.name)
        safe_email = html.escape(request.email)
        safe_type = html.escape(request.type)
        safe_message = html.escape(request.message).replace("\n", "<br>")

        # Send notification to you (styled for email clients)
        resend.Emails.send({
            "from": "Onda Website <onboarding@resend.dev>",
            "to": notification_email,
            "reply_to": request.email,
            "subject": f"New lead: {request.name} · {request.type}",
            "html": f"""
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
<body style="margin:0; padding:0; font-family:'Segoe UI',system-ui,-apple-system,sans-serif; background:#f1f5f9; color:#0f172a;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#f1f5f9; padding:32px 16px;">
<tr><td align="center">
<table width="100%" cellpadding="0" cellspacing="0" style="max-width:560px; background:#fff; border-radius:16px; overflow:hidden; box-shadow:0 4px 24px rgba(15,23,42,0.08);">
<tr><td style="background:linear-gradient(135deg,#2563eb,#1d4ed8); padding:24px 28px;">
<div style="display:flex; align-items:center; gap:10px;">
<span style="font-size:24px;">〰</span>
<span style="font-weight:700; font-size:18px; color:#fff; letter-spacing:-0.02em;">ONDA</span>
</div>
<p style="margin:8px 0 0; font-size:14px; color:rgba(255,255,255,0.9);">New contact form submission</p>
</td></tr>
<tr><td style="padding:28px;">
<table width="100%" cellpadding="0" cellspacing="0">
<tr><td style="padding:12px 0; border-bottom:1px solid #e2e8f0;"><span style="font-size:12px; font-weight:600; color:#64748b; text-transform:uppercase; letter-spacing:0.05em;">Name</span><br><span style="font-size:16px; font-weight:500; color:#0f172a;">{safe_name}</span></td></tr>
<tr><td style="padding:12px 0; border-bottom:1px solid #e2e8f0;"><span style="font-size:12px; font-weight:600; color:#64748b; text-transform:uppercase; letter-spacing:0.05em;">Email</span><br><a href="mailto:{safe_email}" style="font-size:16px; color:#2563eb; text-decoration:none;">{safe_email}</a></td></tr>
<tr><td style="padding:12px 0; border-bottom:1px solid #e2e8f0;"><span style="font-size:12px; font-weight:600; color:#64748b; text-transform:uppercase; letter-spacing:0.05em;">Interest</span><br><span style="font-size:16px; color:#0f172a;">{safe_type}</span></td></tr>
<tr><td style="padding:12px 0;"><span style="font-size:12px; font-weight:600; color:#64748b; text-transform:uppercase; letter-spacing:0.05em;">Message</span><br><div style="font-size:15px; line-height:1.6; color:#334155; margin-top:8px;">{safe_message}</div></td></tr>
</table>
<div style="margin-top:24px; padding-top:20px; border-top:1px solid #e2e8f0;">
<a href="mailto:{safe_email}?subject=Re: Your Onda inquiry" style="display:inline-block; background:#2563eb; color:#fff; padding:12px 24px; border-radius:9999px; font-weight:600; font-size:14px; text-decoration:none;">Reply to {safe_name}</a>
</div>
</td></tr>
</table>
</td></tr>
</table>
</body>
</html>
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
