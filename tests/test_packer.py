import pytest

from cutlist import pack


def test_single_sheet_packs_cleanly():
    sheets = pack(96, 48, [("panel", 24, 24, 8)])
    assert len(sheets) == 1
    assert len(sheets[0].parts) == 8
    assert sheets[0].waste_pct == pytest.approx(0.0)


def test_oversize_part_raises():
    with pytest.raises(ValueError):
        pack(48, 48, [("too big", 60, 10, 1)])


def test_kerf_increases_sheet_count_or_waste():
    no_kerf = pack(48, 48, [("p", 24, 24, 4)], kerf=0.0)
    with_kerf = pack(48, 48, [("p", 24, 24, 4)], kerf=1.0)
    assert with_kerf[0].waste_pct >= no_kerf[0].waste_pct


def test_rotation_used_when_needed():
    sheets = pack(30, 60, [("tall", 50, 20, 1)])
    assert len(sheets) == 1
    assert sheets[0].parts[0].rotated is True


def test_parts_never_overlap_sheet_bounds():
    sheets = pack(96, 48, [("a", 30, 12, 6), ("b", 17, 9, 10), ("c", 44, 20, 2)], kerf=0.125)
    for s in sheets:
        for p in s.parts:
            assert p.x + p.w <= s.sheet_w + 1e-9
            assert p.y + p.h <= s.sheet_h + 1e-9
