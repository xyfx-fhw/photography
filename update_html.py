import os

def write_html(filename, title, date, location, latin_location, description, json_path):
    content = f'''<!DOCTYPE html>
<html lang="zh-CN" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - 摄影画册 | 雪云飞星</title>
    <link rel="icon" href="../favicon.svg" type="image/svg+xml">
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Noto+Sans+SC:wght@300;400;500&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        :root {{ --bg-color: #0f1112; --accent-color: #c5a059; --text-main: #e2e2e2; }}
        body {{ font-family: 'Noto Sans SC', sans-serif; background-color: var(--bg-color); color: var(--text-main); }}
        .font-serif {{ font-family: 'Playfair Display', serif; }}
        .masonry {{ column-count: 1; column-gap: 1.5rem; }}
        @media (min-width: 768px) {{ .masonry {{ column-count: 2; }} }}
        @media (min-width: 1024px) {{ .masonry {{ column-count: 3; }} }}
        .masonry-item {{ break-inside: avoid; margin-bottom: 1.5rem; transform: translateY(20px); opacity: 0; transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1); }}
        .masonry-item.loaded {{ transform: translateY(0); opacity: 1; }}
    </style>
</head>
<body class="antialiased">
    <nav class="fixed top-0 w-full z-50 px-8 py-6 flex justify-between items-center bg-gradient-to-b from-black/80 to-transparent">
        <a href="../index.html" class="flex items-center text-xs uppercase tracking-[0.3em] text-gray-400 hover:text-[#c5a059] transition-colors group">
            <i data-lucide="arrow-left" class="w-4 h-4 mr-2 group-hover:-translate-x-1 transition-transform"></i> 返回首页
        </a>
    </nav>

    <header class="pt-40 pb-20 px-8 max-w-7xl mx-auto border-b border-white/5">
        <div class="flex flex-col md:flex-row md:items-end justify-between">
            <div>
                <span class="text-[#c5a059] text-[10px] uppercase tracking-widest">Travel Log · {date}</span>
                <h1 class="text-5xl md:text-7xl font-serif italic mt-4 mb-6 text-white">{title}</h1>
                <p class="text-gray-500 max-w-2xl leading-relaxed font-light text-sm">{description}</p>
            </div>
            <div class="mt-8 md:mt-0 text-right">
                <div class="flex items-center justify-end space-x-2 text-[#c5a059] mb-1">
                    <i data-lucide="map-pin" class="w-4 h-4"></i>
                    <span class="text-sm font-serif italic text-white text-right">{location}</span>
                </div>
                <p class="text-[10px] text-gray-600 tracking-tighter uppercase">{latin_location}</p>
            </div>
        </div>
    </header>

    <main class="px-8 py-20 max-w-7xl mx-auto">
        <div id="photo-grid" class="masonry"></div>
    </main>

    <div id="lightbox" class="fixed inset-0 bg-[#0a0a0a]/98 z-[100] hidden flex flex-col items-center justify-center p-4 cursor-zoom-out" onclick="closeLightbox()">
        <img id="lightboxImg" class="max-w-full max-h-[90vh] shadow-2xl transition-transform duration-500 scale-95" src="">
    </div>

    <script>
        async function loadGallery() {{
            try {{
                const response = await fetch('{json_path}');
                const photos = await response.json();
                const grid = document.getElementById('photo-grid');
                grid.innerHTML = photos.map(p => `
                    <div class="masonry-item group cursor-zoom-in overflow-hidden rounded-sm bg-neutral-900" onclick="openLightbox('${{p.url}}')">
                        <img src="${{p.url}}" class="w-full h-auto hover:scale-[1.03] transition-transform duration-700" onload="this.parentElement.classList.add('loaded')" loading="lazy">
                    </div>
                `).join('');
                if(window.lucide) lucide.createIcons();
            } catch (e) {{ console.error('Gallery Error:', e); }}
        }}

        function openLightbox(src) {{
            const lb = document.getElementById('lightbox');
            const img = document.getElementById('lightboxImg');
            img.src = src;
            lb.classList.remove('hidden');
            setTimeout(() => img.classList.remove('scale-95'), 10);
            document.body.style.overflow = 'hidden';
        }}

        function closeLightbox() {{
            const lb = document.getElementById('lightbox');
            const img = document.getElementById('lightboxImg');
            img.classList.add('scale-95');
            setTimeout(() => {{ lb.classList.add('hidden'); document.body.style.overflow = 'auto'; }}, 300);
        }}

        window.onload = loadGallery;
    </script>
</body>
</html>'''
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

write_html('notes/aba.html', '川北秋韵', '2024.10', '中国 · 川北', 'Jiuzhai & Huanglong', '九寨沟、黄龙、达古冰川。在深秋奏响的光影协奏曲。', '../images/aba/index.json')
write_html('notes/indonesia.html', '万岛之国', '2024.05', '印度尼西亚 · 巴厘岛', 'Bali & Penida', '巴厘岛与佩尼达岛。热带雨林与悬崖海浪的自然诗篇。', '../images/indonesia/index.json')
write_html('notes/yunnan.html', '滇西北纪行', '2025.02', '中国 · 滇西北', 'Dali, Lijiang & Meili', '大理、丽江、香格里拉与梅里雪山。离天空最近的旅程。', '../images/yunnan/index.json')
