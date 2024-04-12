from __future__ import annotations

from typing import List, TYPE_CHECKING

from discord import Interaction, SelectOption, User, ButtonStyle
from discord.ui import Button

from UI.Common import FroggeView, CloseMessageButton
from Utilities import TrainingLevel

if TYPE_CHECKING:
    from Classes import TUser
################################################################################

__all__ = ("ManageTrainingsView",)

################################################################################
class ManageTrainingsView(FroggeView):

    def __init__(self,  user: User, trainee: TUser, trainer: TUser):
        
        super().__init__(user, close_on_complete=True)
        
        self.add_item(ManageTrainingsButton(trainee, trainer))
        
################################################################################
class ManageTrainingsButton(Button):
    
    def __init__(self, trainee: TUser, trainer: TUser):
                                   
        super().__init__(
            style=ButtonStyle.primary,
            label="Manage Trainings",
            disabled=False,
            row=0
        )
        
        self.trainee: TUser = trainee
        self.trainer: TUser = trainer
        
    async def callback(self, interaction: Interaction):
        await self.trainee._select_training_to_decouple(interaction)
        
        await self.view.cancel(page=self.view.pages[0])
        await interaction.message.delete()
        
        await self.trainer.manage_trainings(interaction)

################################################################################
