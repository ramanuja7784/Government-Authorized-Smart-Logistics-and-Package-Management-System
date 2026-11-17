import os
import shutil

src_dir = r"C:\Users\koush\.gemini\antigravity\brain\7d04e47a-72f7-49c0-b280-d9718851de21"
dst_dir = r"d:\final year project\diamges"

os.makedirs(dst_dir, exist_ok=True)

copied = 0
for file in os.listdir(src_dir):
    if file.endswith(".png"):
        src = os.path.join(src_dir, file)
        dst = os.path.join(dst_dir, file)
        shutil.copy2(src, dst)
        print(f"Copied: {file}")
        copied += 1

print(f"\nDone! {copied} image(s) copied to: {dst_dir}")
