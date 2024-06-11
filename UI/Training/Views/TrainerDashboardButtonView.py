from __future__ import annotations

from typing import TYPE_CHECKING

from discord import Interaction, User, ButtonStyle
from discord.ui import Button

from UI.Common import FroggeView, CloseMessageButton

if TYPE_CHECKING:
    from Classes import Training
################################################################################

__all__ = ("TrainerDashboardButtonView",)

################################################################################
class TrainerDashboardButtonView(FroggeView):

    def __init__(self,  user: User, training: Training):
        
        super().__init__(user, close_on_complete=True)

        self.add_item(EditTrainingButton(training))
        self.add_item(CloseMessageButton())
        
################################################################################
class EditTrainingButton(Button):
    
    def __init__(self, training: Training):

        super().__init__(
            style=ButtonStyle.primary,
            label="Edit Training",
            disabled=False,
            row=0
        )
        
        self.training: Training = training
        
    async def callback(self, interaction: Interaction):
        await self.training.set_requirements(interaction)
        
        await self.view.message.delete()
        # We can get this since we know the parent view is a Paginator.
        current_page = self.view.current_page  # type: ignore
        await self.training.trainer.refresh_dashboard(interaction, current_page)
    
################################################################################
