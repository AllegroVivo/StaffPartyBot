from __future__ import annotations

from typing import Union, Optional

from discord import ButtonStyle, Interaction, Member, User
from discord.ext.pages import Paginator
from discord.ui import Button

from .FroggeView import FroggeView
################################################################################

__all__ = (
    "CloseMessageButton",
    "CloseMessageView",
)

################################################################################
class CloseMessageButton(Button):

    def __init__(self, row: Optional[int] = 4) -> None:
        super().__init__(
            style=ButtonStyle.success,
            label="Close Message",
            disabled=False,
            row=row
        )

    async def callback(self, interaction: Interaction):
        self.view.value = False
        self.view.complete = True
        self.view._close_on_complete = True

        await interaction.response.edit_message()

        if isinstance(self.view, Paginator):
            await self.view.cancel(page=self.view.pages[self.view.current_page])
        else:
            await self.view.stop()  # type: ignore

################################################################################
class CloseMessageView(FroggeView):

    def __init__(self, owner: Union[Member, User]):
        super().__init__(owner, close_on_complete=True)

        self.add_item(CloseMessageButton())

################################################################################
