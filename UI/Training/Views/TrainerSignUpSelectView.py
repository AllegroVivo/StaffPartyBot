from __future__ import annotations

from typing import List, TYPE_CHECKING

from discord import Interaction, SelectOption, User
from discord.ui import Select

from UI.Common import FroggeView, CloseMessageButton

if TYPE_CHECKING:
    from Classes import SignUpMessage, Position
################################################################################

__all__ = ("TrainerSignUpSelectView",)

################################################################################
class TrainerSignUpSelectView(FroggeView):

    def __init__(self,  user: User, msg: SignUpMessage, exclusions: List[Position] = None):
        
        super().__init__(user, close_on_complete=True)
        
        self.msg: SignUpMessage = msg
        
        self.add_item(PositionSelect(msg.position_manager.select_options(exclusions)))
        self.add_item(CloseMessageButton())
        
################################################################################
class PositionSelect(Select):
    
    def __init__(self, options: List[SelectOption]):
        
        if not options:
            options.append(SelectOption(label="None", value="-1"))
                                   
        super().__init__(
            placeholder="Select a position to pick up a trainee for...",
            options=options,
            min_values=1,
            max_values=1,
            disabled=True if options[0].value == "-1" else False,
            row=0
        )
        
    async def callback(self, interaction: Interaction):
        eligible_trainings = self.view.msg.training_manager.get_trainings_for_position(self.values[0])
        training_options = [
            SelectOption(
                label=t.trainee.name,
                value=t.id,
            )
            for t in eligible_trainings
        ]
        if not training_options:
            training_options = [SelectOption(label="No trainees available", value="-1")]
            
        self.view.add_item(TraineeSelect(training_options, self.values[0]))
        
        self.placeholder = [
            option for option in self.options if option.value == self.values[0]
        ][0].label
        self.disabled = True
        
        await interaction.edit(view=self.view)
    
################################################################################
class TraineeSelect(Select):
    
    def __init__(self, options: List[SelectOption], pos_id: str):
        
        super().__init__(
            placeholder=(
                "Select a trainee..." if options[0].value != "-1"
                else "No trainees available..."
            ),
            options=options,
            min_values=1,
            max_values=1,
            disabled=True if options[0].value == "-1" else False,
            row=1
        )

        self.pos_id: str = pos_id
        
    async def callback(self, interaction: Interaction):
        self.view.value = (self.pos_id, self.values[0])
        self.view.complete = True
        
        await interaction.edit()
        await self.view.stop()  # type: ignore
    
################################################################################
