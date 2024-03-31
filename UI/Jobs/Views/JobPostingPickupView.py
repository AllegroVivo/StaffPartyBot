from __future__ import annotations

from typing import TYPE_CHECKING, List

from discord import User, ButtonStyle
from discord.ui import Button, View

from Assets import BotEmojis
from UI.Common import CloseMessageButton

if TYPE_CHECKING:
    from Classes import JobPosting
################################################################################

__all__ = ("JobPostingPickupView",)

################################################################################
class JobPostingPickupView(View):

    def __init__(self, posting: JobPosting):
        
        super().__init__(timeout=None)
        
        self.posting: JobPosting = posting
        
        button_list: List[Button] = (
            [AcceptButton(posting.id)] if posting.candidate is None 
            else []
        )
        button_list.append(RejectButton(posting.id))
        if self.posting.candidate is not None:
            button_list.append(CancelButton(posting))
        
        for btn in button_list:
            self.add_item(btn)
    
################################################################################
class AcceptButton(Button):
    
    def __init__(self, posting_id: str):
        
        super().__init__(
            style=ButtonStyle.success,
            label="Accept",
            disabled=False,
            row=0,
            emoji=BotEmojis.Check,
            custom_id=f"{posting_id}_accept"
        )
        
    async def callback(self, interaction):
        await self.view.posting.candidate_accept(interaction)       
        
################################################################################
class RejectButton(Button):
    
    def __init__(self, posting_id: str):
        
        super().__init__(
            style=ButtonStyle.primary,
            label="Reject",
            disabled=False,
            row=0,
            emoji=BotEmojis.ThumbsDown,
            custom_id=f"{posting_id}_reject"
        )
        
    async def callback(self, interaction):
        await self.view.posting.reject(interaction)
        
################################################################################
class CancelButton(Button):
    
    def __init__(self, posting: JobPosting):
        
        super().__init__(
            style=ButtonStyle.secondary,
            label="Cancel",
            disabled=False,
            row=0,
            emoji=BotEmojis.Cross,
            custom_id=f"{posting.id}_cancel"
        )
        
        self.user: User = posting.candidate.user
        
    async def callback(self, interaction):
        if interaction.user == self.user:
            await self.view.posting.cancel(interaction)
        
################################################################################
        
        