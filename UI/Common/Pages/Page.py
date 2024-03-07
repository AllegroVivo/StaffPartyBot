from __future__ import annotations

from typing import Optional, List

from discord import Embed, File, InvalidArgument, Interaction
from discord.ui import View
################################################################################

__all__ = ("Page", )

################################################################################
class Page:
    
    __slots__ = (
        "_embeds",
        "_custom_view",
    )
    
################################################################################
    def __init__(self, embeds: List[Embed], custom_view: Optional[View] = None):
        
        if embeds is None:
            raise InvalidArgument("A page may not have embeds equal to None.")
        
        self._embeds = embeds
        self._custom_view = custom_view
        
################################################################################
    async def callback(self, interaction: Optional[Interaction] = None) -> None:
    
        pass

################################################################################
    @property
    def embeds(self) -> List[Embed]:
        
        return self._embeds 
    
################################################################################
    @embeds.setter
    def embeds(self, value: List[Embed]) -> None:
        
        self._embeds = value
        
################################################################################
    @property
    def custom_view(self) -> View:
        
        return self._custom_view

################################################################################    
    @custom_view.setter
    def custom_view(self, value: Optional[View]) -> None:
        
        self._custom_view = value
        
################################################################################
        