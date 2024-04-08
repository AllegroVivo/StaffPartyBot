from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Any

from discord import Interaction, Role, User, ButtonStyle
from discord.ui import Button

from Assets import BotEmojis
from UI.Common import FroggeView, CloseMessageButton, FroggeButton
from Utilities import edit_message_helper

if TYPE_CHECKING:
    from Classes import Position, GuildData
################################################################################

__all__ = ("PositionStatusView",)

################################################################################
class PositionStatusView(FroggeView):

    def __init__(self, user: User, position: Position):
        
        super().__init__(user)
        
        self.position = position
        
        button_list = [
            PositionNameButton(),  
            PositionRoleButton(self.position.linked_role),
            PositionTrainerPayButton(self.position.trainer_pay),
            ToggleFollowupButton(self.position.followup_included),
            PositionAddReqButton(), 
            PositionRemoveReqButton(),
            CloseMessageButton()
        ]
        for btn in button_list:
            self.add_item(btn)
            
        self.set_button_style()
        
################################################################################        
    def set_button_style(self) -> None:
        
        if len(self.position.requirements) > 0:
            self.children[5].style = ButtonStyle.danger  # type: ignore
            self.children[5].disabled = False  # type: ignore
        else:
            self.children[5].style = ButtonStyle.secondary  # type: ignore
            self.children[5].disabled = True  # type: ignore
            
################################################################################
class PositionNameButton(Button):
    
    def __init__(self):
        
        super().__init__(
            style=ButtonStyle.primary,
            label="Edit Name",
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction: Interaction):
        await self.view.position.edit_name(interaction)
        await interaction.edit(embed=self.view.position.status(), view=self.view)
        
        # If we change the name of a Position, we'll want the signup message 
        # to update as well to reflect that.
        guild: GuildData = interaction.client[interaction.guild_id]  # type: ignore
        await guild.training_manager.signup_message.update_components()
        
################################################################################
class PositionAddReqButton(Button):
    
    def __init__(self):
        
        super().__init__(
            style=ButtonStyle.primary,
            label="Add Requirement",
            disabled=False,
            row=1
        )
        
    async def callback(self, interaction: Interaction):
        await self.view.position.add_requirement(interaction)
        self.view.set_button_style()
        
        await interaction.edit(embed=self.view.position.status(), view=self.view)
        
################################################################################
class PositionRemoveReqButton(Button):
    
    def __init__(self):
        
        super().__init__(
            style=ButtonStyle.danger,
            label="Remove Requirement",
            disabled=False,
            row=1
        )
        
    async def callback(self, interaction: Interaction):
        await self.view.position.remove_requirement(interaction)
        self.view.set_button_style()
        
        await edit_message_helper(
            interaction, embed=self.view.position.status(), view=self.view
        )
        
################################################################################
class PositionRoleButton(FroggeButton):
    
    def __init__(self, cur_role: Optional[Role]):
        
        super().__init__(
            label="Edit Role",
            disabled=False,
            row=0
        )
        
        self.set_style(cur_role)
        
    async def callback(self, interaction):
        await self.view.position.edit_role(interaction)
        self.set_style(self.view.position.linked_role)
        
        await edit_message_helper(
            interaction, embed=self.view.position.status(), view=self.view
        )
        
################################################################################
class PositionTrainerPayButton(FroggeButton):
    
    def __init__(self, trainer_pay: Optional[int]):
        
        super().__init__(
            label="Edit Trainer Pay",
            disabled=False,
            row=0
        )
        
        self.set_style(trainer_pay)
        
    async def callback(self, interaction):
        await self.view.position.set_trainer_pay(interaction)
        self.set_style(self.view.position.trainer_pay)
        
        await interaction.edit(embed=self.view.position.status(), view=self.view)
        
################################################################################
class ToggleFollowupButton(FroggeButton):
    
    def __init__(self, cur_val: bool):
        
        super().__init__(
            label="Follow-Up Incl.",
            disabled=False,
            row=0
        )
        
        self.set_style(cur_val)
        
    def set_style(self, attribute: Optional[Any]) -> None:
        
        if attribute:
            self.style = ButtonStyle.success
            self.emoji = BotEmojis.Check
        else:
            self.style = ButtonStyle.secondary
            self.emoji = None
        
    async def callback(self, interaction: Interaction):
        self.view.position.toggle_followup()
        self.set_style(self.view.position.followup_included) 
        
        await interaction.edit(embed=self.view.position.status(), view=self.view)
        
################################################################################
