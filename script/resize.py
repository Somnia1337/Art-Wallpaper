#!/usr/bin/env python3

import os
import sys
import subprocess

def main():
    if len(sys.argv) != 4:
        print("usage: python resize.py <IN_DIR> <OUT_DIR> <NEW_SIZE>")
        print("example: python resize.py wallpaper/painting resized/painting 480x270")
        sys.exit(1)

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    size = sys.argv[3]

    if not os.path.exists(input_dir):
        print(f"error: {input_dir} does not exist")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    supported_exts = (".jpg", ".jpeg", ".png", ".webp", ".tiff")

    for filename in os.listdir(input_dir):
        if not filename.lower().endswith(supported_exts):
            continue

        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)

        cmd = [
            "magick",
            input_path,
            "-resize", size,
            output_path
        ]

        print(" ".join(f'"{c}"' if " " in c else c for c in cmd))
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"error: {e}")

if __name__ == "__main__":
    main()
