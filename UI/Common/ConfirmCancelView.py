from __future__ import annotations

from typing import TYPE_CHECKING, Union

from discord import ButtonStyle, Interaction, Member, User
from discord.ui import button

from .FroggeView import FroggeView

if TYPE_CHECKING:
    pass
################################################################################

__all__ = ("ConfirmCancelView",)

################################################################################
class ConfirmCancelView(FroggeView):

    def __init__(self, owner: Union[Member, User], *args, **kwargs):
        super().__init__(owner, *args, close_on_complete=True, **kwargs)

    @button(
        style=ButtonStyle.success,
        label="Confirm",
        disabled=False,
        row=0
    )
    async def confirm(self, _, interaction: Interaction):
        self.value = True
        self.complete = True

        await interaction.response.edit_message()
        await self.stop()  # type: ignore

    @button(
        style=ButtonStyle.danger,
        label="Cancel",
        disabled=False,
        row=0
    )
    async def cancel(self, _, interaction: Interaction):
        self.value = False
        self.complete = True

        await interaction.response.edit_message()
        await self.stop()  # type: ignore

################################################################################
