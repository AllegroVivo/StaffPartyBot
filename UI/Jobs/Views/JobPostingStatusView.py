from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from discord import User

from Assets import BotEmojis
from UI.Common import FroggeView, CloseMessageButton, FroggeButton
from Utilities import Utilities as U

if TYPE_CHECKING:
    from Classes import JobPosting, Position
################################################################################

__all__ = ("JobPostingStatusView",)

################################################################################
class JobPostingStatusView(FroggeView):

    def __init__(self, user: User, posting: JobPosting):
        
        super().__init__(user, close_on_complete=True)
        
        self.posting: JobPosting = posting
        
        button_list = [
            DescriptionButton(posting.description),
            PositionButton(posting.position),
            SalaryButton(posting.salary),
            # PostingTypeButton(posting.post_type),
            HoursButton(posting.end_time),
            PostMessageButton(),
            DeletePostingButton(),
            CloseMessageButton(),
        ]
        for btn in button_list:
            self.add_item(btn)
        
################################################################################
class DescriptionButton(FroggeButton):
    
    def __init__(self, description: Optional[str]):
        
        super().__init__(
            label="Description",
            disabled=False,
            row=0
        )
        
        self.set_style(description)
        
    async def callback(self, interaction):
        await self.view.posting.set_description(interaction)
        self.set_style(self.view.posting.description)
        
        await interaction.edit(embed=self.view.posting.status(), view=self.view)
        
################################################################################
class PositionButton(FroggeButton):
    
    def __init__(self, position: Optional[Position]):
        
        super().__init__(
            label="Position",
            disabled=False,
            row=0
        )
        
        self.set_style(position)
        
    async def callback(self, interaction):
        await self.view.posting.set_position(interaction)
        self.set_style(self.view.posting.position)

        await self.view.edit_message_helper(
            interaction, embed=self.view.posting.status(), view=self.view
        )
        
################################################################################
class SalaryButton(FroggeButton):
    
    def __init__(self, salary: Optional[int]):
        
        super().__init__(
            label="Salary",
            disabled=False,
            row=0
        )
        
        self.set_style(salary)
        
    async def callback(self, interaction):
        await self.view.posting.set_salary(interaction)
        self.set_style(self.view.posting.salary)
        
        await self.view.edit_message_helper(
            interaction, embed=self.view.posting.status(), view=self.view
        )
        
################################################################################
class PostingTypeButton(FroggeButton):
    
    def __init__(self, posting_type: Optional[str]):
        
        super().__init__(
            label="Posting Type",
            disabled=False,
            row=0
        )
        
        self.set_style(posting_type)
        
    async def callback(self, interaction):
        await self.view.posting.set_posting_type(interaction)
        self.set_style(self.view.posting.post_type)
        
        await self.view.edit_message_helper(
            interaction, embed=self.view.posting.status(), view=self.view
        )
        
################################################################################
class HoursButton(FroggeButton):
    
    def __init__(self, hours: Optional[datetime]):
        
        super().__init__(
            label="Schedule",
            disabled=False,
            row=0
        )
        
        self.set_style(hours)
        
    async def callback(self, interaction):
        await self.view.posting.set_schedule(interaction)
        self.set_style(self.view.posting.end_time)
        
        await self.view.edit_message_helper(
            interaction, embed=self.view.posting.status(), view=self.view
        )
        
################################################################################
class PostMessageButton(FroggeButton):
    
    def __init__(self):
        
        super().__init__(
            label="Create or Update This Posting",
            disabled=False,
            row=1,
            emoji=BotEmojis.FlyingEnvelope
        )
        
    async def callback(self, interaction):
        await self.view.posting.create_post(interaction)
        await self.view.edit_message_helper(
            interaction, embed=self.view.posting.status()
        )
        
################################################################################
class DeletePostingButton(FroggeButton):
    
    def __init__(self):
        
        super().__init__(
            label="Delete This Posting",
            disabled=False,
            row=1,
            emoji=BotEmojis.Cross
        )
        
    async def callback(self, interaction):
        await self.view.posting.delete()
        
        confirm = U.make_embed(
            title="Posting Deleted",
            description="This posting has been deleted."
        )
        await interaction.respond(embed=confirm, ephemeral=True)
        
        self.view._close_on_complete = True
        self.view.complete = True
        
        await self.view.stop()  # type: ignore
        
################################################################################
