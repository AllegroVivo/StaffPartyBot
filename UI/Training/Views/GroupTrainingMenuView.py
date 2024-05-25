from __future__ import annotations

from typing import TYPE_CHECKING

from discord import Interaction, User, ButtonStyle
from discord.ui import Button

from UI.Common import FroggeView

if TYPE_CHECKING:
    from Classes import TrainingManager
################################################################################

__all__ = ("GroupTrainingMenuView",)

################################################################################
class GroupTrainingMenuView(FroggeView):

    def __init__(self, user: User, mgr: TrainingManager) -> None:

        super().__init__(user)

        self.mgr: TrainingManager = mgr

        button_list = [
            AddGroupTrainingButton(),
            ModifyGroupTrainingButton(),
            RemoveGroupTrainingButton(),
        ]
        for btn in button_list:
            self.add_item(btn)

################################################################################
class AddGroupTrainingButton(Button):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.primary,
            label="Add New Group Training",
            disabled=False,
            row=0
        )

    async def callback(self, interaction: Interaction) -> None:
        self.view.complete = True
        await self.view.stop()  # type: ignore
        
        await self.view.mgr.add_group_training(interaction)

################################################################################
class ModifyGroupTrainingButton(Button):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.primary,
            label="Modify Existing Group Training",
            disabled=False,
            row=0
        )

    async def callback(self, interaction: Interaction) -> None:
        self.view.complete = True
        await self.view.stop()  # type: ignore

        await self.view.mgr.modify_group_training(interaction)

################################################################################
class RemoveGroupTrainingButton(Button):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.primary,
            label="Remove/Delete Group Training",
            disabled=False,
            row=0
        )

    async def callback(self, interaction: Interaction) -> None:
        self.view.complete = True
        await self.view.stop()  # type: ignore

        await self.view.mgr.remove_group_training(interaction)

################################################################################
