from __future__ import annotations

from typing import TYPE_CHECKING, List

from discord import Interaction, SelectOption, User
from discord.ui import Select

from UI.Common import FroggeView, CloseMessageButton

if TYPE_CHECKING:
    pass
################################################################################

__all__ = ("PositionSelectView",)

################################################################################
class PositionSelectView(FroggeView):

    def __init__(self, user: User, options: List[SelectOption], multi_select: bool = False):
        
        super().__init__(user, close_on_complete=True)
        
        self.add_item(PositionSelect(options, multi_select))
        self.add_item(CloseMessageButton())
        
################################################################################
class PositionSelect(Select):
    
    def __init__(self, options: List[SelectOption], multi_select: bool):
        
        if not options:
            options.append(SelectOption(label="None", value="-1"))
                                   
        super().__init__(
            placeholder="Select a position...",
            options=options,
            min_values=1,
            max_values=1 if not multi_select else len(options),
            disabled=True if options[0].value == "-1" else False,
            row=0
        )
        
        self.options = options
        self.multi_select = multi_select
        
    async def callback(self, interaction: Interaction):
        self.view.value = self.values if self.multi_select else self.values[0]
        self.view.complete = True
        
        await self.view.edit_message_helper(interaction, view=self.view)
        await self.view.stop()  # type: ignore
    
################################################################################
