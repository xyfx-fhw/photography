import os
import json
import re
from PIL import Image, ImageOps
try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
    print("✅ HEIF Support Registered")
except ImportError:
    print("⚠️ pillow-heif not found, HEIC files might fail")

def process_images_for_folder(source_folder, output_folder, web_path_prefix, max_width=2560, quality=80):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    image_data = []
    supported_formats = ('.jpg', '.jpeg', '.png', '.webp', '.heic', '.heif', '.tiff')

    print(f"\n🚀 Processing: {source_folder}")

    if not os.path.exists(source_folder):
        print(f"❌ Folder not found: {source_folder}")
        return

    # List files and filter by extensions
    files = sorted([f for f in os.listdir(source_folder) if f.lower().endswith(supported_formats)])

    if not files:
        print(f"⚠️ No images found in {source_folder}")
        return

    for filename in files:
        file_path = os.path.join(source_folder, filename)
        try:
            with Image.open(file_path) as img:
                # Correct orientation
                img = ImageOps.exif_transpose(img)

                # Convert to RGB
                if img.mode != "RGB":
                    img = img.convert("RGB")

                # Get dimensions
                w, h = img.size

                # Scale down if too large
                if w > max_width:
                    new_w = max_width
                    new_h = int(h * (max_width / w))
                    img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                else:
                    new_w, new_h = w, h

                # Save as WebP
                output_filename = os.path.splitext(filename)[0] + ".webp"
                output_path = os.path.join(output_folder, output_filename)

                img.save(output_path, "WEBP", quality=quality, method=6)

                image_data.append({
                    "url": f"{web_path_prefix}/{output_filename}",
                    "width": new_w,
                    "height": new_h,
                    "title": os.path.splitext(filename)[0]
                })
                print(f"✅ {filename} -> {output_filename} ({os.path.getsize(output_path)//1024}KB)")
        except Exception as e:
            print(f"❌ Failed {filename}: {str(e)}")

    # Update HTML
    update_gallery_html(source_folder.split('/')[-1], image_data)

    # Save a JSON backup
    with open(os.path.join(output_folder, "index.json"), "w") as f:
        json.dump(image_data, f, indent=4)

def update_gallery_html(gallery_id, photos):
    path = f"notes/{gallery_id}.html"
    if not os.path.exists(path): return

    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    data_str = json.dumps(photos, indent=8, ensure_ascii=False)

    new_func = f"""
        function loadGallery() {{
            const photos = {data_str};
            const grid = document.getElementById('photo-grid');
            if (!grid) return;
            grid.innerHTML = photos.map(p => `
                <div class="masonry-item group cursor-zoom-in overflow-hidden rounded-sm bg-neutral-900" onclick="openLightbox('${{p.url}}')">
                    <img src="${{p.url}}" class="w-full h-auto hover:scale-[1.03] transition-transform duration-700" onload="this.parentElement.classList.add('loaded')" loading="lazy">
                </div>
            `).join('');
            if(window.lucide) lucide.createIcons();
        }}"""

    pattern = r"(async\s+)?function\s+loadGallery\s*\(\)\s*\{.*?\}(?=\s*function|window\.onload)"
    if re.search(pattern, html, flags=re.DOTALL):
        html = re.sub(pattern, new_func + "\n        ", html, flags=re.DOTALL)
    else:
        pattern_data = r"const\s+photos\s*=\s*\[.*?\];"
        html = re.sub(pattern_data, f"const photos = {data_str};", html, flags=re.DOTALL)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == "__main__":
    tasks = [
        ('raw_photos/aba', 'images/aba', '../images/aba'),
        ('raw_photos/indonesia', 'images/indonesia', '../images/indonesia'),
        ('raw_photos/yunnan', 'images/yunnan', '../images/yunnan')
    ]
    for src, out, web in tasks:
        process_images_for_folder(src, out, web)
