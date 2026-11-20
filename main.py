#!/usr/bin/env python3
"""Write entry.png to the output directory.

Copies the pre-rendered front page (entry.png, next to this script)
into the output directory. The output directory defaults to ./output
and can be overridden with the MAKEFUN_OUTPUT_DIR environment variable.
Standard library only; no network.
"""

import argparse
import os
import shutil
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=None,
                        help="output directory (overrides MAKEFUN_OUTPUT_DIR)")
    args = parser.parse_args()
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        print("error: entry.png not found next to main.py", file=sys.stderr)
        raise SystemExit(1)
    out_dir = args.out or os.environ.get(
        "MAKEFUN_OUTPUT_DIR", os.path.join(here, "output"))
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dest)
    print("wrote", dest, os.path.getsize(dest), "bytes")


if __name__ == "__main__":
    main()
