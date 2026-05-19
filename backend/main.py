from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, HTTPException, Request, Depends, status
from fastapi.responses import (
    FileResponse,
    PlainTextResponse,
    Response,
    HTMLResponse,
    JSONResponse,
)
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import html
import logging
import os
import time
import secrets
import datetime as _dt
from typing import Optional, Dict, Any
from collections import defaultdict
from dotenv import load_dotenv
from pathlib import Path

import analytics as _an

# Canonical site origin (used for SEO tags, sitemap, llms.txt)
SITE_URL = os.getenv("SITE_URL", "https://agencyonda.com")
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

# (path -> filename) for the language-specific homepages.
LANG_HOME = {"en": "index_v5.html", "es": "index_es.html"}

# Canonical page set: (path, filename, lang, page_type)
PAGES = [
    ("/", "index_v5.html", "en", "home"),
    ("/index_es.html", "index_es.html", "es", "home"),
    ("/portfolio.html", "portfolio.html", "en", "portfolio"),
    ("/portfolio_es.html", "portfolio_es.html", "es", "portfolio"),
    ("/process.html", "process.html", "en", "process"),
    ("/process_es.html", "process_es.html", "es", "process"),
    # Industry landing pages + blog (EN + ES; same page_type per slug so the
    # sitemap emits the en/es hreflang cluster).
    ("/web-design-dental-clinics.html", "web-design-dental-clinics.html", "en", "v-dental"),
    ("/web-design-dental-clinics-es.html", "web-design-dental-clinics-es.html", "es", "v-dental"),
    ("/web-design-restaurants.html", "web-design-restaurants.html", "en", "v-restaurants"),
    ("/web-design-restaurants-es.html", "web-design-restaurants-es.html", "es", "v-restaurants"),
    ("/web-design-real-estate.html", "web-design-real-estate.html", "en", "v-realestate"),
    ("/web-design-real-estate-es.html", "web-design-real-estate-es.html", "es", "v-realestate"),
    ("/web-design-aesthetic-clinics.html", "web-design-aesthetic-clinics.html", "en", "v-aesthetic"),
    ("/web-design-aesthetic-clinics-es.html", "web-design-aesthetic-clinics-es.html", "es", "v-aesthetic"),
    ("/web-design-architecture-studios.html", "web-design-architecture-studios.html", "en", "v-architecture"),
    ("/web-design-architecture-studios-es.html", "web-design-architecture-studios-es.html", "es", "v-architecture"),
    ("/blog.html", "blog.html", "en", "blog"),
    ("/blog-es.html", "blog-es.html", "es", "blog"),
    ("/how-much-does-a-website-cost-spain.html", "how-much-does-a-website-cost-spain.html", "en", "post-cost"),
    ("/how-much-does-a-website-cost-spain-es.html", "how-much-does-a-website-cost-spain-es.html", "es", "post-cost"),
    ("/how-to-choose-a-web-designer.html", "how-to-choose-a-web-designer.html", "en", "post-choose"),
    ("/how-to-choose-a-web-designer-es.html", "how-to-choose-a-web-designer-es.html", "es", "post-choose"),
    # Legal pages
    ("/privacy.html", "privacy.html", "en", "legal-privacy"),
    ("/privacy-es.html", "privacy-es.html", "es", "legal-privacy"),
    ("/terms.html", "terms.html", "en", "legal-terms"),
    ("/terms-es.html", "terms-es.html", "es", "legal-terms"),
]

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

# --- Analytics (cookieless) -------------------------------------------------
analytics_db = _an.AnalyticsDB(os.getenv("DATABASE_URL"))
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "")
_basic = HTTPBasic()

# Lightweight in-process per-IP token bucket: ~60 events/minute.
_rl_bucket: Dict[str, list] = defaultdict(lambda: [60.0, time.time()])


def _rate_limited(ip: str) -> bool:
    tokens, last = _rl_bucket[ip]
    now = time.time()
    tokens = min(60.0, tokens + (now - last) * 1.0)  # refill 1/sec, cap 60
    if tokens < 1.0:
        _rl_bucket[ip] = [tokens, now]
        return True
    _rl_bucket[ip] = [tokens - 1.0, now]
    return False


@app.on_event("startup")
async def _startup() -> None:
    await analytics_db.connect()


@app.on_event("shutdown")
async def _shutdown() -> None:
    await analytics_db.close()


def _require_admin(creds: HTTPBasicCredentials = Depends(_basic)) -> bool:
    ok_user = secrets.compare_digest(creds.username, "admin")
    ok_pass = bool(ADMIN_PASSWORD) and secrets.compare_digest(
        creds.password, ADMIN_PASSWORD
    )
    if not (ok_user and ok_pass):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Basic"},
        )
    return True


class TrackEvent(BaseModel):
    event_type: str
    session_id: Optional[str] = None
    page: Optional[str] = None
    lang: Optional[str] = None
    referrer: Optional[str] = None
    scroll_depth: Optional[int] = None
    meta: Optional[Dict[str, Any]] = None


class ContactRequest(BaseModel):
    name: str
    email: str
    phone: Optional[str] = ""
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
        safe_phone = html.escape((request.phone or "").strip())
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
{f'<tr><td style="padding:12px 0; border-bottom:1px solid #e2e8f0;"><span style="font-size:12px; font-weight:600; color:#64748b; text-transform:uppercase; letter-spacing:0.05em;">Phone</span><br><a href="tel:{safe_phone}" style="font-size:16px; color:#2563eb; text-decoration:none;">{safe_phone}</a></td></tr>' if safe_phone else ''}
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
    except HTTPException:
        # Deliberate responses (e.g. 503 when unconfigured) must keep their
        # status/detail and not be masked by the generic 500 below.
        raise
    except Exception as e:
        logger.error(f"Failed to send email notification: {e}")
        raise HTTPException(status_code=500, detail="Failed to send message. Please try again later.")
    
    return {"status": "success", "message": "Message received"}

@app.get("/api/health")
async def health_check():
    """Simple health check to verify backend is running"""
    return {"status": "ok", "service": "onda-backend", "version": "1.0.0"}

# ---------------------------------------------------------------------------
# SEO / GEO  (Phase 1)
# ---------------------------------------------------------------------------

@app.middleware("http")
async def cache_control(request: Request, call_next):
    """Replace the page-level no-cache meta tags with sane HTTP caching."""
    response = await call_next(request)
    path = request.url.path
    if path.startswith("/api/admin") or path.startswith("/api/track") or path == "/admin":
        response.headers["Cache-Control"] = "no-store"
    elif path.startswith("/assets/") or path.endswith(
        (".png", ".jpg", ".jpeg", ".webp", ".svg", ".ico", ".woff2", ".woff", ".css", ".js")
    ):
        response.headers["Cache-Control"] = "public, max-age=31536000, immutable"
    elif path == "/" or path.endswith(".html"):
        response.headers["Cache-Control"] = "public, max-age=300, must-revalidate"
    return response


@app.get("/", include_in_schema=False)
async def root(lang: Optional[str] = None):
    """Serve real English homepage content at the canonical root with HTTP 200.

    This replaces the old client-side JS geo-redirect loader so crawlers and
    AI answer engines index actual content. Language preference is handled as a
    progressive enhancement inside the page (localStorage 'onda_lang_override').
    """
    fname = LANG_HOME.get(lang or "en", LANG_HOME["en"])
    return FileResponse(FRONTEND_DIR / fname, media_type="text/html")


def _hreflang_alternates(page_type: str):
    group = [(lg, p) for (p, _f, lg, t) in PAGES if t == page_type]
    out = []
    for lg, p in group:
        out.append((lg, SITE_URL + ("" if p == "/" else p)))
    en_url = next((u for lg, u in out if lg == "en"), SITE_URL)
    out.append(("x-default", en_url))
    return out


@app.get("/robots.txt", include_in_schema=False)
async def robots_txt():
    body = (
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /admin\n"
        "Disallow: /api/\n\n"
        "# AI answer engines are explicitly welcome (GEO)\n"
        "User-agent: GPTBot\nAllow: /\n\n"
        "User-agent: ClaudeBot\nAllow: /\n\n"
        "User-agent: PerplexityBot\nAllow: /\n\n"
        "User-agent: Google-Extended\nAllow: /\n\n"
        f"Sitemap: {SITE_URL}/sitemap.xml\n"
    )
    return PlainTextResponse(body)


@app.get("/sitemap.xml", include_in_schema=False)
async def sitemap_xml():
    urlset = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ]
    for path, _f, _lg, ptype in PAGES:
        loc = SITE_URL + ("" if path == "/" else path)
        urlset.append("  <url>")
        urlset.append(f"    <loc>{loc}</loc>")
        for hl, href in _hreflang_alternates(ptype):
            urlset.append(
                f'    <xhtml:link rel="alternate" hreflang="{hl}" href="{href}"/>'
            )
        urlset.append("    <changefreq>monthly</changefreq>")
        urlset.append(f"    <priority>{'1.0' if ptype == 'home' else '0.7'}</priority>")
        urlset.append("  </url>")
    urlset.append("</urlset>")
    return Response("\n".join(urlset), media_type="application/xml")


@app.get("/llms.txt", include_in_schema=False)
async def llms_txt():
    body = f"""# Onda

> Onda is a web design studio that builds fast, premium websites, landing pages,
> and starter automations for service businesses that need to look established
> and capture more leads. Based in Spain, working remotely worldwide.

## Facts
- Name: Onda ({SITE_URL.split("//")[-1]})
- Founder: Tymur Chystiakov
- Location: Spain (remote, worldwide clients)
- Languages: English, Spanish
- Services: web design, web development, business automation
- Turnaround: fast delivery (days, not months)

## Pricing
- Launch Page — EUR 690: one-page custom website with WhatsApp / contact capture
- Business Website — EUR 1490: up to 5 pages with SEO, CTA flow, trust sections
- Site + Automation — EUR 2490: full website plus one practical automation

## Key pages
- {SITE_URL}/ — home (English)
- {SITE_URL}/index_es.html — home (Spanish)
- {SITE_URL}/portfolio.html — concept work / portfolio
- {SITE_URL}/process.html — how we work

## Contact
- Website contact form at {SITE_URL}/#contact
"""
    return PlainTextResponse(body)


# ---------------------------------------------------------------------------
# Analytics ingestion + admin dashboard  (Phase 2)
# ---------------------------------------------------------------------------

def _client_ip(request: Request) -> str:
    xff = request.headers.get("x-forwarded-for")
    if xff:
        return xff.split(",")[0].strip()
    return request.client.host if request.client else "0.0.0.0"


@app.post("/api/track", status_code=204)
async def track(ev: TrackEvent, request: Request):
    """Cookieless event ingestion. Never raises to the client."""
    try:
        if ev.event_type not in _an.EVENT_TYPES:
            return Response(status_code=204)
        ip = _client_ip(request)
        if _rate_limited(ip):
            return Response(status_code=204)
        ua = request.headers.get("user-agent", "")
        site_host = SITE_URL.split("//")[-1]
        country = (
            request.headers.get("cf-ipcountry")
            or request.headers.get("x-vercel-ip-country")
            or None
        )
        sd = ev.scroll_depth
        if sd is not None:
            sd = max(0, min(100, int(sd)))
        await analytics_db.insert_event({
            "event_type": ev.event_type,
            "session_id": (ev.session_id or "")[:64] or None,
            "visitor_hash": _an.visitor_hash(ip, ua),
            "page": (ev.page or "")[:256] or None,
            "lang": (ev.lang or "")[:8] or None,
            "referrer_host": _an.referrer_host(ev.referrer or "", site_host),
            "utm_source": _an.utm_source_from(ev.page or "", ev.referrer or ""),
            "device": _an.device_from_ua(ua),
            "country": (country or None),
            "scroll_depth": sd,
            "meta": ev.meta if isinstance(ev.meta, dict) else None,
        })
    except Exception as e:  # analytics must never break a page
        logger.error("track failed: %s", e)
    return Response(status_code=204)


def _date_range(frm: Optional[str], to: Optional[str]):
    today = _dt.datetime.utcnow().date()
    try:
        d1 = _dt.date.fromisoformat(to) if to else today
    except ValueError:
        d1 = today
    try:
        d0 = _dt.date.fromisoformat(frm) if frm else (d1 - _dt.timedelta(days=29))
    except ValueError:
        d0 = d1 - _dt.timedelta(days=29)
    return d0.isoformat(), d1.isoformat()


@app.get("/api/admin/stats")
async def admin_stats(request: Request, _: bool = Depends(_require_admin)):
    frm = request.query_params.get("from")
    to = request.query_params.get("to")
    d0, d1 = _date_range(frm, to)

    funnel = await analytics_db.funnel(d0, d1)
    steps = [
        ("Landing", funnel["landing"]),
        ("Scrolled 50%+", funnel["scrolled"]),
        ("Viewed work", funnel["explored"]),
        ("Saw contact form", funnel["form_view"]),
        ("Submitted form", funnel["form_submit"]),
    ]
    funnel_out = []
    for i, (name, count) in enumerate(steps):
        prev = steps[i - 1][1] if i > 0 else count
        drop = 0.0
        if i > 0 and prev > 0:
            drop = round((1 - count / prev) * 100, 1)
        conv = 0.0
        if steps[0][1] > 0:
            conv = round(count / steps[0][1] * 100, 1)
        funnel_out.append({
            "step": name, "count": count,
            "drop_from_prev_pct": drop, "of_landing_pct": conv,
        })

    return JSONResponse({
        "range": {"from": d0, "to": d1},
        "totals": await analytics_db.totals(d0, d1),
        "funnel": funnel_out,
        "timeseries": await analytics_db.timeseries(d0, d1),
        "top_pages": await analytics_db.breakdown("page", d0, d1),
        "sources": await analytics_db.breakdown("referrer_host", d0, d1),
        "devices": await analytics_db.breakdown("device", d0, d1),
        "countries": await analytics_db.breakdown("country", d0, d1),
        "languages": await analytics_db.breakdown("lang", d0, d1),
        "db_ready": analytics_db.ready,
    })


_ADMIN_HTML = r"""<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex"><title>Onda · Analytics</title>
<style>
:root{--bg:#0a0a0a;--surf:rgba(255,255,255,.03);--bd:rgba(255,255,255,.08);
--tx:#fafafa;--mut:#a1a1aa;--ac:#3B82F6}
*{box-sizing:border-box;margin:0}body{background:var(--bg);color:var(--tx);
font:15px/1.5 system-ui,-apple-system,sans-serif;padding:24px;max-width:1100px;margin:0 auto}
h1{font-size:20px;font-weight:700;letter-spacing:-.02em}
.row{display:flex;gap:12px;flex-wrap:wrap;align-items:center}
.bar{justify-content:space-between;margin-bottom:20px}
input,button{background:var(--surf);color:var(--tx);border:1px solid var(--bd);
border-radius:8px;padding:8px 12px;font:inherit}
button{cursor:pointer}button:hover{border-color:var(--ac)}
.cards{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:18px 0}
.card{background:var(--surf);border:1px solid var(--bd);border-radius:12px;padding:16px}
.card .k{font-size:12px;color:var(--mut);text-transform:uppercase;letter-spacing:.05em}
.card .v{font-size:26px;font-weight:700;margin-top:6px}
.sec{background:var(--surf);border:1px solid var(--bd);border-radius:12px;
padding:18px;margin-bottom:16px}
.sec h2{font-size:13px;color:var(--mut);text-transform:uppercase;
letter-spacing:.06em;margin-bottom:14px}
.frow{display:flex;align-items:center;gap:12px;margin:8px 0}
.fname{width:140px;font-size:13px;color:var(--mut);flex-shrink:0}
.ftrack{flex:1;background:rgba(255,255,255,.05);border-radius:6px;height:30px;
position:relative;overflow:hidden}
.ffill{background:linear-gradient(90deg,var(--ac),#2563eb);height:100%;
border-radius:6px;min-width:2px;transition:width .5s}
.fval{position:absolute;left:10px;top:0;line-height:30px;font-size:13px;font-weight:600}
.fmeta{width:150px;font-size:12px;color:var(--mut);text-align:right;flex-shrink:0}
.drop{color:#f87171}
table{width:100%;border-collapse:collapse;font-size:13px}
td,th{text-align:left;padding:7px 8px;border-bottom:1px solid var(--bd)}
th{color:var(--mut);font-weight:500;font-size:11px;text-transform:uppercase}
td:last-child,th:last-child{text-align:right}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:16px}
svg{width:100%;height:90px;display:block}
.muted{color:var(--mut);font-size:12px}
@media(max-width:760px){.cards{grid-template-columns:repeat(2,1fr)}
.grid2{grid-template-columns:1fr}.fname{width:90px}.fmeta{width:90px}}
</style></head><body>
<div class="row bar"><h1>〰 Onda Analytics</h1>
<div class="row"><input type="date" id="from"><input type="date" id="to">
<button onclick="load()">Refresh</button></div></div>
<div id="warn" class="muted" style="margin-bottom:12px"></div>
<div class="cards" id="cards"></div>
<div class="sec"><h2>Conversion funnel — where people drop off</h2><div id="funnel"></div></div>
<div class="sec"><h2>Unique visitors / day</h2><svg id="ts" viewBox="0 0 600 90" preserveAspectRatio="none"></svg>
<div class="muted" id="tslab"></div></div>
<div class="grid2">
<div class="sec"><h2>Top pages</h2><table id="pages"></table></div>
<div class="sec"><h2>Sources</h2><table id="sources"></table></div>
<div class="sec"><h2>Devices</h2><table id="devices"></table></div>
<div class="sec"><h2>Countries</h2><table id="countries"></table></div>
</div>
<div class="sec"><h2>Languages</h2><table id="languages"></table></div>
<script>
function esc(s){return String(s==null?'':s).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]))}
function tbl(id,rows,h){var t=document.getElementById(id);
if(!rows||!rows.length){t.innerHTML='<tr><td class="muted">No data yet</td></tr>';return}
var html='<tr><th>'+h[0]+'</th><th>'+h[1]+'</th></tr>';
rows.forEach(r=>{html+='<tr><td>'+esc(r.label)+'</td><td>'+r.hits+'</td></tr>'});
t.innerHTML=html}
function load(){
var f=document.getElementById('from').value,t=document.getElementById('to').value;
fetch('/api/admin/stats?from='+f+'&to='+t,{credentials:'same-origin'})
.then(r=>r.json()).then(d=>{
document.getElementById('warn').textContent=d.db_ready?'':'⚠ Analytics database not connected — set DATABASE_URL.';
var T=d.totals||{};
document.getElementById('cards').innerHTML=
card('Unique visitors',T.visitors)+card('Sessions',T.sessions)+
card('Pageviews',T.pageviews)+card('Leads (form submits)',T.leads);
var fn=d.funnel||[],max=Math.max(1,fn.length?fn[0].count:1),h='';
fn.forEach(s=>{var w=Math.round(s.count/max*100);
h+='<div class="frow"><div class="fname">'+esc(s.step)+'</div>'+
'<div class="ftrack"><div class="ffill" style="width:'+w+'%"></div>'+
'<span class="fval">'+s.count+'</span></div>'+
'<div class="fmeta">'+s.of_landing_pct+'% of landing'+
(s.drop_from_prev_pct>0?' · <span class="drop">−'+s.drop_from_prev_pct+'%</span>':'')+
'</div></div>'});
document.getElementById('funnel').innerHTML=h;
var ts=d.timeseries||[],n=ts.length,mx=Math.max(1,...ts.map(x=>x.visitors||0));
var bw=n?600/n:600,sv='';
ts.forEach((x,i)=>{var bh=(x.visitors||0)/mx*80;
sv+='<rect x="'+(i*bw+1)+'" y="'+(85-bh)+'" width="'+Math.max(1,bw-2)+
'" height="'+bh+'" fill="#3B82F6" rx="1"></rect>'});
document.getElementById('ts').innerHTML=sv;
document.getElementById('tslab').textContent=n?(ts[0].day+' → '+ts[n-1].day+
'  ·  peak '+mx+' visitors/day'):'No data yet';
tbl('pages',d.top_pages,['Page','Views']);
tbl('sources',d.sources,['Referrer','Views']);
tbl('devices',d.devices,['Device','Views']);
tbl('countries',d.countries,['Country','Views']);
tbl('languages',d.languages,['Language','Views']);
}).catch(e=>{document.getElementById('warn').textContent='Failed to load stats: '+e})}
function card(k,v){return '<div class="card"><div class="k">'+k+
'</div><div class="v">'+(v==null?0:v)+'</div></div>'}
(function(){var t=new Date(),f=new Date(Date.now()-29*864e5);
document.getElementById('to').value=t.toISOString().slice(0,10);
document.getElementById('from').value=f.toISOString().slice(0,10);load()})();
</script></body></html>"""


@app.get("/admin", response_class=HTMLResponse, include_in_schema=False)
async def admin_page(_: bool = Depends(_require_admin)):
    return HTMLResponse(_ADMIN_HTML)


# Mount frontend files LAST so it never overrides the API/SEO routes above.
app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
