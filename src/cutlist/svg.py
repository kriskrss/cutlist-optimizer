"""Render a packed sheet as a printable SVG cut diagram."""

from __future__ import annotations

import html


def sheet_svg(sheet, px_per_unit: float = 8.0, margin: float = 40.0) -> str:
    """Return an SVG string showing every placed part on the sheet.

    Rotated parts get a dashed border and an (R) tag.
    """
    W = sheet.sheet_w * px_per_unit + margin * 2
    H = sheet.sheet_h * px_per_unit + margin * 2
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="{H:.0f}" '
        f'viewBox="0 0 {W:.0f} {H:.0f}" font-family="sans-serif">',
        f'<rect x="{margin}" y="{margin}" width="{sheet.sheet_w * px_per_unit:.1f}" '
        f'height="{sheet.sheet_h * px_per_unit:.1f}" fill="#f8fafc" stroke="#0f172a" stroke-width="2"/>',
        f'<text x="{margin}" y="{margin - 12}" font-size="14" font-weight="bold">'
        f"{html.escape(f'{sheet.sheet_w} x {sheet.sheet_h} — waste {sheet.waste_pct:.1f}%')}"
        "</text>",
    ]
    for p in sheet.parts:
        x = margin + p.x * px_per_unit
        y = margin + p.y * px_per_unit
        w = p.w * px_per_unit
        h = p.h * px_per_unit
        dash = ' stroke-dasharray="6,3"' if p.rotated else ""
        label = html.escape(p.name) + (" (R)" if p.rotated else "")
        out.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'fill="#dbeafe" stroke="#1d4ed8" stroke-width="1.5"{dash}/>'
        )
        if w > 60 and h > 18:
            out.append(
                f'<text x="{x + 4:.1f}" y="{y + 16:.1f}" font-size="12">{label}</text>'
                f'<text x="{x + 4:.1f}" y="{y + 32:.1f}" font-size="11" fill="#475569">'
                f"{p.w:g} x {p.h:g}</text>"
            )
    out.append("</svg>")
    return "\n".join(out)
