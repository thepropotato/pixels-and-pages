import os
import time
import re

path = 'photos'
path = os.path.abspath(path)

image_exts = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.heic'}

timestamp_pattern = re.compile(r'^\d+$')

for filename in sorted(os.listdir(path)):
    old_path = os.path.join(path, filename)
    
    if not os.path.isfile(old_path):
        continue

    name, ext = os.path.splitext(filename)
    ext = ext.lower()

    if ext not in image_exts:
        continue

    if timestamp_pattern.match(name):
        continue

    new_name = f"{int(time.time() * 1000)}{ext}"
    new_path = os.path.join(path, new_name)

    time.sleep(0.005)

    os.rename(old_path, new_path)
    print(f"Renamed: {filename} → {new_name}")

print("\n-> All non-timestamp image files renamed successfully.")