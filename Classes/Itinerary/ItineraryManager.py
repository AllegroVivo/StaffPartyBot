from __future__ import annotations

from discord import Interaction
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from Classes import GuildData, XIVVenue
################################################################################

__all__ = ("ItineraryManager", )

################################################################################
class ItineraryManager:

    __slots__ = (
        "_parent",
    )
    
################################################################################
    def __init__(self, parent: GuildData) -> None:

        self._parent: GuildData = parent

################################################################################
    async def compile_itinerary(self, interaction: Interaction, region: Optional[str]) -> None:
        
        pass

################################################################################
    