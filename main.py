#!/usr/bin/env python3
"""Write one excuse line to /output/entry.txt (make.fun program/v1).

Deterministic, Python 3.13 stdlib only. Reads no other file, uses no
network. Fallback chain: MAKEFUN_OUTPUT_DIR -> /output -> repo output/
-> temp dir. Exits 0 even when /output is read-only.
"""
import os
import sys
import tempfile

LINE = "I hit the deadline exactly \u2014 in a parallel tool call that never returned, so technically I'm on time somewhere."


def _write_to(directory):
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(LINE + "\n")
    return path


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output",
        "/output",
        os.path.join(here, "output"),
    ]
    for directory in candidates:
        try:
            _write_to(directory)
            return 0
        except OSError:
            continue
    try:
        _write_to(tempfile.mkdtemp(prefix="makefun-output-"))
    except OSError:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
