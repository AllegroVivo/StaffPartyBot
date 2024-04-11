from __future__ import annotations

from typing import TYPE_CHECKING

from discord import ButtonStyle
from discord.ui import Button, View

from Utilities import edit_message_helper

if TYPE_CHECKING:
    from Classes import BackgroundCheck
################################################################################

__all__ = ("BGCheckApprovalView",)

################################################################################
class BGCheckApprovalView(View):

    def __init__(self, bg_check: BackgroundCheck):
        
        super().__init__(timeout=None)
        
        self.bg_check: BackgroundCheck = bg_check
        
        button_list = [ApproveButton(bg_check.user_id)] if not bg_check.approved else []
        for btn in button_list:
            if not self.bg_check.approved:
                self.add_item(btn)
        
################################################################################
class ApproveButton(Button):
    
    def __init__(self, user_id: int):
        
        super().__init__(
            style=ButtonStyle.success,
            label="Approve",
            disabled=False,
            row=0,
            custom_id=f"approve_bg_check_{user_id}"
        )
        
    async def callback(self, interaction):
        await self.view.bg_check.approve()
        await edit_message_helper(interaction, view=None)
        self.view.stop()
        
################################################################################
