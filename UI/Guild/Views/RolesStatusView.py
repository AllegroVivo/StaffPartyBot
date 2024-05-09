from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from discord import User, Role

from UI.Common import FroggeView, CloseMessageButton, FroggeButton
from Utilities import RoleType

if TYPE_CHECKING:
    from Classes import RoleManager
################################################################################

__all__ = ("RolesStatusView",)

################################################################################
class RolesStatusView(FroggeView):

    def __init__(self, user: User, roles: RoleManager):
        
        super().__init__(user, close_on_complete=True)
        
        self.roles: RoleManager = roles
        
        button_list = [
            TrainerRoleButton(roles.trainer_main),
            TrainerPendingRoleButton(roles.trainer_pending),
            TrainerHiatusRoleButton(roles.trainer_hiatus),
            StaffMainRoleButton(roles.staff_main),
            StaffUnvalidatedRoleButton(roles.staff_unvalidated),
            VenueManagementButton(roles.venue_management),
            CloseMessageButton(),
        ]
        for btn in button_list:
            self.add_item(btn)
        
################################################################################
class TrainerRoleButton(FroggeButton):
    
    def __init__(self, cur_role: Optional[Role]):
        
        super().__init__(
            label="Main Trainer Role",
            disabled=False,
            row=0
        )
        
        self.set_style(cur_role)
        
    async def callback(self, interaction):
        await self.view.roles.set_role(interaction, RoleType.TrainerMain)
        self.set_style(self.view.roles.trainer_main)
        
        await self.view.edit_message_helper(
            interaction, embed=self.view.roles.status(), view=self.view
        )
        
################################################################################
class TrainerPendingRoleButton(FroggeButton):
    
    def __init__(self, cur_role: Optional[Role]):
        
        super().__init__(
            label="Trainer Pending",
            disabled=False,
            row=0
        )
        
        self.set_style(cur_role)
        
    async def callback(self, interaction):
        await self.view.roles.set_role(interaction, RoleType.TrainerPending)
        self.set_style(self.view.roles.trainer_main)

        await self.view.edit_message_helper(
            interaction, embed=self.view.roles.status(), view=self.view
        )
        
################################################################################
class TrainerHiatusRoleButton(FroggeButton):
    
    def __init__(self, cur_role: Optional[Role]):
        
        super().__init__(
            label="Trainer Hiatus",
            disabled=False,
            row=0
        )
        
        self.set_style(cur_role)
        
    async def callback(self, interaction):
        await self.view.roles.set_role(interaction, RoleType.TrainingHiatus)
        self.set_style(self.view.roles.trainer_hiatus)

        await self.view.edit_message_helper(
            interaction, embed=self.view.roles.status(), view=self.view
        )
        
################################################################################
class StaffMainRoleButton(FroggeButton):
    
    def __init__(self, cur_role: Optional[Role]):
        
        super().__init__(
            label="Staff Main Role",
            disabled=False,
            row=0
        )
        
        self.set_style(cur_role)
        
    async def callback(self, interaction):
        await self.view.roles.set_role(interaction, RoleType.StaffMain)
        self.set_style(self.view.roles.staff_main)

        await self.view.edit_message_helper(
            interaction, embed=self.view.roles.status(), view=self.view
        )
        
################################################################################
class StaffUnvalidatedRoleButton(FroggeButton):
    
    def __init__(self, cur_role: Optional[Role]):
        
        super().__init__(
            label="Staff Unvalidated",
            disabled=False,
            row=1
        )
        
        self.set_style(cur_role)
        
    async def callback(self, interaction):
        await self.view.roles.set_role(interaction, RoleType.StaffNotValidated)
        self.set_style(self.view.roles.staff_unvalidated)

        await self.view.edit_message_helper(
            interaction, embed=self.view.roles.status(), view=self.view
        )
        
################################################################################
class VenueManagementButton(FroggeButton):
    
    def __init__(self, cur_role: Optional[Role]):
        
        super().__init__(
            label="Venue Management",
            disabled=False,
            row=1
        )
        
        self.set_style(cur_role)
        
    async def callback(self, interaction):
        await self.view.roles.set_role(interaction, RoleType.VenueManagement)
        self.set_style(self.view.roles.venue_management)

        await self.view.edit_message_helper(
            interaction, embed=self.view.roles.status(), view=self.view
        )
        
################################################################################
