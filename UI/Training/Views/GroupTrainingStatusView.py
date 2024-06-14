from __future__ import annotations

from datetime import datetime, UTC
from typing import TYPE_CHECKING, Optional

from discord import Interaction, User, ButtonStyle

from Assets import BotEmojis
from Utilities import Utilities as U
from UI.Common import FroggeView, CloseMessageButton, FroggeButton

if TYPE_CHECKING:
    from Classes import GroupTraining
################################################################################

__all__ = ("GroupTrainingStatusView",)

################################################################################
class GroupTrainingStatusView(FroggeView):

    def __init__(self, user: User, training: GroupTraining) -> None:

        super().__init__(user, close_on_complete=True)

        self.group: GroupTraining = training

        button_list = [
            SetTitleButton(self.group.name),
            SetDescriptionButton(self.group.description),
            SetTimesButton(self.group.start_time),
            PostTrainingButton(),
            CompleteTrainingButton(self.group.start_time),
            CloseMessageButton(),
        ]
        
        for btn in button_list:
            self.add_item(btn)

################################################################################
class SetTitleButton(FroggeButton):

    def __init__(self, name: Optional[str]) -> None:

        super().__init__(
            label="Set Title",
            disabled=False,
            row=0
        )
        
        self.set_style(name)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.group.set_title(interaction)
        self.set_style(self.view.group.name)
        
        await interaction.edit(embed=self.view.group.status(), view=self.view)

################################################################################
class SetDescriptionButton(FroggeButton):

    def __init__(self, desc: Optional[str]) -> None:

        super().__init__(
            label="Set Description",
            disabled=False,
            row=0
        )
        
        self.set_style(desc)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.group.set_description(interaction)
        self.set_style(self.view.group.description)
        
        await interaction.edit(embed=self.view.group.status(), view=self.view)

################################################################################
class SetTimesButton(FroggeButton):

    def __init__(self, start_dt: Optional[datetime]) -> None:

        super().__init__(
            label="Set Times",
            disabled=False,
            row=0
        )
        
        self.set_style(start_dt)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.group.set_times(interaction)
        self.set_style(self.view.group.start_time)
        
        await self.view.edit_message_helper(
            interaction, embed=self.view.group.status(), view=self.view
        )

################################################################################
class PostTrainingButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.secondary,
            label="Post Group Training",
            disabled=False,
            row=1,
            emoji=BotEmojis.FlyingEnvelope
        )

    async def callback(self, interaction: Interaction) -> None:
        await self.view.group.post(interaction)
        
        await self.view.edit_message_helper(
            interaction, embed=self.view.group.status(), view=self.view
        )

################################################################################
class CompleteTrainingButton(FroggeButton):

    def __init__(self, start_time: Optional[datetime]) -> None:

        super().__init__(
            style=ButtonStyle.success,
            label="Complete Training",
            # disabled=U.compare_datetimes(start_time, datetime.now()) != -1,
            disabled=False,
            row=1,
            emoji=BotEmojis.Check
        )

    async def callback(self, interaction: Interaction) -> None:
        if await self.view.group.on_complete(interaction):
            self.view.complete = True
            await self.view.stop()  # type: ignore

################################################################################
