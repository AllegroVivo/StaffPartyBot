from __future__ import annotations

from typing import TYPE_CHECKING

from discord import Interaction, User, ButtonStyle
from discord.ui import Button

from UI.Common import FroggeView
from Utilities import edit_message_helper

if TYPE_CHECKING:
    from Classes import TUser
################################################################################

__all__ = ("TUserStatusView", )

################################################################################
class TUserStatusView(FroggeView):

    def __init__(self, user: User, tuser: TUser) -> None:

        super().__init__(user)

        self.tuser: TUser = tuser

        button_list = [
            EditNameButton(),
            ModifyScheduleButton(),
            AddTrainingButton(),
            RemoveTrainingButton()
        ]
        for btn in button_list:
            self.add_item(btn)
            
        self.set_buttons()

################################################################################        
    def set_buttons(self) -> None:

        disable_buttons = len(self.tuser.trainings) == 0

        # We can safely access the 'disabled' attribute of the components because
        # we know they are all buttons.
        self.children[3].disabled = disable_buttons

################################################################################
class EditNameButton(Button):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.primary,
            label="Change Name",
            disabled=False,
            row=0
        )

    async def callback(self, interaction: Interaction) -> None:
        await self.view.tuser.set_name(interaction)
        await interaction.edit(embed=self.view.tuser.user_status())

################################################################################
class ModifyScheduleButton(Button):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.primary,
            label="Edit Availability",
            disabled=False,
            row=0
        )

    async def callback(self, interaction: Interaction) -> None:
        await self.view.tuser.set_availability(interaction)
        await edit_message_helper(interaction, embed=self.view.tuser.user_status())

################################################################################
class AddTrainingButton(Button):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.success,
            label="Request Training",
            row=2
        )

    async def callback(self, interaction: Interaction) -> None:
        await self.view.tuser.add_training(interaction)
        self.view.set_buttons()

        await edit_message_helper(interaction, embed=self.view.tuser.user_status(), view=self.view)

################################################################################
class RemoveTrainingButton(Button):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.danger,
            label="Remove Training",
            row=2
        )

    async def callback(self, interaction: Interaction) -> None:
        await self.view.tuser.remove_training(interaction)
        self.view.set_buttons()

        await edit_message_helper(interaction, embed=self.view.tuser.user_status(), view=self.view)

################################################################################
