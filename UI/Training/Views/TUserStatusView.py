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
            TogglePingsButton(),
            DataCenterButton(),
            HiatusToggleButton(self.tuser.on_hiatus),
            AddQualificationButton(),
            ModifyQualificationButton(),
            RemoveQualificationButton(),
            AddTrainingButton(),
            RemoveTrainingButton()
        ]
        for btn in button_list:
            self.add_item(btn)
            
        self.set_buttons()

################################################################################        
    def set_buttons(self) -> None:

        disable_buttons = len(self.tuser.trainings_as_trainee) == 0

        # We can safely access the 'disabled' attribute of the components because
        # we know they are all buttons.
        self.children[6].disabled = disable_buttons

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
class DataCenterButton(Button):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.primary,
            label="Data Center",
            disabled=False,
            row=0
        )

    async def callback(self, interaction: Interaction) -> None:
        await self.view.tuser.set_data_centers(interaction)
        await edit_message_helper(interaction, embed=self.view.tuser.admin_status())

################################################################################
class HiatusToggleButton(Button):

    def __init__(self, hiatus: bool) -> None:

        super().__init__(
            disabled=False,
            row=0
        )

        self._set_style(hiatus)

    def _set_style(self, hiatus: bool) -> None:
        if hiatus:
            self.style = ButtonStyle.success
            self.label = "End Hiatus"
        else:
            self.style = ButtonStyle.secondary
            self.label = "Start Hiatus"

    async def callback(self, interaction: Interaction) -> None:
        await self.view.tuser.toggle_hiatus(interaction)
        self._set_style(self.view.tuser.on_hiatus)

        await edit_message_helper(
            interaction, embed=self.view.tuser.user_status(), view=self.view
        )

################################################################################
class TogglePingsButton(Button):
    
    def __init__(self) -> None:
        
        super().__init__(
            style=ButtonStyle.primary,
            label="Toggle Pings",
            disabled=False,
            row=0
        )
    
    async def callback(self, interaction: Interaction) -> None:
        self.view.tuser.toggle_pings()
        await interaction.respond("** **", delete_after=0.1)
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
class AddQualificationButton(Button):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.success,
            label="Add Qualification",
            disabled=False,
            row=1
        )

    async def callback(self, interaction: Interaction) -> None:
        await self.view.tuser.add_qualification(interaction)
        self.view.set_buttons()

        await edit_message_helper(
            interaction,
            embed=self.view.tuser.admin_status(),
            view=self.view
        )

################################################################################
class ModifyQualificationButton(Button):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.primary,
            label="Modify Qualification",
            row=1
        )

    async def callback(self, interaction: Interaction) -> None:
        await self.view.tuser.modify_qualification(interaction)
        self.view.set_buttons()

        await edit_message_helper(
            interaction,
            embed=self.view.tuser.admin_status(),
            view=self.view
        )

################################################################################
class RemoveQualificationButton(Button):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.danger,
            label="Remove Qualification",
            row=1
        )

    async def callback(self, interaction: Interaction) -> None:
        await self.view.tuser.remove_qualification(interaction)
        self.view.set_buttons()

        await edit_message_helper(
            interaction,
            embed=self.view.tuser.admin_status(),
            view=self.view
        )
        
################################################################################
        