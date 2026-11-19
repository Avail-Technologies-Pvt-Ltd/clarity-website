#!/usr/bin/env python3
"""
optimize_images.py
High-performance image compressor for Avail Technologies / Clarity Website.
Converts client logos and hardware photography into modern, ultra-lightweight WebP assets.
"""

import os
import sys
from pathlib import Path
from PIL import Image

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / 'static' / 'images'
STATICFILES_DIR = BASE_DIR / 'staticfiles' / 'images'

def optimize_client_logos():
    client_dir = STATIC_DIR / 'clients'
    if not client_dir.exists():
        print(f"[!] Clients directory not found: {client_dir}")
        return

    print("--> Optimizing Client Logos (target: max height 120px, WebP quality 88)...")
    total_orig = 0
    total_opt = 0

    for file_path in client_dir.iterdir():
        if file_path.suffix.lower() not in ('.png', '.jpg', '.jpeg'):
            continue

        orig_size = file_path.stat().st_size
        total_orig += orig_size

        try:
            with Image.open(file_path) as img:
                # Convert color mode appropriately
                if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                    img = img.convert('RGBA')
                else:
                    img = img.convert('RGB')

                # Calculate resize: max height 120px (for 48-52px display @ 2.5x retina)
                w, h = img.size
                if h > 120:
                    new_h = 120
                    new_w = max(1, int(w * (new_h / h)))
                    img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

                webp_name = file_path.stem + '.webp'
                webp_path = client_dir / webp_name
                img.save(webp_path, 'WEBP', quality=88, method=6)

                opt_size = webp_path.stat().st_size
                total_opt += opt_size

                reduction = (1 - (opt_size / orig_size)) * 100
                print(f"  [OK] {file_path.name} ({orig_size/1024:.1f} KB) -> {webp_name} ({opt_size/1024:.1f} KB, -{reduction:.1f}%)")

        except Exception as e:
            print(f"  [ERR] Failed to process {file_path.name}: {e}")

    total_red = (1 - (total_opt / total_orig)) * 100 if total_orig else 0
    print(f"==> Client Logos Summary: {total_orig/1024:.1f} KB -> {total_opt/1024:.1f} KB (-{total_red:.1f}% reduction)\n")


def optimize_hardware_photos():
    hw_dir = STATIC_DIR / 'hardware'
    if not hw_dir.exists():
        print(f"[!] Hardware directory not found: {hw_dir}")
        return

    print("--> Optimizing Hardware Photography (target: max width 800px, WebP quality 82)...")
    total_orig = 0
    total_opt = 0

    for file_path in hw_dir.iterdir():
        if file_path.suffix.lower() not in ('.png', '.jpg', '.jpeg'):
            continue

        orig_size = file_path.stat().st_size
        total_orig += orig_size

        try:
            with Image.open(file_path) as img:
                img = img.convert('RGB')
                w, h = img.size
                if w > 800:
                    new_w = 800
                    new_h = max(1, int(h * (new_w / w)))
                    img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

                webp_name = file_path.stem + '.webp'
                webp_path = hw_dir / webp_name
                img.save(webp_path, 'WEBP', quality=82, method=6)

                opt_size = webp_path.stat().st_size
                total_opt += opt_size

                reduction = (1 - (opt_size / orig_size)) * 100
                print(f"  [OK] {file_path.name} ({orig_size/1024:.1f} KB) -> {webp_name} ({opt_size/1024:.1f} KB, -{reduction:.1f}%)")

        except Exception as e:
            print(f"  [ERR] Failed to process {file_path.name}: {e}")

    total_red = (1 - (total_opt / total_orig)) * 100 if total_orig else 0
    print(f"==> Hardware Photos Summary: {total_orig/1024:.1f} KB -> {total_opt/1024:.1f} KB (-{total_red:.1f}% reduction)\n")


if __name__ == '__main__':
    optimize_client_logos()
    optimize_hardware_photos()
    print("Optimization completed successfully!")
