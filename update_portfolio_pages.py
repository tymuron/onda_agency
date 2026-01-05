import os
import re

PORTFOLIO_DIR = 'frontend/portfolio'

# Templates
HEAD_TEMPLATE = """<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Onda | {title}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <link rel="icon" type="image/png" href="../favicon.png">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #FFFFFF;
            --text-primary: #0F172A;
            --text-secondary: #64748B;
            --accent: #2563EB;
            --accent-soft: #EFF6FF;
            --border-color: #E2E8F0;
        }}
        body {{
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-primary);
            overflow-x: hidden;
        }}
        .btn-primary {{
            background-color: var(--accent);
            color: white;
            padding: 0.75rem 1.5rem;
            border-radius: 9999px;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            transition: all 0.2s ease;
        }}
        .btn-primary:hover {{
            background-color: #1D4ED8;
            transform: translateY(-1px);
        }}
        .modern-card {{
            background: white;
            border: 1px solid var(--border-color);
            border-radius: 1rem;
            transition: all 0.3s ease;
        }}
    </style>
</head>"""

NAV_EN = """<nav class="fixed w-full z-50 bg-white/90 backdrop-blur-md border-b border-slate-100 transition-all duration-300">
        <div class="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
            <a href="../index.html" class="flex items-center gap-2 group">
                <div class="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center text-white">
                    <i data-lucide="waves" class="w-5 h-5"></i>
                </div>
                <span class="text-xl font-bold tracking-tight text-slate-900">ONDA</span>
            </a>
            <div class="hidden md:flex items-center gap-8 text-sm font-medium text-slate-600">
                <a href="../portfolio.html" class="text-blue-600 font-bold transition-colors">Back to Collection</a>
                <a href="../index.html#agents" class="hover:text-blue-600 transition-colors">Solutions</a>
                <a href="../process.html" class="hover:text-blue-600 transition-colors">Process</a>
                <a href="../index.html#contact" class="hover:text-blue-600 transition-colors">Contact</a>
                <div class="flex gap-3 border-l border-slate-200 pl-6">
                    <span class="text-blue-600 font-bold">EN</span>
                    <a href="{link_es}" class="text-slate-400 hover:text-slate-900 transition-colors">ES</a>
                    <a href="{link_ru}" class="text-slate-400 hover:text-slate-900 transition-colors">RU</a>
                </div>
            </div>
            <button class="md:hidden text-slate-900"><i data-lucide="menu"></i></button>
        </div>
    </nav>"""

NAV_ES = """<nav class="fixed w-full z-50 bg-white/90 backdrop-blur-md border-b border-slate-100 transition-all duration-300">
        <div class="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
            <a href="../index_es.html" class="flex items-center gap-2 group">
                <div class="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center text-white">
                    <i data-lucide="waves" class="w-5 h-5"></i>
                </div>
                <span class="text-xl font-bold tracking-tight text-slate-900">ONDA</span>
            </a>
            <div class="hidden md:flex items-center gap-8 text-sm font-medium text-slate-600">
                <a href="../portfolio_es.html" class="text-blue-600 font-bold transition-colors">Volver a la Colección</a>
                <a href="../index_es.html#agents" class="hover:text-blue-600 transition-colors">Demos IA</a>
                <a href="../process_es.html" class="hover:text-blue-600 transition-colors">Proceso</a>
                <a href="../index_es.html#contact" class="hover:text-blue-600 transition-colors">Contacto</a>
                <div class="flex gap-3 border-l border-slate-200 pl-6">
                    <a href="{link_en}" class="text-slate-400 hover:text-slate-900 transition-colors">EN</a>
                    <span class="text-blue-600 font-bold">ES</span>
                    <a href="{link_ru}" class="text-slate-400 hover:text-slate-900 transition-colors">RU</a>
                </div>
            </div>
            <button class="md:hidden text-slate-900"><i data-lucide="menu"></i></button>
        </div>
    </nav>"""

NAV_RU = """<nav class="fixed w-full z-50 bg-white/90 backdrop-blur-md border-b border-slate-100 transition-all duration-300">
        <div class="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
            <a href="../index_ru.html" class="flex items-center gap-2 group">
                <div class="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center text-white">
                    <i data-lucide="waves" class="w-5 h-5"></i>
                </div>
                <span class="text-xl font-bold tracking-tight text-slate-900">ONDA</span>
            </a>
            <div class="hidden md:flex items-center gap-8 text-sm font-medium text-slate-600">
                <a href="../portfolio_ru.html" class="text-blue-600 font-bold transition-colors">Назад в Коллекцию</a>
                <a href="../index_ru.html#agents" class="hover:text-blue-600 transition-colors">AI Демо</a>
                <a href="../process_ru.html" class="hover:text-blue-600 transition-colors">Процесс</a>
                <a href="../index_ru.html#contact" class="hover:text-blue-600 transition-colors">Контакты</a>
                <div class="flex gap-3 border-l border-slate-200 pl-6">
                    <a href="{link_en}" class="text-slate-400 hover:text-slate-900 transition-colors">EN</a>
                    <a href="{link_es}" class="text-slate-400 hover:text-slate-900 transition-colors">ES</a>
                    <span class="text-blue-600 font-bold">RU</span>
                </div>
            </div>
            <button class="md:hidden text-slate-900"><i data-lucide="menu"></i></button>
        </div>
    </nav>"""

FOOTER_EN = """<footer class="bg-slate-900 text-white py-12 text-center px-6 mt-12">
        <p class="text-slate-500 text-sm font-medium">&copy; 2024 Onda. Intelligence Applied.</p>
    </footer>"""

FOOTER_ES = """<footer class="bg-slate-900 text-white py-12 text-center px-6 mt-12">
        <p class="text-slate-500 text-sm font-medium">&copy; 2024 Onda. Inteligencia Aplicada.</p>
    </footer>"""

FOOTER_RU = """<footer class="bg-slate-900 text-white py-12 text-center px-6 mt-12">
        <p class="text-slate-500 text-sm font-medium">&copy; 2024 Onda. Прикладной Интеллект.</p>
    </footer>"""

def get_links(filename):
    base = filename.replace('_es.html', '').replace('_ru.html', '').replace('.html', '')
    return {
        'en': f"{base}.html",
        'es': f"{base}_es.html",
        'ru': f"{base}_ru.html"
    }

def process_file(filename):
    path = os.path.join(PORTFOLIO_DIR, filename)
    with open(path, 'r') as f:
        content = f.read()

    # Determine Lang
    lang = 'en'
    if '_es.html' in filename: lang = 'es'
    if '_ru.html' in filename: lang = 'ru'
    
    # Extract Title (preserve it)
    title_match = re.search(r'<title>(.*?)</title>', content)
    title = title_match.group(1).replace('Onda | ', '') if title_match else 'Case Study'

    # Get Links
    links = get_links(filename)

    # Select Templates
    head = HEAD_TEMPLATE.format(title=title)
    if lang == 'en':
        nav = NAV_EN.format(link_es=links['es'], link_ru=links['ru'])
        footer = FOOTER_EN
    elif lang == 'es':
        nav = NAV_ES.format(link_en=links['en'], link_ru=links['ru'])
        footer = FOOTER_ES
    elif lang == 'ru':
        nav = NAV_RU.format(link_en=links['en'], link_es=links['es'])
        footer = FOOTER_RU

    # Replace specific sections using generic string markers or regex if structure varies
    # We assume standard structure based on previous view: Head, Body > Nav, Content, Footer
    
    # Replace Head
    content = re.sub(r'<head>.*?</head>', head, content, flags=re.DOTALL)
    
    # Replace Nav (Scanning for <nav>...</nav>)
    content = re.sub(r'<nav.*?</nav>', nav, content, flags=re.DOTALL)
    
    # Replace Footer (Scanning for <footer.*?>.*?</footer>)
    content = re.sub(r'<footer.*?</footer>', footer, content, flags=re.DOTALL)

    # Update Body classes if needed (remove old font classes if any, though CSS handles it)
    content = content.replace('font-serif', '') # Remove old serif classes from body elements to let Inter take over
    content = content.replace('italic', '') # Remove old italic styles
    
    # Write back
    with open(path, 'w') as f:
        f.write(content)
    print(f"Updated {filename}")

def main():
    files = [f for f in os.listdir(PORTFOLIO_DIR) if f.endswith('.html')]
    for f in files:
        try:
            process_file(f)
        except Exception as e:
            print(f"Error processing {f}: {e}")

if __name__ == '__main__':
    main()
