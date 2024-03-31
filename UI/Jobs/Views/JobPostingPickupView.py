from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from discord import User

from Assets import BotEmojis
from UI.Common import FroggeView, CloseMessageButton, FroggeButton
from Utilities import Utilities as U, edit_message_helper

if TYPE_CHECKING:
    from Classes import JobPosting, Position
################################################################################

__all__ = ("JobPostingStatusView",)

################################################################################
class JobPostingStatusView(FroggeView):

    def __init__(self, user: User, posting: JobPosting):
        
        super().__init__(user, timeout=None, close_on_complete=True)
        
        self.posting: JobPosting = posting
        
        button_list = [
            PickupPostingButton(),
            CloseMessageButton(),
        ]
        for btn in button_list:
            self.add_item(btn)

################################################################################
class PickupPostingButton(FroggeButton):
    
    def __init__(self):
        
        super().__init__(
            label="Oh! Me! I Want This One!",
            disabled=False,
            row=0,
            emoji=BotEmojis.Check
        )
        
    async def callback(self, interaction):
        picked_up = await self.view.posting.pickup(interaction)        
        if picked_up:
            await self.view.stop()  # type: ignore
        
################################################################################
