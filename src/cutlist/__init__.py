"""Cut-list optimizer: 2D guillotine packing for woodworking."""

from .packer import SheetResult, pack
from .svg import sheet_svg

__all__ = ["SheetResult", "pack", "sheet_svg"]
__version__ = "0.1.0"
