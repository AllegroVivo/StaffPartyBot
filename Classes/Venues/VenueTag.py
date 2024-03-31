from __future__ import annotations

from discord import PartialEmoji
from typing import TYPE_CHECKING

from Assets import BotEmojis

if TYPE_CHECKING:
    pass
################################################################################

__all__ = ("VenueTag",)

################################################################################
class VenueTag:

    __slots__ = (
        "_text",
    )
    
################################################################################
    def __init__(self, text: str) -> None:

        self._text: str = text
        
################################################################################
    @property
    def tag_text(self) -> str:
        
        return self._text
    
################################################################################
    @property
    def emoji(self) -> PartialEmoji:
        
        match self._text.lower():
            case _:
                return BotEmojis.Cross
            
################################################################################
    