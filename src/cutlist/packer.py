"""Greedy guillotine 2D packer with best-area-fit placement.

Parts are sorted by area (largest first) and placed into the free rectangle
that leaves the least leftover area. After each placement the remaining
L-shaped space is split guillotine-style into a right strip and a bottom
strip. Parts may rotate 90 degrees. Kerf (saw-blade width) is reserved
around every part.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Rect:
    x: float
    y: float
    w: float
    h: float


@dataclass
class PlacedPart:
    name: str
    x: float
    y: float
    w: float
    h: float
    rotated: bool = False


@dataclass
class SheetResult:
    sheet_w: float
    sheet_h: float
    parts: list = field(default_factory=list)
    _free: list = field(default_factory=list, repr=False)

    @property
    def used_area(self) -> float:
        return sum(p.w * p.h for p in self.parts)

    @property
    def waste_pct(self) -> float:
        total = self.sheet_w * self.sheet_h
        return 100.0 * (total - self.used_area) / total if total else 0.0


def pack(sheet_w, sheet_h, parts, kerf=0.0):
    """Pack parts onto sheets.

    Args:
        sheet_w, sheet_h: stock sheet dimensions.
        parts: iterable of (name, w, h, qty) tuples.
        kerf: blade width reserved around each part (same units).

    Returns:
        List of SheetResult, one per sheet used.

    Raises:
        ValueError: if a part fits on no orientation of the sheet.
    """
    items = []
    for name, w, h, qty in parts:
        items.extend([(name, w, h)] * int(qty))
    items.sort(key=lambda t: t[1] * t[2], reverse=True)

    sheets: list[SheetResult] = []
    for name, w, h in items:
        placed = any(_place_in_sheet(s, name, w, h, kerf) for s in sheets)
        if not placed:
            sheet = SheetResult(sheet_w, sheet_h, _free=[Rect(0, 0, sheet_w, sheet_h)])
            if not _place_in_sheet(sheet, name, w, h, kerf):
                raise ValueError(
                    f"Part {name!r} ({w}x{h}) fits on no orientation of a "
                    f"{sheet_w}x{sheet_h} sheet"
                )
            sheets.append(sheet)
    return sheets


def _place_in_sheet(sheet: SheetResult, name, w, h, kerf) -> bool:
    best = None  # (leftover_area, rect, pw, ph, rotated)
    for r in sheet._free:
        for pw, ph, rotated in ((w, h, False), (h, w, True)):
            if pw <= r.w and ph <= r.h:
                leftover = r.w * r.h - pw * ph
                if best is None or leftover < best[0]:
                    best = (leftover, r, pw, ph, rotated)
    if best is None:
        return False

    _, r, pw, ph, rotated = best
    sheet._free.remove(r)
    sheet.parts.append(PlacedPart(name, r.x, r.y, pw, ph, rotated))

    # Guillotine split of the remaining L-shape: right strip + bottom strip.
    kw, kh = pw + kerf, ph + kerf
    if r.w - kw > 1e-9:
        sheet._free.append(Rect(r.x + kw, r.y, r.w - kw, ph))
    if r.h - kh > 1e-9:
        sheet._free.append(Rect(r.x, r.y + kh, r.w, r.h - kh))
    return True
