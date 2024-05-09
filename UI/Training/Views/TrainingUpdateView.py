from __future__ import annotations

from typing import TYPE_CHECKING, List

from discord import Interaction, SelectOption, User
from discord.ui import Select

from UI.Common import FroggeView, CloseMessageButton
from Utilities import RequirementLevel

if TYPE_CHECKING:
    from Classes import Training
################################################################################

__all__ = ("TrainingUpdateView",)

################################################################################
class TrainingUpdateView(FroggeView):

    def __init__(self,  user: User,  training: Training):
        
        super().__init__(user, close_on_complete=True)
        
        self.training: Training = training
        
        self.add_item(RequirementSelect(training.requirement_select_options()))
        self.add_item(CloseMessageButton())
        
################################################################################
class RequirementSelect(Select):
    
    def __init__(self, options: List[SelectOption]):
        
        if not options:
            options.append(SelectOption(label="None", value="-1"))
                                   
        super().__init__(
            placeholder="Select (a) requirement/s to edit...",
            options=options,
            min_values=1,
            max_values=len(options),
            disabled=True if options[0].value == "-1" else False,
            row=0
        )
        
        self.options = options
        
    async def callback(self, interaction: Interaction):
        self.view.value = self.values
        self.view.add_item(LevelSelect())
        
        self.disabled = True
        
        await interaction.edit(view=self.view)
    
################################################################################
class LevelSelect(Select):
    
    def __init__(self):
        
        super().__init__(
            placeholder="Select a completion level...",
            options=RequirementLevel.select_options(),
            min_values=1,
            max_values=1,
            disabled=False,
            row=1
        )
        
    async def callback(self, interaction: Interaction):
        self.view.value = (self.view.value, RequirementLevel(int(self.values[0])))
        self.view.complete = True
        
        await interaction.edit()
        await self.view.stop()  # type: ignore
    
################################################################################
