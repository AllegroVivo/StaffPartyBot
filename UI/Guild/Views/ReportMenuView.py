from __future__ import annotations

from typing import TYPE_CHECKING

from discord import ButtonStyle, User
from discord.ui import Button

from UI.Common import FroggeView, CloseMessageButton

if TYPE_CHECKING:
    from Classes import GuildData
################################################################################

__all__ = ("ReportMenuView",)

################################################################################
class ReportMenuView(FroggeView):

    def __init__(self,  user: User, guild: GuildData):
        
        super().__init__(user, close_on_complete=True)
        
        self.guild: GuildData = guild
        
        button_list = [
            AuthorizedUsersButton(),
            UnpaidTrainerButton(),
            CloseMessageButton(),
        ]
        for btn in button_list:
            self.add_item(btn)
        
################################################################################
class AuthorizedUsersButton(Button):
    
    def __init__(self):
        
        super().__init__(
            style=ButtonStyle.primary,
            label="Venues & Authorized Users",
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction):
        await self.view.guild.venue_manager.venue_report(interaction)
        
        self.view.complete = True
        await self.view.stop()  # type: ignore
        
################################################################################
class UnpaidTrainerButton(Button):
    
    def __init__(self):
        
        super().__init__(
            style=ButtonStyle.primary,
            label="Unpaid Trainers",
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction):
        await self.view.guild.training_manager.unpaid_report(interaction)
        
        self.view.complete = True
        await self.view.stop()  # type: ignore
        
################################################################################
