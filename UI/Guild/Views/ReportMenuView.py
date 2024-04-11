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
            VenuesButton(),
            UnpaidTrainerButton(),
            PositionsButton(),
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
            label="Venues",
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
            label="Trainer Payments",
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction):
        await self.view.guild.training_manager.unpaid_report(interaction)
        
        self.view.complete = True
        await self.view.stop()  # type: ignore
        
################################################################################
class PositionsButton(Button):
    
    def __init__(self):
        
        super().__init__(
            style=ButtonStyle.primary,
            label="Positions",
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction):
        await self.view.guild.position_manager.positions_report(interaction)
        
        self.view.complete = True
        await self.view.stop()  # type: ignore
        
################################################################################
class TempJobPostingsButton(Button):
    
    def __init__(self):
        
        super().__init__(
            style=ButtonStyle.primary,
            label="Temporary Job Postings",
            disabled=False,
            row=1
        )
        
    async def callback(self, interaction):
        await self.view.guild.jobs_manager.temp_job_report(interaction)
        
        self.view.complete = True
        await self.view.stop()  # type: ignore
        
################################################################################
