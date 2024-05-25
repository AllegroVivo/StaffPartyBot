from __future__ import annotations

from typing import List, TYPE_CHECKING

from discord import Interaction, SelectOption, User
from discord.ui import Select

from UI.Common import FroggeView, CloseMessageButton

if TYPE_CHECKING:
    from Classes import SignUpMessage, TUser
################################################################################

__all__ = ("AcquireTraineeView",)

################################################################################
class AcquireTraineeView(FroggeView):

    def __init__(self, user: User, msg: SignUpMessage, options: List[SelectOption]):
        
        super().__init__(user)
        
        self.msg: SignUpMessage = msg

        chunk_size = 25
        if len(options) <= chunk_size:
            self.add_item(TraineeSelect(options))
        else:
            for i in range(0, len(options), chunk_size):
                chunk = options[i:i + chunk_size]
                self.add_item(TraineeSelect(chunk))
            
        self.add_item(CloseMessageButton())
        
################################################################################
class TraineeSelect(Select):

    def __init__(self, options: List[SelectOption]):

        if not options:
            options.append(SelectOption(label="None", value="-1"))

        super().__init__(
            placeholder="Select a trainee...",
            options=options,
            min_values=1,
            max_values=1,
            disabled=True if options[0].value == "-1" else False,
            row=0
        )

    async def callback(self, interaction: Interaction):
        trainee_id = int(self.values[0])
        trainee = self.view.msg.training_manager[trainee_id]
        
        options = [
            SelectOption(
                label=training.position.name,
                value=training.id,
            )
            for training in trainee.unmatched_trainings
        ]
        
        self.view.add_item(PositionSelect(options, trainee))

        self.placeholder = [
            option for option in self.options if option.value == self.values[0]
        ][0].label
        self.disabled = True

        await interaction.edit(view=self.view)

################################################################################
class PositionSelect(Select):
    
    def __init__(self, options: List[SelectOption], trainee: TUser):
        
        if not options:
            options.append(SelectOption(label="None", value="-1"))
                                   
        super().__init__(
            placeholder="Select the position(s) to pick up...",
            options=options,
            min_values=1,
            max_values=len(options),
            disabled=True if options[0].value == "-1" else False,
            row=0
        )
        
        self.trainee: TUser = trainee
        
    async def callback(self, interaction: Interaction):
        self.view.value = (self.trainee, self.values)
        self.view.complete = True
        
        await interaction.edit()
        await self.view.stop()  # type: ignore
    
################################################################################
