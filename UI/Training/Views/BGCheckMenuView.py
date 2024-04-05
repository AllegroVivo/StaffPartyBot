from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Any

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
            ToggleTrainButton(self.bg_check.want_to_train),
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
            label="Edit Names",
            disabled=False,
            row=0
        )
        
        self.set_style(names)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.bg_check.set_names(interaction)
        self.set_style(self.view.bg_check.names)
        
        await interaction.edit(embed=self.view.bg_check.status(), view=self.view)

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
        
        if len(self.view.bg_check.venues) > 0:
            self.view.children[2].disabled = False
        
        await interaction.edit(embed=self.view.bg_check.status(), view=self.view)
        
################################################################################
class RemoveVenueButton(FroggeButton):

    def __init__(self, venues: List[BGCheckVenue]) -> None:

        super().__init__(
            label="Remove Experience",
            disabled=len(venues) == 0,
            row=0
        )
        
        self.set_style(venues)
        
    def set_style(self, attribute: Optional[Any]) -> None:
        
        super().set_style(attribute)
        self.disabled = len(attribute) == 0

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
class ToggleTrainButton(FroggeButton):
    
    def __init__(self, cur_val: bool) -> None:
        
        super().__init__(
            label="I Want to Train Staff",
            disabled=False,
            row=0
        )
        
        self.set_style(cur_val)
        
    def set_style(self, attribute: Optional[Any]) -> None:
        
        if attribute:
            self.style = ButtonStyle.success
            self.emoji = BotEmojis.Check
        else:
            self.style = ButtonStyle.danger
            self.emoji = None

    async def callback(self, interaction: Interaction) -> None:
        self.view.bg_check.toggle_previously_trained()
        self.set_style(self.view.bg_check.want_to_train)

        await interaction.edit(embed=self.view.bg_check.status(), view=self.view)

    ################################################################################
