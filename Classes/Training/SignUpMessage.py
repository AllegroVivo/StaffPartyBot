from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Tuple, Any, List, Dict

from discord import (
    Message,
    TextChannel, 
    HTTPException,
    NotFound, 
    Interaction, 
    Embed, 
    EmbedField
)

from Utilities import Utilities as U
from UI.Common import ConfirmCancelView
from UI.Training import TrainerMessageButtonView, TrainerSignUpSelectView

if TYPE_CHECKING:
    from Classes import TrainingBot, TrainingManager, PositionManager
################################################################################

__all__ = ("SignUpMessage",)

################################################################################
class SignUpMessage:

    __slots__ = (
        "_manager",
        "_channel",
        "_message",
    )

################################################################################
    def __init__(self, mgr: TrainingManager):

        self._manager: TrainingManager = mgr

        self._channel: Optional[TextChannel] = None
        self._message: Optional[Message] = None

################################################################################
    async def load(self, data: Tuple[Any, ...]) -> None:

        guild_id = data[0]
        channel_id = data[1]
        message_id = data[2]

        if channel_id is None:
            return

        try:
            self._channel = await self.bot.fetch_channel(channel_id)
        except (HTTPException, NotFound):
            self._channel = None
            self._message = None
            self.update(guild_id)
            return

        if message_id is None:
            return

        try:
            self._message = await self._channel.fetch_message(message_id)
        except (HTTPException, NotFound):
            self._message = None
            self.update(guild_id)
            return

        await self.update_components()

################################################################################
    @property
    def bot(self) -> TrainingBot:
        
        return self._manager.bot 
    
################################################################################
    @property
    def training_manager(self) -> TrainingManager:
        
        return self._manager
    
################################################################################
    @property
    def position_manager(self) -> PositionManager:
        
        return self._manager.guild.position_manager
    
################################################################################
    @property
    def channel(self) -> Optional[TextChannel]:
        
        return self._channel

################################################################################
    @property
    def message(self) -> Optional[Message]:
        
        return self._message
    
################################################################################
    @property
    def jump_url(self) -> Optional[str]:
        
        return self._message.jump_url if self._message is not None else None
    
################################################################################
    def update(self, guild_id: int) -> None:
        
        self.bot.database.update.signup_message(guild_id, self)
    
################################################################################
    def status(self) -> Embed:
        
        return U.make_embed(
            title="__TRAINER/TRAINEE MATCHING__",
            description=(
                "This is the sign up message for the trainer/trainee matching system. "
                "If you are a trainer and wish to pick up a trainee, please select the "
                "trainee's name from the selector below.\n\n"

                "Please consider your selection carefully. Once you have selected a "
                "trainee, you will be unable to change your selection without consulting "
                "a member of management.\n"
                f"{U.draw_line(extra=49)}"
            ),
            fields=self.available_trainee_fields(),
        )
    
################################################################################
    def available_trainee_fields(self) -> List[EmbedField]:

        position_dict = { 
            p.name: [] 
            for p in self._manager.guild.position_manager.positions 
        }

        for training in self._manager.unmatched_trainings:
            position_dict[training.position.name].append(training)

        fields = []
        for position_name, trainings in position_dict.items():
            value = ""
            if len(trainings) == 0:
                value = "`No trainees available.`\n"
            else:
                for t in trainings:
                    if t.trainee.on_hiatus:
                        continue
                    dc = (
                        "" if not t.trainee.data_centers 
                        else f" - *({'/'.join([dc.abbreviation for dc in t.trainee.data_centers])})*"
                    )
                    value += f"`{t.trainee.name}`{dc} - {t.trainee.user.mention}\n"

            fields.append(EmbedField(name=position_name, value=value, inline=False))

        return fields

################################################################################
    async def post(self, interaction: Interaction, channel: TextChannel) -> None:

        self._channel = channel
        self.update(interaction.guild_id)
        
        if self._message is not None:
            await self._message.delete()

        view = TrainerMessageButtonView(self)
    
        self._message = await self._channel.send(embed=self.status(), view=view)
        self.bot.add_view(view, message_id=self._message.id)
        
        self.update(interaction.guild_id)
        
        await interaction.respond("Signup message posted.", ephemeral=True)
        
################################################################################
    async def update_components(self) -> None:
        
        if self._channel is None or self._message is None:
            return
        
        view = TrainerMessageButtonView(self)
        self.bot.add_view(view, message_id=self._message.id)
        
        await self._message.edit(embed=self.status(), view=view)

################################################################################
    async def acquire_trainee(self, interaction: Interaction) -> None:
        
        prompt = U.make_embed(
            title="Acquire Trainee",
            description=(
                "Below is a list of all positions for which you are both "
                "qualified, and for which there are trainees available. "
                "Please select the position you would like to acquire a "
                "trainee for."
            )
        )
        
        trainer = self.training_manager[interaction.user.id]
        view = TrainerSignUpSelectView(
            interaction.user, self, [q.position for q in trainer.qualifications]
        )
        
        await interaction.respond(embed=prompt, view=view, ephemeral=True)
        await view.wait()
        
        if not view.complete or view.value is False:
            return
        
        training = self._manager.get_training(view.value[1])
        acquire = U.make_embed(
            title=f"Acquire Trainee __{training.trainee.name}__",
            description=(
                f"Are you sure you want to pick up {training.trainee.name}\n"
                f"has for training as a `{training.position.name}`?\n\n"
                
                "Please keep in mind that changing this later will\n"
                "require administrator intervention.\n"
                f"{U.draw_line(extra=25)}"
            )
        )
        view = ConfirmCancelView(interaction.user)
        
        await interaction.respond(embed=acquire, view=view, ephemeral=True)
        await view.wait()
        
        if not view.complete or view.value is False:
            return
        
        trainer = self._manager[interaction.user.id]
        await training.set_trainer(trainer)
        
        await self.update_components()
        await self._manager.guild.log.training_matched(training)
        
        confirm = U.make_embed(
            title="Trainee Acquired",
            description=(
                f"Congratulations! You have successfully acquired {training.trainee.name} "
                f"({training.trainee.user.mention}) as a trainee for the "
                f"`{training.position.name}` position.\n\n"
                
                "Please reach out to them as soon as possible to begin the training process."
            )
        )
        
        await interaction.respond(embed=confirm, ephemeral=True)
    
################################################################################
