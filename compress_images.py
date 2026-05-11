"""
One-time image compression script. Run from repo root:
    python compress_images.py

- JPGs: resize to max 1400px, quality=82
- PNGs with alpha: resize to max 1400px, save as compressed PNG
- PNGs without alpha (solid photos): convert to JPEG, save as .jpg
  (template references to converted files must be updated separately)
"""
from pathlib import Path
from PIL import Image

IMG_DIR = Path("static/img")
MAX_SIZE = 1400
JPEG_QUALITY = 82

# PNGs to keep as PNG regardless of alpha (logos, icons, QR codes)
KEEP_PNG = {
    "logo.png",
    "mappin.png",
    "gift-card.png",
    "TNKY Design.png",
    "Google Review QR.png",
    "yelplogo.png",
}

converted_to_jpg = []
compressed_png = []
compressed_jpg = []

for path in sorted(IMG_DIR.iterdir()):
    if path.suffix.lower() not in (".jpg", ".jpeg", ".png", ".webp"):
        continue

    try:
        img = Image.open(path)
    except Exception as e:
        print(f"  SKIP {path.name}: {e}")
        continue

    original_size = path.stat().st_size
    w, h = img.size

    # Resize if larger than MAX_SIZE on either dimension
    if w > MAX_SIZE or h > MAX_SIZE:
        img.thumbnail((MAX_SIZE, MAX_SIZE), Image.LANCZOS)

    if path.suffix.lower() == ".png" and path.name not in KEEP_PNG:
        # Check for alpha channel
        has_alpha = img.mode in ("RGBA", "LA") or (
            img.mode == "P" and "transparency" in img.info
        )
        if not has_alpha:
            # Convert to JPEG — save as .jpg alongside original, then replace
            jpg_path = path.with_suffix(".jpg")
            rgb = img.convert("RGB")
            rgb.save(jpg_path, "JPEG", quality=JPEG_QUALITY, optimize=True)
            path.unlink()  # remove the original .png
            new_size = jpg_path.stat().st_size
            converted_to_jpg.append(path.name)
            print(f"  PNG->JPG {path.name} -> {jpg_path.name}  {original_size//1024}KB -> {new_size//1024}KB")
            continue
        else:
            # Keep as PNG but compress
            img.save(path, "PNG", optimize=True)
            new_size = path.stat().st_size
            compressed_png.append(path.name)
            print(f"  PNG     {path.name}  {original_size//1024}KB -> {new_size//1024}KB")
    else:
        # JPEG or kept PNG
        if path.suffix.lower() in (".jpg", ".jpeg"):
            rgb = img.convert("RGB")
            rgb.save(path, "JPEG", quality=JPEG_QUALITY, optimize=True)
            new_size = path.stat().st_size
            compressed_jpg.append(path.name)
            print(f"  JPG     {path.name}  {original_size//1024}KB -> {new_size//1024}KB")
        else:
            img.save(path, "PNG", optimize=True)
            new_size = path.stat().st_size
            compressed_png.append(path.name)
            print(f"  PNG     {path.name}  {original_size//1024}KB -> {new_size//1024}KB")

print()
print("=== Summary ===")
print(f"JPGs compressed: {len(compressed_jpg)}")
print(f"PNGs kept+compressed: {len(compressed_png)}")
print(f"PNGs converted to JPG: {len(converted_to_jpg)}")
if converted_to_jpg:
    print("FILES RENAMED (update template references):")
    for f in converted_to_jpg:
        print(f"  {f} -> {Path(f).stem}.jpg")
