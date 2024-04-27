from __future__ import annotations

from typing import TYPE_CHECKING, List, Any, Dict, Optional

from discord import Interaction

from .HireableService import HireableService
from .ServiceProfile import ServiceProfile
from UI.Common import ConfirmCancelView
from Utilities import Utilities as U, ServiceNotFoundError

if TYPE_CHECKING:
    from Classes import GuildData, StaffPartyBot
################################################################################

__all__ = ("ServicesManager",)

################################################################################
class ServicesManager:
    
    __slots__ = (
        "_guild",
        "_services",
        "_profiles",
    )
    
################################################################################
    def __init__(self, guild: GuildData):
        
        self._guild: GuildData = guild
        self._services: List[HireableService] = []
        self._profiles: List[ServiceProfile] = []
        
################################################################################
    async def _load_all(self, data: Dict[str, Any]) -> None:
        
        self._services = [await HireableService.load(self, s) for s in data["services"]]
        self._profiles = [
            await ServiceProfile.load(self, p) for p in data["service_profiles"]
        ]
    
################################################################################
    @property
    def bot(self) -> StaffPartyBot:
        
        return self._guild.bot
    
################################################################################
    @property
    def guild(self) -> GuildData:
        
        return self._guild
    
################################################################################
    @property
    def guild_id(self) -> int:
        
        return self._guild.guild_id
    
################################################################################
    def get_service_by_name(self, name: str) -> Optional[HireableService]:
        
        for service in self._services:
            if service.name.lower() == name.lower():
                return service
    
################################################################################
    async def add_service(self, interaction: Interaction, name: str) -> None:
        
        service = self.get_service_by_name(name)
        if service is not None:
            await service.menu(interaction)
            return
        
        prompt = U.make_embed(
            title="Add Service?",
            description=(
                f"Please confirm you would you like to add a new hireable "
                f"service called `{name}`?"
            )
        )
        view = ConfirmCancelView(interaction.user)
        
        await interaction.respond(embed=prompt, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            return
        
        service = HireableService.new(self, name)
        self._services.append(service)
        
        await service.menu(interaction)
        
################################################################################
    async def service_status(self, interaction: Interaction, name: str) -> None:
        
        service = self.get_service_by_name(name)
        if service is None:
            error = ServiceNotFoundError(name)
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        await service.menu(interaction)
    
################################################################################
    