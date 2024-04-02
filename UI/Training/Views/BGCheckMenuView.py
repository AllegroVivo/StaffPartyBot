from __future__ import annotations

from typing import TYPE_CHECKING, List

from discord import Interaction, User, ButtonStyle

from Assets import BotEmojis
from UI.Common import FroggeView, CloseMessageButton, FroggeButton
from Utilities import edit_message_helper

if TYPE_CHECKING:
    from Classes import BackgroundCheck, BGCheckVenue
################################################################################

__all__ = ("BGCheckMenuView",)

################################################################################
class BGCheckMenuView(FroggeView):

    def __init__(self, user: User, bg_check: BackgroundCheck) -> None:

        super().__init__(user)

        self.bg_check: BackgroundCheck = bg_check

        button_list = [
            EditNamesButton(self.bg_check.names),
            AddVenueButton(self.bg_check.venues),
            RemoveVenueButton(self.bg_check.venues),
            SubmitAndAgreeButton(),
            SubmitAndRejectButton(),
            CloseMessageButton(),
        ]
        for btn in button_list:
            self.add_item(btn)

################################################################################
class EditNamesButton(FroggeButton):

    def __init__(self, names: List[str]) -> None:

        super().__init__(
            label="Change Name",
            disabled=False,
            row=0
        )
        
        self.set_style(names)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.tuser.set_names(interaction)
        self.set_style(self.view.bg_check.names)
        
        await interaction.edit(embed=self.view.tuser.user_status(), view=self.view)

################################################################################
class AddVenueButton(FroggeButton):

    def __init__(self, venues: List[BGCheckVenue]) -> None:

        super().__init__(
            label="Add Experience",
            disabled=False,
            row=0
        )
        
        self.set_style(venues)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.bg_check.add_venue_experience(interaction)
        self.set_style(self.view.bg_check.venues)
        
        await interaction.edit(embed=self.view.bg_check.status(), view=self.view)
        
################################################################################
class RemoveVenueButton(FroggeButton):

    def __init__(self, venues: List[BGCheckVenue]) -> None:

        super().__init__(
            label="Remove Experience",
            disabled=False,
            row=0
        )
        
        self.set_style(venues)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.bg_check.remove_venue_experience(interaction)
        self.set_style(self.view.bg_check.venues)
        
        await edit_message_helper(
            interaction, embed=self.view.bg_check.status(), view=self.view
        )
        
################################################################################
class SubmitAndAgreeButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.primary,
            label="Submit and Agree",
            disabled=False,
            row=1,
            emoji=BotEmojis.ThumbsUp
        )

    async def callback(self, interaction: Interaction) -> None:
        await self.view.bg_check.submit(interaction, True)
        self.view.complete = True

        await edit_message_helper(interaction, view=self.view)
        await self.view.stop()  # type: ignore

################################################################################
class SubmitAndRejectButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.primary,
            label="Submit and Disagree",
            disabled=False,
            row=1,
            emoji=BotEmojis.ThumbsDown
        )

    async def callback(self, interaction: Interaction) -> None:
        await self.view.bg_check.submit(interaction, False)
        self.view.complete = True

        await edit_message_helper(interaction, view=self.view)
        await self.view.stop()  # type: ignore

################################################################################
