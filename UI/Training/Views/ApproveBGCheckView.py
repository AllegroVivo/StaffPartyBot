from __future__ import annotations

from typing import TYPE_CHECKING, List

from discord import Interaction, User, ButtonStyle

from Assets import BotEmojis
from UI.Common import FroggeView, CloseMessageButton, FroggeButton
from Utilities import edit_message_helper

if TYPE_CHECKING:
    from Classes import BackgroundCheck, BGCheckVenue
################################################################################

__all__ = ("ApproveBGCheckView",)

################################################################################
class ApproveBGCheckView(FroggeView):

    def __init__(self, user: User, bg_check: BackgroundCheck) -> None:

        super().__init__(user)

        self.bg_check: BackgroundCheck = bg_check

        button_list = [
            AcceptBGCheckButton(),
            CloseMessageButton(),
        ]
        for btn in button_list:
            self.add_item(btn)

################################################################################
class AcceptBGCheckButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.success,
            label="Approve User",
            disabled=False,
            row=0
        )

    async def callback(self, interaction: Interaction) -> None:
        await self.view.bg_check.approve()
        self.view.complete = True
        
        await edit_message_helper(interaction, view=None)
        await self.view.stop()  # type: ignore

################################################################################
