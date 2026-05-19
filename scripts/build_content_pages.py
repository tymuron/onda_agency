#!/usr/bin/env python3
"""Generate the vertical (industry) landing pages + blog, EN and ES.

One shared structural template; every page's body is hand-written and
segment-specific (problem / what-we-build / FAQ / proof), and ES is
transcreated (Spain register, agency voice), NOT machine-translated — so each
page is genuinely unique and useful, not a doorway/templated name-swap (Google
spam policy), and EN/ES are a valid hreflang cluster, not duplicates.

Every page ships with self-canonical + full hreflang cluster, JSON-LD
(Service/Article + FAQPage + BreadcrumbList), the analytics tracker, and the
lean brand CSS + built Tailwind. Idempotent: overwrites the generated files.

Run:  python3 scripts/build_content_pages.py
"""
import html
import json
from pathlib import Path

FRONTEND = Path(__file__).resolve().parent.parent / "frontend"
SITE = "https://agencyonda.com"
WA_EN = ("https://wa.me/34607864285?text=Hi%2C%20I%20saw%20agencyonda.com%20"
         "and%20I%E2%80%99m%20interested%20in%20a%20project.")
WA_ES = ("https://wa.me/34607864285?text=Hola%2C%20vi%20agencyonda.com%20y%20"
         "me%20interesa%20un%20proyecto.")

T = {  # UI strings per language
    "en": {"work": "Work", "blog": "Blog", "pricing": "Pricing",
           "quote": "Get a quote", "wa": "Message us on WhatsApp",
           "home": "Home", "industry": "Industry", "faq": "FAQ",
           "wa_url": WA_EN, "studio": "Web design studio · Spain · works "
           "across Europe", "contact": "/#contact",
           "fixed": "Fixed price, agreed up front. Most sites go live in "
           "about three weeks.", "see": "See a", "concept": "concept we "
           "built →", "common": "websites — common questions",
           "blog_h1": "Plain answers for small-business owners",
           "blog_lead": "No jargon. What a website should cost, how to "
           "choose who builds it, and what actually gets you more clients.",
           "blog_title": "Blog — web design for small businesses in "
           "Spain | Onda", "blog_desc": "Plain-English guides on website "
           "cost, choosing a web designer and getting more clients — "
           "for small businesses in Spain."},
    "es": {"work": "Proyectos", "blog": "Blog", "pricing": "Precios",
           "quote": "Pedir presupuesto", "wa": "Escríbenos por WhatsApp",
           "home": "Inicio", "industry": "Sector", "faq": "Preguntas",
           "wa_url": WA_ES, "studio": "Estudio de diseño web · España "
           "· trabajamos en toda Europa", "contact": "/index_es.html#contact",
           "fixed": "Precio cerrado, acordado de antemano. La mayoría de "
           "webs se publican en unas tres semanas.", "see": "Mira un",
           "concept": "concepto que hicimos →",
           "common": "— preguntas frecuentes",
           "blog_h1": "Respuestas claras para dueños de negocio",
           "blog_lead": "Sin jerga. Cuánto debería costar una web, "
           "cómo elegir quién la hace y qué te consigue de "
           "verdad más clientes.",
           "blog_title": "Blog — diseño web para pequeños "
           "negocios en España | Onda", "blog_desc": "Guías claras "
           "sobre el precio de una web, cómo elegir diseñador y "
           "cómo conseguir más clientes — para pequeños "
           "negocios en España."},
}


def slug_file(slug, lang):
    return f"{slug}.html" if lang == "en" else f"{slug}-es.html"


def url_of(slug, lang):
    return f"{SITE}/{slug_file(slug, lang)}"


def nav(lang):
    t = T[lang]
    home = "/" if lang == "en" else "/index_es.html"
    other = ("es", "Español") if lang == "en" else ("en", "English")
    return f"""<nav class="nav">
  <a href="{home}" class="brand">ONDA</a>
  <a href="{home}#work" class="hide-sm">{t['work']}</a>
  <a href="/{'blog.html' if lang=='en' else 'blog-es.html'}" class="hide-sm">{t['blog']}</a>
  <a href="{home}#packages" class="hide-sm">{t['pricing']}</a>
  <a href="{t['contact']}" class="cta">{t['quote']}</a>
</nav>"""


def footer(lang, links):
    t = T[lang]
    ls = "".join(f'<a href="/{slug_file(s,lang)}">{html.escape(n)}</a>'
                 for s, n in links)
    blog = "blog.html" if lang == "en" else "blog-es.html"
    contact = t["contact"]
    return (f'<footer><div class="wrap" style="display:flex;flex-wrap:wrap;'
            f'gap:1.5rem;justify-content:space-between">'
            f'<div><span style="color:#fff;font-weight:800">ONDA</span><br>'
            f'{html.escape(t["studio"])}</div>'
            f'<nav aria-label="{t["industry"]}" style="display:flex;gap:1.1rem;'
            f'flex-wrap:wrap;max-width:34rem">{ls}'
            f'<a href="/{blog}">{t["blog"]}</a>'
            f'<a href="{contact}">{"Contact" if lang=="en" else "Contacto"}</a>'
            f'</nav></div></footer>')


def head(title, desc, slug, lang, jsonld):
    canonical = url_of(slug, lang)
    alts = (f'<link rel="alternate" hreflang="en" href="{url_of(slug,"en")}">\n'
            f'<link rel="alternate" hreflang="es" href="{url_of(slug,"es")}">\n'
            f'<link rel="alternate" hreflang="x-default" '
            f'href="{url_of(slug,"en")}">')
    blocks = "\n".join(
        f'<script type="application/ld+json">{json.dumps(o, ensure_ascii=False)}</script>'
        for o in jsonld)
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canonical}">
{alts}
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,300..800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/tailwind.css">
<link rel="stylesheet" href="/assets/css/onda-pages.css">
{blocks}
</head>
<body>
{nav(lang)}
<main>"""


def tail(lang, links):
    return (f"</main>\n{footer(lang, links)}\n"
            f'<script defer src="/assets/js/analytics.js"></script>\n'
            f"</body>\n</html>")


def faq_html(faq):
    return '<div class="faq">' + "".join(
        f"<details><summary>{html.escape(q)}</summary>"
        f"<p>{html.escape(a)}</p></details>" for q, a in faq) + "</div>"


def faq_schema(faq, url):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "@id": url + "#faq",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}}
                           for q, a in faq]}


# --- content -------------------------------------------------------------
# Each vertical: shared keys + per-lang dict. ES is transcreated, not literal.
VERTICALS = [
 {"slug": "web-design-dental-clinics", "example": "examples/dental-clinic.html",
  "en": {"crumb": "Dental clinics",
   "title": "Web Design for Dental Clinics in Spain | Onda",
   "meta": "Onda builds fast, booking-focused websites for dental clinics in "
   "Spain — patient trust, treatment pages, online booking. Fixed price, "
   "~3 weeks.",
   "service": "Website design for dental clinics",
   "h1": "Web design for dental clinics in Spain",
   "lead": "Most clinic websites are digital brochures. A dental clinic site "
   "has one job: turn a nervous first-time visitor into a booked appointment. "
   "That is what we build.",
   "ptitle": "Why most dental clinic sites lose patients",
   "problems": [("Booking is buried", "Patients hunt for a phone number on "
     "mobile. Every extra tap is a lost appointment."),
    ("No trust signals", "No real photos, team or reviews — so a new "
     "patient picks the clinic that looks more established."),
    ("Slow and dated", "A heavy 2015 template that loads in 6 seconds on a "
     "phone tells people the care will feel the same.")],
   "btitle": "What a dental clinic site needs",
   "builds": ["Online booking or one-tap WhatsApp/contact on every screen",
    "Clear treatment pages (implants, ortho, whitening) that rank",
    "Real trust: clinic photos, the dentists, verified reviews",
    "Fast mobile-first build (<2s) with local SEO + Google Business",
    "Multilingual when you serve expat patients (ES / EN)"],
   "faq": [("How much does a dental clinic website cost?", "Most clinics fit "
     "our Business Website tier (from EUR 1,490) — a fixed price agreed "
     "before we start."),
    ("Can patients book online?", "Yes. We connect a booking tool or a "
     "one-tap WhatsApp/contact flow, whichever your clinic actually uses."),
    ("Do you handle text and photos?", "Yes. Most clinics don't have content "
     "ready — we shape the structure and tighten the copy.")],
   "cta": "Get more patients booking from your website"},
  "es": {"crumb": "Clínicas dentales",
   "title": "Diseño web para clínicas dentales en España | Onda",
   "meta": "Onda crea webs rápidas y enfocadas en la reserva para "
   "clínicas dentales en España — confianza, páginas de "
   "tratamientos y cita online. Precio cerrado, ~3 semanas.",
   "service": "Diseño web para clínicas dentales",
   "h1": "Diseño web para clínicas dentales en España",
   "lead": "La mayoría de webs de clínica son folletos digitales. "
   "Una web dental tiene un solo trabajo: convertir a un paciente nuevo y "
   "nervioso en una cita reservada. Eso es lo que construimos.",
   "ptitle": "Por qué la mayoría de webs dentales pierden pacientes",
   "problems": [("La reserva está escondida", "El paciente busca un "
     "teléfono en el móvil. Cada toque de más es una cita "
     "perdida."),
    ("Sin señales de confianza", "Sin fotos reales, equipo ni "
     "reseñas, el paciente elige la clínica que parece más "
     "sólida."),
    ("Lenta y anticuada", "Una plantilla de 2015 que tarda 6 segundos en el "
     "móvil sugiere que la atención será igual.")],
   "btitle": "Lo que necesita una web de clínica dental",
   "builds": ["Cita online o WhatsApp/contacto a un toque en cada pantalla",
    "Páginas de tratamientos claras (implantes, ortodoncia) que posicionan",
    "Confianza real: fotos de la clínica, el equipo, reseñas",
    "Web rápida y mobile-first (<2s) con SEO local + Google Business",
    "Multilenguaje si atiendes pacientes extranjeros (ES / EN)"],
   "faq": [("¿Cuánto cuesta una web para clínica dental?", "La "
     "mayoría encaja en el plan Business Website (desde 1.490 EUR), un "
     "precio cerrado acordado antes de empezar."),
    ("¿Pueden reservar online los pacientes?", "Sí. Conectamos una "
     "herramienta de reservas o un flujo de WhatsApp/contacto a un toque."),
    ("¿Os encargáis del texto y las fotos?", "Sí. Casi ninguna "
     "clínica tiene el contenido listo — damos estructura y pulimos "
     "el texto.")],
   "cta": "Consigue más pacientes reservando desde tu web"}},

 {"slug": "web-design-restaurants", "example": "examples/casa-serena.html",
  "en": {"crumb": "Restaurants",
   "title": "Web Design for Restaurants in Spain | Onda",
   "meta": "Onda builds fast restaurant websites in Spain — menu, "
   "reservations and Google Maps that turn searches into tables. Fixed price, "
   "~3 weeks.",
   "service": "Website design for restaurants and hospitality",
   "h1": "Web design for restaurants in Spain",
   "lead": "People decide where to eat on a phone in under a minute. Your "
   "site has to load fast, show the menu and let them book — before they "
   "tab back to the map.",
   "ptitle": "Why diners leave restaurant sites",
   "problems": [("The menu is a PDF", "A PDF that pinch-zooms on mobile is "
     "the fastest way to lose a hungry table."),
    ("No reservations", "If booking isn't one tap, they call a competitor "
     "that made it easy."),
    ("Invisible on Maps", "Weak Google Business presence loses the "
     "'restaurants near me' moment entirely.")],
   "btitle": "What a restaurant site needs",
   "builds": ["A real, fast HTML menu (not a PDF) that's easy to update",
    "One-tap reservations (your tool or WhatsApp) on every page",
    "Google Maps + Business Profile set up to win 'near me' search",
    "Mouth-watering photography, fast on 4G",
    "Multilingual for tourist areas (ES / EN)"],
   "faq": [("Can you replace our PDF menu?", "Yes — we build it as fast, "
     "editable web pages that also help you rank for specific dishes."),
    ("Do you set up reservations?", "Yes. We connect your booking system or "
     "a one-tap WhatsApp flow, whichever fills tables."),
    ("We're in a tourist area — multilingual?", "Yes. Spanish + English "
     "is built in from the start, not bolted on later.")],
   "cta": "Turn 'restaurants near me' into booked tables"},
  "es": {"crumb": "Restaurantes",
   "title": "Diseño web para restaurantes en España | Onda",
   "meta": "Onda crea webs rápidas para restaurantes en España "
   "— carta, reservas y Google Maps que convierten búsquedas en "
   "mesas. Precio cerrado, ~3 semanas.",
   "service": "Diseño web para restaurantes y hostelería",
   "h1": "Diseño web para restaurantes en España",
   "lead": "La gente decide dónde comer en el móvil en menos de un "
   "minuto. Tu web tiene que cargar rápido, enseñar la carta y "
   "dejar reservar — antes de que vuelvan al mapa.",
   "ptitle": "Por qué los comensales abandonan las webs de restaurante",
   "problems": [("La carta es un PDF", "Un PDF que hay que ampliar en el "
     "móvil es la forma más rápida de perder una mesa."),
    ("Sin reservas", "Si reservar no es un toque, llaman al competidor que "
     "lo puso fácil."),
    ("Invisibles en Maps", "Una presencia débil en Google Business "
     "pierde el momento 'restaurantes cerca de mí'.")],
   "btitle": "Lo que necesita una web de restaurante",
   "builds": ["Una carta web real y rápida (no un PDF), fácil de "
    "actualizar", "Reservas a un toque (tu herramienta o WhatsApp) en cada "
    "página", "Google Maps + Perfil de Empresa para ganar el 'cerca de "
    "mí'", "Fotografía apetecible, rápida en 4G",
    "Multilenguaje para zonas turísticas (ES / EN)"],
   "faq": [("¿Podéis sustituir nuestra carta en PDF?", "Sí: la "
     "hacemos como páginas web rápidas y editables que además "
     "ayudan a posicionar por platos concretos."),
    ("¿Configuráis las reservas?", "Sí. Conectamos tu sistema "
     "de reservas o un flujo de WhatsApp a un toque."),
    ("Zona turística — ¿multilenguaje?", "Sí. "
     "Español + inglés desde el principio, no añadido luego.")],
   "cta": "Convierte 'restaurantes cerca de mí' en mesas reservadas"}},

 {"slug": "web-design-real-estate", "example": "examples/real-estate.html",
  "en": {"crumb": "Real estate",
   "title": "Web Design for Real Estate Agencies in Spain | Onda",
   "meta": "Onda builds real-estate websites in Spain that capture qualified "
   "leads — fast listings, strong trust, clear inquiry path. Fixed "
   "price, ~3 weeks.",
   "service": "Website design for real estate agencies",
   "h1": "Web design for real estate agencies in Spain",
   "lead": "High-value buyers judge an agency in seconds. A site that looks "
   "cinematic and makes inquiring effortless is the difference between a lead "
   "and a bounce.",
   "ptitle": "Why property sites lose qualified leads",
   "problems": [("Listings feel cheap", "Generic portal-style cards undersell "
     "premium property and the agency."),
    ("Inquiry is friction", "Long forms and no WhatsApp lose the serious "
     "buyer who wants an answer now."),
    ("No trust", "International buyers need proof you're credible before "
     "they wire money or fly over.")],
   "btitle": "What a real-estate site needs",
   "builds": ["Cinematic, fast listing pages that make property feel premium",
    "Low-friction inquiry: short form + one-tap WhatsApp on every listing",
    "Trust: team, track record, languages, process for foreign buyers",
    "Multilingual (ES / EN), fast on mobile abroad",
    "Lead routing so inquiries reach the right agent instantly"],
   "faq": [("Can you pull listings from our CRM/portal?", "Often yes — "
     "tell us what you use and we'll scope the cleanest sync."),
    ("Do you build for international buyers?", "Yes. Multilingual, fast on "
     "mobile abroad, trust-first structure."),
    ("How fast can it launch?", "Most agency sites go live in about three "
     "weeks at a fixed price agreed up front.")],
   "cta": "Turn property searches into qualified inquiries"},
  "es": {"crumb": "Inmobiliarias",
   "title": "Diseño web para inmobiliarias en España | Onda",
   "meta": "Onda crea webs inmobiliarias en España que captan leads "
   "cualificados — listados rápidos, confianza y contacto claro. "
   "Precio cerrado, ~3 semanas.",
   "service": "Diseño web para inmobiliarias",
   "h1": "Diseño web para inmobiliarias en España",
   "lead": "El comprador de alto valor juzga a una agencia en segundos. Una "
   "web cinematográfica y con un contacto sin fricción marca la "
   "diferencia entre un lead y un rebote.",
   "ptitle": "Por qué las webs inmobiliarias pierden leads",
   "problems": [("Los listados parecen baratos", "Tarjetas genéricas "
     "tipo portal infravaloran la propiedad y la agencia."),
    ("Contactar cuesta", "Formularios largos y sin WhatsApp pierden al "
     "comprador serio que quiere respuesta ya."),
    ("Sin confianza", "El comprador internacional necesita pruebas de que "
     "eres fiable antes de transferir o viajar.")],
   "btitle": "Lo que necesita una web inmobiliaria",
   "builds": ["Páginas de listado rápidas y cinematográficas",
    "Contacto sin fricción: formulario corto + WhatsApp en cada listado",
    "Confianza: equipo, trayectoria, idiomas, proceso para extranjeros",
    "Multilenguaje (ES / EN), rápida en móvil desde el extranjero",
    "Enrutado de leads al agente correcto al instante"],
   "faq": [("¿Podéis traer los listados de nuestro CRM/portal?",
     "A menudo sí — dinos qué usáis y planificamos la "
     "sincronización más limpia."),
    ("¿Construís para compradores internacionales?", "Sí. "
     "Multilenguaje, rápida fuera y con estructura centrada en "
     "confianza."),
    ("¿En cuánto se publica?", "La mayoría en unas tres "
     "semanas, a precio cerrado acordado de antemano.")],
   "cta": "Convierte búsquedas de propiedad en consultas cualificadas"}},

 {"slug": "web-design-aesthetic-clinics",
  "example": "examples/aesthetic-clinic.html",
  "en": {"crumb": "Aesthetic clinics",
   "title": "Web Design for Aesthetic & Beauty Clinics in Spain | Onda",
   "meta": "Onda builds calm, trust-first websites for aesthetic and beauty "
   "clinics in Spain — consultation bookings, before/after, fast mobile. "
   "Fixed price, ~3 weeks.",
   "service": "Website design for aesthetic and beauty clinics",
   "h1": "Web design for aesthetic clinics in Spain",
   "lead": "Aesthetic treatment is an emotional, high-trust decision. The "
   "site has to feel calm and premium, answer doubts, and make booking a "
   "consultation effortless.",
   "ptitle": "Why aesthetic clinic sites don't convert",
   "problems": [("It feels clinical or cheap", "The look has to match the "
     "price of the treatment, or the visitor doesn't believe the result."),
    ("Doubts unanswered", "No clear price range, process or before/after "
     "means they leave to 'think about it'."),
    ("Booking is hard", "High-intent visitors abandon when the consultation "
     "path isn't obvious and instant.")],
   "btitle": "What an aesthetic clinic site needs",
   "builds": ["Calm, premium design that matches the treatment price point",
    "Treatment pages with process, expectations and price ranges",
    "Tasteful before/after and real practitioner credibility",
    "Frictionless consultation booking + one-tap WhatsApp",
    "Fast, mobile-first, multilingual (ES / EN) where needed"],
   "faq": [("Can you show before/after tastefully?", "Yes — designed to "
     "build trust without feeling clinical, within what's allowed."),
    ("Do you include treatment pricing?", "We recommend clear price ranges "
     "— it pre-qualifies enquiries and builds trust."),
    ("How do consultations get booked?", "Whatever you use — a booking "
     "tool or a one-tap WhatsApp flow on every page.")],
   "cta": "Turn treatment research into booked consultations"},
  "es": {"crumb": "Clínicas estéticas",
   "title": "Diseño web para clínicas estéticas en España "
   "| Onda",
   "meta": "Onda crea webs serenas y centradas en la confianza para "
   "clínicas estéticas en España — reserva de consultas, "
   "antes/después, móvil rápido. Precio cerrado, ~3 semanas.",
   "service": "Diseño web para clínicas estéticas y de belleza",
   "h1": "Diseño web para clínicas estéticas en España",
   "lead": "El tratamiento estético es una decisión emocional y de "
   "mucha confianza. La web tiene que transmitir calma y nivel, resolver "
   "dudas y hacer la reserva de consulta muy fácil.",
   "ptitle": "Por qué no convierten las webs de estética",
   "problems": [("Parece clínica o barata", "El aspecto debe estar a la "
     "altura del precio del tratamiento o no creen el resultado."),
    ("Dudas sin resolver", "Sin rango de precio, proceso ni antes/"
     "después, se van a 'pensarlo'."),
    ("Reservar cuesta", "El visitante con intención alta abandona si la "
     "consulta no es obvia e inmediata.")],
   "btitle": "Lo que necesita una web de clínica estética",
   "builds": ["Diseño sereno y premium acorde al precio del tratamiento",
    "Páginas de tratamiento con proceso, expectativas y rangos de precio",
    "Antes/después con buen gusto y credibilidad real del equipo",
    "Reserva de consulta sin fricción + WhatsApp a un toque",
    "Rápida, mobile-first, multilenguaje (ES / EN) si hace falta"],
   "faq": [("¿Mostráis antes/después con buen gusto?", "Sí "
     "— diseñado para generar confianza sin parecer clínico, "
     "dentro de lo permitido."),
    ("¿Incluís precios de tratamiento?", "Recomendamos rangos "
     "claros: precualifican consultas y generan confianza."),
    ("¿Cómo se reservan las consultas?", "Con lo que ya uses: una "
     "herramienta de reservas o WhatsApp a un toque en cada página.")],
   "cta": "Convierte la búsqueda de tratamiento en consultas reservadas"}},

 {"slug": "web-design-architecture-studios",
  "example": "examples/architecture-studio.html",
  "en": {"crumb": "Architecture studios",
   "title": "Web Design for Architecture & Design Studios in Spain | Onda",
   "meta": "Onda builds portfolio-first websites for architecture and design "
   "studios in Spain — work that wins the next project. Fixed price, ~3 "
   "weeks.",
   "service": "Website design for architecture and design studios",
   "h1": "Web design for architecture studios in Spain",
   "lead": "For a studio, the website is the portfolio. It has to make the "
   "work look as considered as it is — and make the right client reach "
   "out.",
   "ptitle": "Why studio sites undersell the work",
   "problems": [("Slow, heavy galleries", "Big images that crawl on mobile "
     "bury the work the studio is judged on."),
    ("No narrative", "Projects as thumbnails with no story — the "
     "thinking that wins commissions is invisible."),
    ("Generic template", "A template says 'generic studio'. The site should "
     "feel designed, like the practice.")],
   "btitle": "What an architecture studio site needs",
   "builds": ["Fast, full-bleed project pages that load instantly on mobile",
    "Project narrative: brief, approach, outcome — not just images",
    "A considered, custom feel that matches the practice",
    "A clear, low-friction path for the right client to make contact",
    "Multilingual (ES / EN) for international commissions"],
   "faq": [("Can you handle large project imagery fast?", "Yes — modern "
     "image formats and a build tuned so heavy galleries still load fast."),
    ("Do you write the project narratives?", "We structure them and tighten "
     "the copy with you so the thinking comes through."),
    ("Can it feel custom, not templated?", "That's the point — every "
     "concept we ship is designed and built in-house.")],
   "cta": "Make your portfolio win the next commission"},
  "es": {"crumb": "Estudios de arquitectura",
   "title": "Diseño web para estudios de arquitectura en España | "
   "Onda",
   "meta": "Onda crea webs centradas en el portfolio para estudios de "
   "arquitectura y diseño en España — trabajo que gana el "
   "siguiente proyecto. Precio cerrado, ~3 semanas.",
   "service": "Diseño web para estudios de arquitectura y diseño",
   "h1": "Diseño web para estudios de arquitectura en España",
   "lead": "Para un estudio, la web es el portfolio. Tiene que hacer que el "
   "trabajo se vea tan cuidado como es — y que el cliente adecuado "
   "escriba.",
   "ptitle": "Por qué las webs de estudio infravaloran el trabajo",
   "problems": [("Galerías lentas y pesadas", "Imágenes enormes que "
     "se arrastran en móvil entierran el trabajo que se juzga."),
    ("Sin relato", "Proyectos como miniaturas sin historia — el "
     "pensamiento que gana encargos es invisible."),
    ("Plantilla genérica", "Una plantilla dice 'estudio genérico'. "
     "La web debe sentirse diseñada, como el estudio.")],
   "btitle": "Lo que necesita una web de estudio de arquitectura",
   "builds": ["Páginas de proyecto a sangre, rápidas en móvil",
    "Relato del proyecto: encargo, enfoque, resultado — no solo "
    "imágenes", "Una sensación cuidada y a medida, como el estudio",
    "Un camino claro y sin fricción para que escriba el cliente correcto",
    "Multilenguaje (ES / EN) para encargos internacionales"],
   "faq": [("¿Manejáis imágenes grandes rápido?", "Sí "
     "— formatos modernos y un build afinado para que las galerías "
     "pesadas carguen rápido."),
    ("¿Escribís los relatos de proyecto?", "Los estructuramos y "
     "pulimos contigo para que se vea el pensamiento detrás."),
    ("¿Puede sentirse a medida, no de plantilla?", "Ese es el punto: "
     "cada concepto que entregamos es diseñado y programado en casa.")],
   "cta": "Haz que tu portfolio gane el próximo encargo"}},
]

FOOTER_LINKS = [(v["slug"], v["en"]["crumb"]) for v in VERTICALS]
FOOTER_LINKS_ES = [(v["slug"], v["es"]["crumb"]) for v in VERTICALS]


def vertical_page(v, lang):
    c = v[lang]
    t = T[lang]
    url = url_of(v["slug"], lang)
    problems = "".join(f'<div class="card"><h3>{html.escape(pt)}</h3>'
                       f'<p>{html.escape(pd)}</p></div>'
                       for pt, pd in c["problems"])
    builds = "".join(f'<div class="check">{html.escape(b)}</div>'
                     for b in c["builds"])
    jsonld = [
     {"@context": "https://schema.org", "@type": "Service",
      "serviceType": c["service"], "name": c["h1"],
      "provider": {"@type": "Organization", "name": "Onda",
                   "@id": f"{SITE}/#org", "url": SITE},
      "areaServed": {"@type": "Country", "name": "Spain"},
      "inLanguage": lang, "description": c["meta"], "url": url},
     faq_schema(c["faq"], url),
     {"@context": "https://schema.org", "@type": "BreadcrumbList",
      "itemListElement": [
       {"@type": "ListItem", "position": 1, "name": t["home"], "item": SITE},
       {"@type": "ListItem", "position": 2, "name": c["crumb"],
        "item": url}]}]
    links = FOOTER_LINKS if lang == "en" else FOOTER_LINKS_ES
    body = f"""
<section><div class="wrap reveal">
  <div class="crumb"><a href="{'/' if lang=='en' else '/index_es.html'}">{t['home']}</a> · {html.escape(c['crumb'])}</div>
  <div class="eyebrow" style="margin:1.5rem 0 .9rem">{t['industry']} · {html.escape(c['crumb'])}</div>
  <h1 style="max-width:18ch">{html.escape(c['h1'])}</h1>
  <p class="lead" style="margin-top:1.1rem">{html.escape(c['lead'])}</p>
  <div style="display:flex;gap:.75rem;flex-wrap:wrap;margin-top:2rem">
    <a class="btn btn-p" href="{t['contact']}">{t['quote']}</a>
    <a class="btn btn-g" href="{t['wa_url']}" target="_blank" rel="noopener">{t['wa']}</a>
  </div>
</div></section>
<hr class="divider">
<section><div class="wrap">
  <h2 style="max-width:20ch">{html.escape(c['ptitle'])}</h2>
  <div class="grid cols-3" style="margin-top:2rem">{problems}</div>
</div></section>
<hr class="divider">
<section><div class="wrap">
  <div class="eyebrow">{'What we build' if lang=='en' else 'Qué construimos'}</div>
  <h2 style="margin:.7rem 0 1.5rem;max-width:22ch">{html.escape(c['btitle'])}</h2>
  <div style="max-width:48rem">{builds}</div>
  <p style="margin-top:2rem"><a href="{v['example']}" class="btn btn-g">{t['see']} {html.escape(c['crumb'].lower())} {t['concept']}</a></p>
</div></section>
<hr class="divider">
<section><div class="wrap prose">
  <div class="eyebrow">{t['faq']}</div>
  <h2 style="margin:.7rem 0 1.5rem">{html.escape(c['crumb'])} {t['common']}</h2>
  {faq_html(c['faq'])}
</div></section>
<hr class="divider">
<section><div class="wrap" style="text-align:center">
  <h2 style="margin:0 auto;max-width:20ch">{html.escape(c['cta'])}</h2>
  <p style="margin:1rem auto 2rem;max-width:48ch">{t['fixed']}</p>
  <a class="btn btn-p" href="{t['contact']}">{t['quote']}</a>
</div></section>"""
    return head(c["title"], c["meta"], v["slug"], lang, jsonld) + body + tail(lang, links)


BLOG_POSTS = [
 {"slug": "how-much-does-a-website-cost-spain",
  "en": {"crumb": "Website cost in Spain (2026)",
   "title": "How Much Does a Website Cost in Spain? (2026 Guide) | Onda",
   "h1": "How much does a website cost in Spain in 2026?",
   "desc": "A straight answer on website pricing in Spain in 2026 — real "
   "ranges for small-business sites, what changes the price, what to avoid.",
   "body": [("Short answer", "For a small service business in Spain in 2026, "
     "a custom website typically costs between EUR 690 and EUR 2,490. A "
     "one-page launch site is around EUR 690; a 5-page business site with SEO "
     "and lead capture around EUR 1,490; a site plus one practical automation "
     "around EUR 2,490. DIY builders are cheaper up front but cost more over "
     "three years once you add plugins, fixes and lost leads."),
    ("What changes the price", "Number of pages, online booking or "
     "e-commerce, how much copy and photography is ready, languages (Spanish "
     "+ English is common), and how fast you need it live. A fixed scope "
     "agreed up front keeps the price predictable."),
    ("Cheap vs custom over 3 years", "A EUR 25/month builder looks cheaper "
     "than a EUR 1,490 custom site until you add paid themes, plugins, a "
     "developer to fix them, and the leads a slow generic site loses every "
     "month. Over three years the gap usually closes or reverses."),
    ("What to avoid", "Agencies that won't give a number before a call, "
     "'unlimited revisions' with no fixed scope, and anyone who can't show "
     "you work. Ask for a fixed price, a clear scope and a launch date in "
     "writing.")],
   "faq": [("Is a cheap template website a bad idea?", "Not always — for "
     "a brand-new business testing an idea it can be fine. Once the site must "
     "win trust and capture leads, a fast custom site usually pays for "
     "itself."),
    ("Why do prices vary so much?", "Scope. Pages, booking/e-commerce, "
     "languages and ready content move price far more than the agency's "
     "logo."),
    ("Does Onda give fixed prices?", "Yes. We agree a fixed price and scope "
     "before starting — most small-business sites fall in the EUR "
     "690–2,490 range.")]},
  "es": {"crumb": "Precio de una web en España (2026)",
   "title": "¿Cuánto cuesta una página web en España? "
   "(Guía 2026) | Onda",
   "h1": "¿Cuánto cuesta una página web en España en 2026?",
   "desc": "Respuesta clara sobre el precio de una web en España en 2026 "
   "— rangos reales para pequeños negocios, qué cambia el "
   "precio y qué evitar.",
   "body": [("Respuesta corta", "Para un pequeño negocio de servicios en "
     "España en 2026, una web a medida suele costar entre 690 EUR y "
     "2.490 EUR. Una web de una página ronda los 690 EUR; una web de 5 "
     "páginas con SEO y captación de leads, unos 1.490 EUR; una web "
     "más una automatización práctica, unos 2.490 EUR. Los "
     "creadores DIY son más baratos al principio pero cuestan más "
     "en tres años con plugins, arreglos y leads perdidos."),
    ("Qué cambia el precio", "Número de páginas, reserva "
     "online o tienda, cuánto texto y foto hay listos, idiomas "
     "(español + inglés es habitual) y para cuándo lo "
     "necesitas. Un alcance cerrado de antemano mantiene el precio "
     "predecible."),
    ("Barato vs a medida en 3 años", "Un creador de 25 EUR/mes parece "
     "más barato que una web a medida de 1.490 EUR hasta que sumas "
     "plantillas de pago, plugins, un dev que los arregle y los leads que "
     "una web lenta y genérica pierde cada mes. En tres años la "
     "diferencia suele igualarse o invertirse."),
    ("Qué evitar", "Agencias que no dan una cifra antes de una llamada, "
     "'revisiones ilimitadas' sin alcance cerrado, y quien no puede "
     "enseñarte trabajo. Pide precio cerrado, alcance claro y fecha de "
     "publicación por escrito.")],
   "faq": [("¿Una web de plantilla barata es mala idea?", "No siempre "
     "— para un negocio nuevo probando una idea puede valer. Cuando la "
     "web debe generar confianza y captar leads, una web rápida a "
     "medida suele amortizarse sola."),
    ("¿Por qué varían tanto los precios?", "El alcance. "
     "Páginas, reservas/tienda, idiomas y contenido listo mueven el "
     "precio mucho más que el logo de la agencia."),
    ("¿Onda da precios cerrados?", "Sí. Acordamos precio y alcance "
     "antes de empezar — la mayoría de webs de pequeño "
     "negocio caen entre 690 y 2.490 EUR.")]}},

 {"slug": "how-to-choose-a-web-designer",
  "en": {"crumb": "How to choose a web designer",
   "title": "How to Choose a Web Designer: 10 Questions to Ask | Onda",
   "h1": "How to choose a web designer (10 questions to ask first)",
   "desc": "The 10 questions that separate a web designer who gets you more "
   "clients from one who just makes a pretty site. A buyer's checklist.",
   "body": [("Start with the outcome, not the design", "The right question "
     "is not 'will it look good' — it's 'will it get me more booked "
     "clients'. Ask how they'll make the site convert, not just how it will "
     "look. A beautiful site that doesn't generate inquiries is a cost, not "
     "an asset."),
    ("The 10 questions", "1. Can I see real work? 2. What's the fixed price "
     "and what's included? 3. When exactly does it go live? 4. Who actually "
     "does the work? 5. How will it get me more inquiries? 6. Is it fast on "
     "mobile (Core Web Vitals)? 7. Do you set up Google/local SEO? 8. What "
     "happens if I need changes later? 9. Do you handle copy and photos? "
     "10. Who owns the site and domain?"),
    ("Red flags", "No price before a call, no portfolio, 'unlimited "
     "revisions' with no fixed scope, vague timelines, and you can't tell "
     "who'll do the work. Slow, generic template output is the most common "
     "and most expensive mistake."),
    ("Green flags", "A fixed price and scope in writing, real examples, a "
     "clear launch date, one accountable person, and answers framed around "
     "your customers and inquiries — not just visuals.")],
   "faq": [("Agency or freelancer?", "What matters is who's accountable, the "
     "quality of the work and a fixed scope — not the label. Ask to "
     "speak to whoever actually builds it."),
    ("Should the price be fixed?", "For a small-business site, yes. A fixed "
     "price and scope agreed up front protects you from open-ended bills."),
    ("How long should it take?", "A focused small-business site is usually "
     "~3 weeks. Months usually means bloated process, not better quality.")]},
  "es": {"crumb": "Cómo elegir diseñador web",
   "title": "Cómo elegir un diseñador web: 10 preguntas | Onda",
   "h1": "Cómo elegir un diseñador web (10 preguntas antes de "
   "contratar)",
   "desc": "Las 10 preguntas que distinguen a un diseñador que te trae "
   "más clientes de uno que solo hace una web bonita. Checklist para "
   "contratar.",
   "body": [("Empieza por el resultado, no por el diseño", "La pregunta "
     "correcta no es '¿quedará bonita?' sino '¿me traerá "
     "más clientes?'. Pregunta cómo harán que la web convierta, "
     "no solo cómo se verá. Una web preciosa que no genera "
     "consultas es un gasto, no un activo."),
    ("Las 10 preguntas", "1. ¿Puedo ver trabajo real? 2. ¿Precio "
     "cerrado y qué incluye? 3. ¿Cuándo se publica "
     "exactamente? 4. ¿Quién hace el trabajo? 5. ¿Cómo me "
     "traerá más consultas? 6. ¿Es rápida en móvil "
     "(Core Web Vitals)? 7. ¿Configuráis SEO local/Google? 8. "
     "¿Qué pasa si necesito cambios luego? 9. ¿Os encargáis "
     "del texto y las fotos? 10. ¿De quién es la web y el dominio?"),
    ("Señales de alarma", "Sin precio antes de una llamada, sin "
     "portfolio, 'revisiones ilimitadas' sin alcance, plazos vagos y no "
     "saber quién hará el trabajo. Una plantilla lenta y "
     "genérica es el error más común y más caro."),
    ("Buenas señales", "Precio y alcance cerrados por escrito, ejemplos "
     "reales, fecha de publicación clara, una persona responsable y "
     "respuestas centradas en tus clientes y consultas, no solo en lo "
     "visual.")],
   "faq": [("¿Agencia o freelance?", "Lo que importa es quién "
     "responde, la calidad del trabajo y un alcance cerrado, no la etiqueta. "
     "Pide hablar con quien lo construye."),
    ("¿El precio debería ser cerrado?", "Para una web de "
     "pequeño negocio, sí. Precio y alcance acordados de antemano "
     "te protegen de facturas abiertas."),
    ("¿Cuánto debería tardar?", "Una web enfocada suele ser "
     "~3 semanas. Meses suele significar proceso inflado, no más "
     "calidad.")]}},
]


def blog_post_page(p, lang):
    c = p[lang]
    t = T[lang]
    url = url_of(p["slug"], lang)
    secs = "".join(f'<h2 style="margin-top:2.5rem">{html.escape(ht)}</h2>'
                   f'<p style="margin-top:.8rem">{html.escape(bd)}</p>'
                   for ht, bd in c["body"])
    blog_home = "blog.html" if lang == "en" else "blog-es.html"
    jsonld = [
     {"@context": "https://schema.org", "@type": "Article",
      "headline": c["h1"], "description": c["desc"], "url": url,
      "inLanguage": lang,
      "author": {"@type": "Organization", "name": "Onda", "@id": f"{SITE}/#org"},
      "publisher": {"@type": "Organization", "name": "Onda",
                    "@id": f"{SITE}/#org"}},
     faq_schema(c["faq"], url),
     {"@context": "https://schema.org", "@type": "BreadcrumbList",
      "itemListElement": [
       {"@type": "ListItem", "position": 1, "name": t["home"], "item": SITE},
       {"@type": "ListItem", "position": 2, "name": t["blog"],
        "item": f"{SITE}/{blog_home}"},
       {"@type": "ListItem", "position": 3, "name": c["crumb"],
        "item": url}]}]
    links = FOOTER_LINKS if lang == "en" else FOOTER_LINKS_ES
    body = f"""
<section><div class="wrap prose reveal">
  <div class="crumb"><a href="{'/' if lang=='en' else '/index_es.html'}">{t['home']}</a> · <a href="/{blog_home}">{t['blog']}</a> · {html.escape(c['crumb'])}</div>
  <h1 style="margin:1.4rem 0 1rem;max-width:22ch">{html.escape(c['h1'])}</h1>
  <p class="lead">{html.escape(c['desc'])}</p>
  {secs}
  <h2 style="margin-top:2.5rem">{t['faq']}</h2>
  {faq_html(c['faq'])}
  <p style="margin-top:2.5rem"><a class="btn btn-p" href="{t['contact']}">{t['quote']}</a></p>
</div></section>"""
    return head(c["title"], c["desc"], p["slug"], lang, jsonld) + body + tail(lang, links)


def blog_index(lang):
    t = T[lang]
    slug = "blog"
    url = f"{SITE}/{'blog.html' if lang=='en' else 'blog-es.html'}"
    cards = "".join(
        f'<a class="card" href="/{slug_file(p["slug"],lang)}" style="display:block">'
        f'<h3>{html.escape(p[lang]["h1"])}</h3>'
        f'<p style="margin-top:.5rem">{html.escape(p[lang]["desc"])}</p></a>'
        for p in BLOG_POSTS)
    jsonld = [{"@context": "https://schema.org", "@type": "Blog", "url": url,
               "name": "Onda Blog", "inLanguage": lang,
               "publisher": {"@type": "Organization", "name": "Onda",
                             "@id": f"{SITE}/#org"}}]
    links = FOOTER_LINKS if lang == "en" else FOOTER_LINKS_ES
    body = f"""
<section><div class="wrap reveal">
  <div class="crumb"><a href="{'/' if lang=='en' else '/index_es.html'}">{t['home']}</a> · {t['blog']}</div>
  <div class="eyebrow" style="margin:1.5rem 0 .9rem">{t['blog']}</div>
  <h1 style="max-width:20ch">{html.escape(t['blog_h1'])}</h1>
  <p class="lead" style="margin-top:1rem">{html.escape(t['blog_lead'])}</p>
  <div class="grid cols-2" style="margin-top:2.5rem">{cards}</div>
</div></section>"""
    # blog index hreflang: handled via head() using slug 'blog'
    return head(t["blog_title"], t["blog_desc"], slug, lang, jsonld) + body + tail(lang, links)


def main():
    n = 0
    for lang in ("en", "es"):
        for v in VERTICALS:
            (FRONTEND / slug_file(v["slug"], lang)).write_text(
                vertical_page(v, lang), encoding="utf-8")
            n += 1
        for p in BLOG_POSTS:
            (FRONTEND / slug_file(p["slug"], lang)).write_text(
                blog_post_page(p, lang), encoding="utf-8")
            n += 1
        (FRONTEND / ("blog.html" if lang == "en" else "blog-es.html")).write_text(
            blog_index(lang), encoding="utf-8")
        n += 1
    print(f"  generated {n} pages (EN+ES verticals/posts/blog)")


if __name__ == "__main__":
    print("Build content pages (EN + ES):")
    main()
