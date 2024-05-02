from __future__ import annotations

from typing import TYPE_CHECKING

from discord import ButtonStyle, User
from discord.ui import Button

from UI.Common import FroggeView, CloseMessageButton

if TYPE_CHECKING:
    from Classes import GuildData
################################################################################

__all__ = ("BulkUpdateView",)

################################################################################
class BulkUpdateView(FroggeView):

    def __init__(self,  user: User, guild: GuildData):
        
        super().__init__(user, close_on_complete=True)
        
        self.guild: GuildData = guild
        
        button_list = [
            VenuesButton(),
            ProfilesButton(),
            TempJobPostingsButton(),
            CloseMessageButton(),
        ]
        for btn in button_list:
            self.add_item(btn)
        
################################################################################
class VenuesButton(Button):
    
    def __init__(self):
        
        super().__init__(
            style=ButtonStyle.primary,
            label="Venue Profiles",
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction):
        await self.view.guild.venue_manager.bulk_update(interaction)
        
        self.view.complete = True
        await self.view.stop()  # type: ignore
        
################################################################################
class ProfilesButton(Button):
    
    def __init__(self):
        
        super().__init__(
            style=ButtonStyle.primary,
            label="Staff Profiles",
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction):
        await self.view.guild.profile_manager.bulk_update(interaction)

        self.view.complete = True
        await self.view.stop()  # type: ignore
        
################################################################################
class TempJobPostingsButton(Button):
    
    def __init__(self):
        
        super().__init__(
            style=ButtonStyle.primary,
            label="Temporary Job Postings",
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction):
        await self.view.guild.jobs_manager.bulk_update(interaction)

        self.view.complete = True
        await self.view.stop()  # type: ignore
        
################################################################################
