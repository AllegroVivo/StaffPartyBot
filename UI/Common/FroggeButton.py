from __future__ import annotations

from typing import Any, Optional

from discord import ButtonStyle
from discord.ui import Button
################################################################################

__all__ = ("FroggeButton",)

################################################################################
class FroggeButton(Button):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

################################################################################
    def set_style(self, attribute: Optional[Any]) -> None:
        
        if isinstance(attribute, str):
            attribute = attribute.strip("═")
            attribute = attribute.strip()

        if not attribute or attribute in ("`Not Set`", "Not Set"):
            self.style = ButtonStyle.secondary
        else:
            self.style = ButtonStyle.primary
            
################################################################################
            