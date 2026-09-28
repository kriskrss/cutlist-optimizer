# Cutlist Optimizer

2D cut-list optimizer for woodworking: feed it your parts list and sheet size,
get back how many sheets you need, a layout per sheet, the waste %, and an SVG
cut diagram you can print and take to the shop.

The packing core is a greedy **guillotine** algorithm with best-area-fit
placement — simple, fast, and good enough for real shop use. Smarter solvers
(MaxRects, metaheuristics) are on the roadmap.

## Quick start

```bash
pip install -e .
cutlist --sheet 96x48 --kerf 0.125 parts.json -o cuts/
```

`parts.json`:

```json
[
  {"name": "shelf side", "w": 30, "h": 12, "qty": 4},
  {"name": "shelf", "w": 28, "h": 11.5, "qty": 6}
]
```

Or as a library:

```python
from cutlist import pack, sheet_svg

sheets = pack(96, 48, [("shelf side", 30, 12, 4), ("shelf", 28, 11.5, 6)], kerf=0.125)
for i, s in enumerate(sheets):
    print(f"Sheet {i+1}: {len(s.parts)} parts, waste {s.waste_pct:.1f}%")
    open(f"sheet{i+1}.svg", "w").write(sheet_svg(s))
```

Units are whatever you use consistently (inches recommended). Parts may be
rotated 90° to fit; the SVG marks rotated parts.

## Tests

```bash
pip install -e ".[dev]"
pytest
```

## Roadmap

- [x] Greedy guillotine packer + waste % + SVG diagrams + CLI
- [ ] MaxRects packer, A/B compare against greedy
- [ ] Grain direction constraints
- [ ] Web UI (pairs with the Boxwise stack)
- [ ] Publish to PyPI as `cutlist-optimizer`

## Layout

```
src/cutlist/packer.py   packing algorithms
src/cutlist/svg.py      SVG cut-diagram rendering
src/cutlist/cli.py      command-line interface
tests/                  pytest suite
```
