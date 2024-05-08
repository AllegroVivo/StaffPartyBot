from __future__ import annotations

from discord import Interaction
from typing import TYPE_CHECKING, Optional

from Utilities import GlobalDataCenter

if TYPE_CHECKING:
    from Classes import GuildData, XIVVenue, StaffPartyBot
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
    @property
    def bot(self) -> StaffPartyBot:
        
        return self._parent.bot
    
################################################################################
    async def compile_itinerary(self, interaction: Interaction, region: Optional[str]) -> None:
        
        await interaction.response.defer()

        all_venues = await self.bot.veni_client.get_all_venues()
        await self.bot.report_manager.itinerary_report(interaction, all_venues, region)

################################################################################
    