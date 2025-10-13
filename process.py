import os
import time
import re
from PIL import Image

# Paths
original_folder = 'photos'           # original images
processed_folder = 'photos_processed'  # processed/compressed images

os.makedirs(processed_folder, exist_ok=True)

original_folder = os.path.abspath(original_folder)
processed_folder = os.path.abspath(processed_folder)

image_exts = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.heic'}
MAX_SIZE_KB = 200
timestamp_pattern = re.compile(r'^\d{13}$')

for filename in sorted(os.listdir(original_folder)):
    old_path = os.path.join(original_folder, filename)
    
    if not os.path.isfile(old_path):
        continue

    name, ext = os.path.splitext(filename)
    ext = ext.lower()

    if ext not in image_exts:
        continue

    timestamp_name = f"{int(time.time() * 1000)}"
    new_original_name = f"{timestamp_name}{ext}"
    new_original_path = os.path.join(original_folder, new_original_name)

    os.rename(old_path, new_original_path)

    new_processed_name = f"{timestamp_name}.webp"
    new_processed_path = os.path.join(processed_folder, new_processed_name)

    try:
        with Image.open(new_original_path) as img:
            if img.mode not in ("RGB", "RGBA"):
                img = img.convert("RGB")

            img.save(new_processed_path, format="WEBP", quality=95, method=6)
            final_size = os.path.getsize(new_processed_path) / 1024

            quality = 95
            while final_size > MAX_SIZE_KB and quality > 10:
                quality -= 5
                img.save(new_processed_path, format="WEBP", quality=quality, method=6)
                final_size = os.path.getsize(new_processed_path) / 1024

            original_size = os.path.getsize(new_original_path) / 1024
            print(f"{new_original_name} → {new_processed_name} | Original: {original_size:.2f} KB | Processed: {final_size:.2f} KB | Quality: {quality}")

    except Exception as e:
        print(f"Error processing {new_original_name}: {e}")
        continue

    time.sleep(0.005)

print("\n-> All images renamed in original folder and compressed to processed folder successfully.")