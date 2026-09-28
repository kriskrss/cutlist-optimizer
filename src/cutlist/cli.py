"""CLI: cutlist --sheet 96x48 --kerf 0.125 parts.json -o cuts/"""

from __future__ import annotations

import argparse
import json
import os

from .packer import pack
from .svg import sheet_svg


def parse_dims(s: str) -> tuple[float, float]:
    w, h = s.lower().replace(" ", "").split("x")
    return float(w), float(h)


def main() -> None:
    ap = argparse.ArgumentParser(description="2D cut-list optimizer")
    ap.add_argument("parts", help="JSON file: list of {name, w, h, qty}")
    ap.add_argument("--sheet", required=True, help="sheet size, e.g. 96x48")
    ap.add_argument("--kerf", type=float, default=0.0, help="blade width (default 0)")
    ap.add_argument("-o", "--outdir", default="cuts", help="where to write SVGs")
    args = ap.parse_args()

    sheet_w, sheet_h = parse_dims(args.sheet)
    with open(args.parts) as f:
        raw = json.load(f)
    parts = [(p["name"], p["w"], p["h"], p.get("qty", 1)) for p in raw]

    sheets = pack(sheet_w, sheet_h, parts, kerf=args.kerf)
    os.makedirs(args.outdir, exist_ok=True)
    total_parts = 0
    for i, s in enumerate(sheets, 1):
        path = os.path.join(args.outdir, f"sheet{i}.svg")
        with open(path, "w") as f:
            f.write(sheet_svg(s))
        total_parts += len(s.parts)
        print(f"Sheet {i}: {len(s.parts)} parts, waste {s.waste_pct:.1f}% -> {path}")
    print(f"{len(sheets)} sheet(s), {total_parts} parts total")


if __name__ == "__main__":
    main()
