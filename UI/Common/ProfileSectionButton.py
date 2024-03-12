from __future__ import annotations

from typing import Any, Optional

from discord import ButtonStyle
from discord.ui import Button
################################################################################

__all__ = ("ProfileSectionButton",)

################################################################################
class ProfileSectionButton(Button):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

################################################################################
    def set_style(self, attribute: Optional[Any]) -> None:

        if attribute:
            self.style = ButtonStyle.primary
        else:
            self.style = ButtonStyle.secondary
            
################################################################################
            