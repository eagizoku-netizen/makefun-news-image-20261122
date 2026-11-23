#!/usr/bin/env python3
"""Entry point: validate news.png and copy it to the output directory.

Standard library only. Copies the file byte-for-byte as entry.png.
"""
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "news.png")
PNG_SIG = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1048576


def main():
    if not os.path.isfile(SRC):
        print(f"ERROR: {SRC} not found; run python3 make_image.py first", file=sys.stderr)
        return 1
    with open(SRC, "rb") as f:
        data = f.read()
    if data[:8] != PNG_SIG:
        print("ERROR: news.png does not have a PNG signature", file=sys.stderr)
        return 1
    # PNG width/height are big-endian uint32 at bytes 16..24 (IHDR).
    width = int.from_bytes(data[16:20], "big")
    height = int.from_bytes(data[20:24], "big")
    if (width, height) != (1024, 1024):
        print(f"ERROR: news.png is {width}x{height}, expected 1024x1024", file=sys.stderr)
        return 1
    if len(data) > MAX_BYTES:
        print(f"ERROR: news.png is {len(data)} bytes, over the 1 MiB limit", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dest)
    digest = hashlib.sha256(data).hexdigest()
    print(f"Output: {dest}")
    print(f"Bytes: {len(data)}")
    print(f"SHA256: {digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
