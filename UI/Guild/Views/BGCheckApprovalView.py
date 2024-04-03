from __future__ import annotations

from typing import TYPE_CHECKING

from discord import ButtonStyle, User
from discord.ui import Button, View

from UI.Common import CloseMessageButton

if TYPE_CHECKING:
    from Classes import TUser
################################################################################

__all__ = ("BGCheckApprovalView",)

################################################################################
class BGCheckApprovalView(View):

    def __init__(self, tuser: TUser):
        
        super().__init__()
        
        self.tuser: TUser = tuser
        
        button_list = [ApproveButton()] if not tuser.bg_check.approved else []
        button_list.append(CloseMessageButton())  # type: ignore
        for btn in button_list:
            self.add_item(btn)
        
################################################################################
class ApproveButton(Button):
    
    def __init__(self):
        
        super().__init__(
            style=ButtonStyle.success,
            label="Approve",
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction):
        await self.view.tuser.bg_check.approve(interaction)
        
        self.view.children = []
        await interaction.edit_original_response(view=self.view)
        
        self.view.complete = True
        self.view.stop()
        
################################################################################
