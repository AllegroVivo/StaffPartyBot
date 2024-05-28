from __future__ import annotations

from typing import List

from discord import Interaction, SelectOption, User, ButtonStyle
from discord.ui import Select

from UI.Common import FroggeView, CloseMessageButton, FroggeButton
################################################################################

__all__ = ("GroupTrainingNoShowView",)

################################################################################
class GroupTrainingNoShowView(FroggeView):

    def __init__(self, user: User, trainees: List[SelectOption]):
        
        super().__init__(user, close_on_complete=True)
        
        self.add_item(TraineeSelect(trainees))
        self.add_item(EveryoneShowedUpButton())
        self.add_item(CloseMessageButton())
        
################################################################################
class TraineeSelect(Select):
    
    def __init__(self, options: List[SelectOption]):
        
        if not options:
            options.append(SelectOption(label="None", value="-1"))
        
        super().__init__(
            placeholder="Select any No-Show trainees...",
            options=options,
            min_values=1,
            max_values=len(options),
            disabled=True if options[0].value == "-1" else False,
            row=0
        )
        
        self.options = options
        
    async def callback(self, interaction: Interaction):
        self.view.value = self.values
        self.view.complete = True

        await interaction.edit()
        await self.view.stop()  # type: ignore
    
################################################################################
class EveryoneShowedUpButton(FroggeButton):
    
    def __init__(self):
        
        super().__init__(
            style=ButtonStyle.success,
            label="Everyone Showed Up, There Were 0 No-Shows",
            disabled=False,
            row=1
        )
        
    async def callback(self, interaction: Interaction):
        self.view.value = []
        self.view.complete = True
    
        await interaction.respond("** **", delete_after=0.1)
        await self.view.stop()  # type: ignore
        
################################################################################
    