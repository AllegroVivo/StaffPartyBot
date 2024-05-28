from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from discord import Interaction, User, ButtonStyle
from discord.ui import View

from Assets import BotEmojis
from UI.Common import FroggeView, CloseMessageButton, FroggeButton
from Utilities import edit_message_helper

if TYPE_CHECKING:
    from Classes import GroupTraining
################################################################################

__all__ = ("GroupTrainingPickupView",)

################################################################################
class GroupTrainingPickupView(View):

    def __init__(self, training: GroupTraining) -> None:

        super().__init__(timeout=None)

        self.group: GroupTraining = training

        button_list = [
            AcceptButton(self.group.id),
            TentativeButton(self.group.id),
        ]
        
        for btn in button_list:
            self.add_item(btn)

################################################################################
class AcceptButton(FroggeButton):

    def __init__(self, group_id: str) -> None:

        super().__init__(
            style=ButtonStyle.success,
            label="Sign-Up",
            disabled=False,
            row=0,
            custom_id=f"{group_id}_accept"
        )

    async def callback(self, interaction: Interaction) -> None:
        await self.view.group.signup(interaction)
        await edit_message_helper(interaction, embed=self.view.group.status())

################################################################################
class TentativeButton(FroggeButton):

    def __init__(self, group_id: str) -> None:

        super().__init__(
            style=ButtonStyle.primary,
            label="Tentative",
            disabled=False,
            row=0,
            custom_id=f"{group_id}_tentative"
        )

    async def callback(self, interaction: Interaction) -> None:
        await self.view.group.tentative_signup(interaction)
        await edit_message_helper(interaction, embed=self.view.group.status())

################################################################################
