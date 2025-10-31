#!/usr/bin/env python3

import os
import shlex
import subprocess
import sys

def main():
    if len(sys.argv) != 3:
        print("usage: python artwall.py <art> <preset>")
        print("example: python artwall.py painting color")
        sys.exit(1)

    art = sys.argv[1].lower()
    preset = sys.argv[2].lower()

    if art not in ("painting", "photography"):
        print(f"error: no art named '{art}'")
        sys.exit(1)

    if preset not in ("blur", "color"):
        print(f"error: no preset named '{preset}'")
        sys.exit(1)

    input_file = f"script/config/{art}.txt"
    output_dir = f"work/{art}-{preset}"
    os.makedirs(output_dir, exist_ok=True)

    if not os.path.exists(input_file):
        print(f"error: file '{input_file}' not found")
        sys.exit(1)

    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = shlex.split(line)
            if len(parts) != 3:
                print(f"skipping: {line} in '{input_file}'")
                continue

            path, width, color = parts
            filename = os.path.splitext(os.path.basename(path))[0]
            output_path = os.path.join(output_dir, f"{filename}_{preset}.png")

            if preset == "blur":
                cmd = [
                    "artwall", "blur",
                    path, output_path,
                    "--size", "3840,2160",
                    "--image-width", width,
                    "--blur", "128",
                    "--shadow"
                ]
            elif preset == "color":
                cmd = [
                    "artwall", "color",
                    path, output_path,
                    "--size", "3840,2160",
                    "--image-width", width,
                    "--color", color
                ]
                if art == "painting":
                    cmd += ["--frame-width", "16", "--round", "128"]

            print(" ".join(f'"{c}"' if " " in c else c for c in cmd))

            try:
                subprocess.run(cmd, check=True)
            except subprocess.CalledProcessError as e:
                print(f"error: {e}")

if __name__ == "__main__":
    main()
