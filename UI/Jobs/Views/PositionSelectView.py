from __future__ import annotations

from typing import TYPE_CHECKING, List

from discord import Interaction, SelectOption, User
from discord.ui import Select

from UI.Common import FroggeView, CloseMessageButton
from Utilities import TrainingLevel

if TYPE_CHECKING:
    pass
################################################################################

__all__ = ("PositionSelectView",)

################################################################################
class PositionSelectView(FroggeView):

    def __init__(self,  user: User,  options: List[SelectOption]):
        
        super().__init__(user, close_on_complete=True)
        
        self.add_item(PositionSelect(options))
        self.add_item(CloseMessageButton())
        
################################################################################
class PositionSelect(Select):
    
    def __init__(self, options: List[SelectOption]):
        
        if not options:
            options.append(SelectOption(label="None", value="-1"))
                                   
        super().__init__(
            placeholder="Select a position for this job posting...",
            options=options,
            min_values=1,
            max_values=1,
            disabled=True if options[0].value == "-1" else False,
            row=0
        )
        
        self.options = options
        
    async def callback(self, interaction: Interaction):
        self.view.value = self.values[0]
        self.view.complete = True
        
        await interaction.edit(view=self.view)
        await self.view.stop()  # type: ignore
    
################################################################################
