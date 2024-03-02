from __future__ import annotations

from typing import TYPE_CHECKING

from discord import Interaction, User, ButtonStyle
from discord.ui import Button

from UI.Common import FroggeView, CloseMessageButton
from Utilities import edit_message_helper

if TYPE_CHECKING:
    from Classes import PositionManager
################################################################################

__all__ = ("GlobalRequirementsView",)

################################################################################
class GlobalRequirementsView(FroggeView):

    def __init__(self, user: User, manager: PositionManager):
        
        super().__init__(user)
        
        self.manager = manager
        
        button_list = [
            AddRequirementButton(), 
            RemoveRequirementButton(),
            CloseMessageButton()
        ]
        
        for btn in button_list:
            self.add_item(btn)
        
################################################################################
class AddRequirementButton(Button):
    
    def __init__(self):
        
        super().__init__(
            style=ButtonStyle.primary,
            label="Add Global Requirement",
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction: Interaction):
        await self.view.manager.add_global_requirement(interaction)
        await interaction.edit(
            embed=self.view.manager.global_requirements_status(), view=self.view
        )
        
################################################################################
class RemoveRequirementButton(Button):
    
    def __init__(self):
        
        super().__init__(
            style=ButtonStyle.danger,
            label="Remove Global Requirement",
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction: Interaction):
        await self.view.manager.remove_global_requirement(interaction)
        
        await edit_message_helper(
            interaction=interaction,
            embed=self.view.manager.global_requirements_status(),
            view=self.view
        )
        
################################################################################
