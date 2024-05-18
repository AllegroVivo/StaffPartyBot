from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from discord import Interaction

if TYPE_CHECKING:
    from Classes import GuildData, StaffPartyBot
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
    async def compile_itinerary(self, interaction: Interaction, hours: int, region: Optional[str]) -> None:
        
        await interaction.response.defer()

        all_venues = await self.bot.veni_client.get_all_venues()
        await self.bot.report_manager.itinerary_report(interaction, hours, all_venues, region)

################################################################################
    