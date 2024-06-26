from __future__ import annotations

from typing import List

from discord import Interaction, SelectOption, User
from discord.ui import Select

from UI.Common import FroggeView, CloseMessageButton
################################################################################

__all__ = ("DecoupleTrainingSelectView",)

################################################################################
class DecoupleTrainingSelectView(FroggeView):

    def __init__(self,  user: User,  options: List[SelectOption]):
        
        super().__init__(user, close_on_complete=True)
        
        self.add_item(TrainingSelect(options))
        self.add_item(CloseMessageButton())
        
################################################################################
class TrainingSelect(Select):

    def __init__(self, options: List[SelectOption]):

        super().__init__(
            placeholder="Select a training to decouple...",
            options=options,
            min_values=1,
            max_values=len(options),
            disabled=False,
            row=0
        )

    async def callback(self, interaction: Interaction):
        self.view.value = self.values
        self.view.complete = True

        await interaction.edit()
        await self.view.stop()  # type: ignore

################################################################################
