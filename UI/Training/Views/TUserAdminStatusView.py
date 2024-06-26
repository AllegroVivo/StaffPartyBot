from __future__ import annotations

from typing import TYPE_CHECKING

from discord import Interaction, User, ButtonStyle
from discord.ui import Button

from UI.Common import FroggeView

if TYPE_CHECKING:
    from Classes import TUser
################################################################################

__all__ = ("TUserAdminStatusView", )

################################################################################        
class TUserAdminStatusView(FroggeView):

    def __init__(self, user: User, tuser: TUser):

        super().__init__(user)

        self.tuser: TUser = tuser

        button_list = [
            EditNameButton(),
            EditNotesButton(),
            ModifyScheduleButton(),
            DataCentersButton(),
            HiatusToggleButton(self.tuser.on_hiatus),
            AddQualificationButton(),
            ModifyQualificationButton(),
            RemoveQualificationButton(),
            AddTrainingButton(),
            RemoveTrainingButton(),
        ]
        for btn in button_list:
            self.add_item(btn)

        self.set_buttons()

################################################################################        
    def set_buttons(self) -> None:

        disable_qualification_btn = len(self.tuser.qualifications) == 0
        disable_training_btn = len(self.tuser.trainings_as_trainee) == 0

        # We can safely access the 'disabled' attribute of the components because
        # we know they are all buttons.
        self.children[6].disabled = disable_qualification_btn
        self.children[7].disabled = disable_qualification_btn
    
        self.children[9].disabled = disable_training_btn

################################################################################
class EditNameButton(Button):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.primary,
            label="Name",
            disabled=False,
            row=0
        )

    async def callback(self, interaction: Interaction) -> None:
        await self.view.tuser.set_name(interaction)
        await interaction.edit(embed=self.view.tuser.admin_status())

################################################################################
class EditNotesButton(Button):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.primary,
            label="Notes",
            disabled=False,
            row=0
        )

    async def callback(self, interaction: Interaction) -> None:
        await self.view.tuser.set_notes(interaction)
        await interaction.edit(embed=self.view.tuser.admin_status())

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
        await self.view.edit_message_helper(interaction, embed=self.view.tuser.admin_status())

################################################################################
class DataCentersButton(Button):
    
    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.primary,
            label="Data Center(s)",
            disabled=False,
            row=0
        )

    async def callback(self, interaction: Interaction) -> None:
        await self.view.tuser.set_data_centers(interaction)
        await self.view.edit_message_helper(interaction, embed=self.view.tuser.admin_status())
        
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
        
        await self.view.edit_message_helper(
            interaction, embed=self.view.tuser.admin_status(), view=self.view
        )
        
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

        await self.view.edit_message_helper(
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

        await self.view.edit_message_helper(
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

        await self.view.edit_message_helper(
            interaction,
            embed=self.view.tuser.admin_status(),
            view=self.view
        )
        
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

        await self.view.edit_message_helper(
            interaction,
            embed=self.view.tuser.admin_status(),
            view=self.view
        )

################################################################################
class RemoveTrainingButton(Button):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.danger,
            label="Remove Training",
            row=2,
        )

    async def callback(self, interaction: Interaction) -> None:
        await self.view.tuser.remove_training(interaction)
        self.view.set_buttons()
        
        await self.view.edit_message_helper(
            interaction, 
            embed=self.view.tuser.admin_status(), 
            view=self.view
        )

################################################################################
