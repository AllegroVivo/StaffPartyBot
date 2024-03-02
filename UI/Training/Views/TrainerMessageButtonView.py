from __future__ import annotations

from typing import TYPE_CHECKING

from discord import Interaction, ButtonStyle
from discord.ui import Button, View

if TYPE_CHECKING:
    from Classes import SignUpMessage
################################################################################

__all__ = ("TrainerMessageButtonView",)

################################################################################
class TrainerMessageButtonView(View):

    def __init__(self, msg: SignUpMessage):
        
        super().__init__(timeout=None)
        
        self.msg: SignUpMessage = msg
        
        self.add_item(TrainerMessageButton())        
        self.set_disabled()
        
################################################################################
    def set_disabled(self) -> None:
        
        self.children[0].disabled = len(self.msg.training_manager.unmatched_trainings) == 0
        
################################################################################
class TrainerMessageButton(Button):
    
    def __init__(self):
                                   
        super().__init__(
            style=ButtonStyle.success,
            label="Pick Up a Trainee!",
            row=0,
            custom_id="trainer_message_button"
        )
        
    async def callback(self, interaction: Interaction):
        await self.view.msg.acquire_trainee(interaction)
    
################################################################################
