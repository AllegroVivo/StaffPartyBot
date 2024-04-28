from __future__ import annotations

from typing import TYPE_CHECKING, Optional, TypeVar, Dict, Type, List, Any, Tuple

from discord import EmbedField, Interaction, User, Embed, SelectOption
from discord.ext.pages import Page

from Assets import BotEmojis
from UI.Training import TrainerDashboardButtonView, TrainingUpdateView
from Utilities import Utilities as U, RequirementLevel, RoleType

if TYPE_CHECKING:
    from Classes import Position, TUser, StaffPartyBot, Requirement, TrainingManager
################################################################################

__all__ = ("Training", )

T = TypeVar("T", bound="Training")

################################################################################
class Training:

    __slots__ = (
        "_id",
        "_position",
        "_trainee",
        "_trainer",
        "_overrides",
        "_paid",
    )

################################################################################
    def __init__(
        self,
        _id: str,
        position: Position,
        trainee: TUser,
        trainer: Optional[TUser] = None,
        overrides: Optional[Dict[str, RequirementLevel]] = None,
        paid: bool = False
    ) -> None:

        self._id: str = _id
        self._position: Position = position

        self._trainee: TUser = trainee
        self._trainer: Optional[TUser] = trainer

        self._overrides: Dict[str, RequirementLevel] = overrides or {}
        self._paid: bool = paid

################################################################################
    @classmethod
    def new(cls: Type[T], trainee: TUser, position_id: str) -> T:

        new_id = trainee.bot.database.insert.training(trainee.guild_id, trainee.user_id, position_id)
        position = trainee.guild.position_manager.get_position(position_id)
        
        return cls(new_id, position, trainee)
    
################################################################################
    @classmethod
    def load(
        cls: Type[T],
        trainee: TUser,
        data: Tuple[Any, ...],
        override_data: List[Tuple[Any, ...]]
    ) -> T:

        position = trainee.position_manager.get_position(data[3])
        trainer = trainee.training_manager[data[4]]

        overrides = {
            requirement_id: RequirementLevel(level)
            for requirement_id, level in override_data
        }

        return cls(data[0], position, trainee, trainer, overrides, data[5])

################################################################################
    def __eq__(self, other: Training) -> bool:

        return self._id == other.id
    
################################################################################
    @property
    def bot(self) -> StaffPartyBot:

        return self._trainee.bot

################################################################################
    @property
    def manager(self) -> TrainingManager:
        
        return self._trainee.training_manager
    
################################################################################
    @property
    def id(self) -> str:

        return self._id

################################################################################
    @property
    def user_id(self) -> int:

        return self._trainee.user_id

################################################################################
    @property
    def position(self) -> Position:

        return self._position

################################################################################
    @property
    def requirement_overrides(self) -> Dict[str, RequirementLevel]:

        return self._overrides

################################################################################
    @property
    def trainee(self) -> TUser:

        return self._trainee

################################################################################
    @property
    def trainer(self) -> Optional[TUser]:

        return self._trainer

################################################################################
    @property
    def trainer_paid(self) -> bool:
        
        return self._paid
    
    @trainer_paid.setter
    def trainer_paid(self, value: bool) -> None:
        
        self._paid = value
        self.update()
        
################################################################################
    @property
    def is_complete(self) -> bool:
        
        return (
            0 < len(self._position.all_requirements) == len(self._overrides)
            and all(
                level == RequirementLevel.Complete
                for level in self._overrides.values()
            )
        )
    
################################################################################
    def delete(self) -> None:

        self.bot.database.delete.training(self)
        self.manager._trainings.remove(self)

################################################################################
    def update(self) -> None:

        self.bot.database.update.training(self)

################################################################################
    async def set_trainer(self, trainer: Optional[TUser]) -> None:

        prev_trainer = self.trainer
        self._trainer = trainer
        self.update()
        
        if trainer is None:
            confirm = U.make_embed(
                title="Training Updated",
                description=(
                    f"Due to unforeseen circumstances, your trainer "
                    f"`{prev_trainer.name}` ({prev_trainer.user.mention}) has "
                    f"canceled their training with you. But don't worry, "
                    f"you don't have to take any actions. You will receive "
                    f"a message when another trainer picks up the training."
                )
            )
        else:
            confirm = U.make_embed(
                title="Training Updated",
                description=(
                    f"Your training for `{self._position.name}` has been\n"
                    f"updated with a new trainer.\n\n"
                    
                    f"Your trainer is now `{self._trainer.name}` "
                    f"({self._trainer.user.mention})!\n\n"
                    
                    "They will be in touch shortly about your next steps!\n"
                    f"{U.draw_line(extra=25)}\n"
                ),
            )
        
        try:
            await self._trainee.user.send(embed=confirm)
        except:
            pass
        
        if trainer is None:
            trainer_confirm = U.make_embed(
                title="Training Updated",
                description=(
                    f"Your training for `{self._position.name}` with\n"
                    f"{self._trainee.name} has been canceled."
                )
            )
            await prev_trainer.send(embed=trainer_confirm)
        
################################################################################
    def status_page(self, owner: User) -> Page:
        
        trainee_availability = self._trainee._availability_field(True)
        trainee_availability.name = "__Trainee Availability__"
        
        description = f"**Position:** `{self._position.name}`"
        embed = U.make_embed(
            title=f"Training Status for {self._trainee.name}",
            description=(
                f"{description}\n"
                f"{U.draw_line(text=description)}\n"
            ),
            fields=[
                trainee_availability,
                self._trainee._dc_field(),
                self.requirements_status(emoji=True),
            ]
        )
        view = TrainerDashboardButtonView(owner, self)
        
        return Page(embeds=[embed], custom_view=view)
    
################################################################################
    def requirements_status(self, emoji: bool = False) -> EmbedField:
        
        requirements = self.position.requirements.copy()
        value = ""
        for requirement in requirements:
            value += self._requirement_line(emoji, requirement) + "\n"
        for req in self._position.manager.global_requirements:
            if req not in requirements:
                value += self._requirement_line(emoji, req) + " - *(Global)*\n"

        return EmbedField(
            name="__Position Training Requirements__",
            value=value,
            inline=False
        )
    
################################################################################    
    def _requirement_line(self, emoji: bool, requirement: Requirement) -> str:
        
        override = self.get_override(requirement.id)
        
        em = ""
        if emoji:
            match override:
                case RequirementLevel.Complete:
                    em = BotEmojis.Check
                case RequirementLevel.InProgress:
                    em = BotEmojis.Construction
                case _:
                    em = BotEmojis.Cross
        
        value = requirement.description
        if override is RequirementLevel.Complete:
            value = f"~~{value}~~"
        
        return f"{em}- {value}"

################################################################################
    async def set_requirements(self, interaction: Interaction) -> None:
        
        embed = self.status()
        view = TrainingUpdateView(interaction.user, self)
        
        await interaction.respond(embed=embed, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            return
        
        req_ids = view.value[0]
        level = view.value[1]
        
        for _id in req_ids:
            self._overrides[_id] = level
        self.update()
        
        if self.is_complete:
            await self.on_complete(interaction)
    
################################################################################
    def get_override(self, req_id: str) -> Optional[RequirementLevel]:
        
        return self._overrides.get(req_id, None)
    
################################################################################
    def status(self) -> Embed:
        
        return U.make_embed(
            title=f"Training Detail",
            description=(
                f"**Trainee:** {self._trainee.name}\n"
                f"**Position:** `{self._position.name}`\n"
                f"{U.draw_line(extra=25)}"
            ),
            fields=[self.requirements_status()]
        )
    
################################################################################
    def requirement_select_options(self) -> List[SelectOption]:
        
        ret = []
        
        for requirement in self._position.all_requirements:
            # checked = (
            #     requirement.id in self._overrides and 
            #     self._overrides[requirement.id] == RequirementLevel.Complete
            # )
            ret.append(requirement.select_option())
            
        return ret
    
################################################################################
    def reset(self) -> None:
        
        self._trainer = None
        self._overrides = {}
        
        self.update()

################################################################################
    async def on_complete(self, interaction: Interaction) -> None:

        trainer_embed = U.make_embed(
            title="Training Complete",
            description=(
                f"Congratulations! Your trainee has completed their training\n"
                f"for the position of `{self._position.name}`!\n\n"

                f"This training will now be marked as closed and taken off "
                f"your roster.\n\n"

                "**Thank you for your hard work and dedication to the program!**\n\n"
                f"{U.draw_line(extra=35)}\n"
            ),
        )
        await interaction.respond(embed=trainer_embed)

        trainee_embed = U.make_embed(
            title="Training Complete",
            description=(
                f"Congratulations! You have completed your training for\n"
                f"the position of `{self._position.name}`!\n\n"

                "__**You are now ready to take on your new role!**__\n\n"
                
                "Visit the server and use the `/trainee match` command to find venues "
                "who can offer you a temporary internship! (The goal of these is to give "
                "you on-site training without any risk or obligation on your part.)\n\n"
                
                "Additionally, you need to run the `/staffing profile` "
                "command to set up your profile! (Follow the instructions "
                "at https://discord.com/channels/1104515062187708525/1219788797223374938 "
                "to get started!)\n\n"
                f"{U.draw_line(extra=25)}\n"
            ),
        )
        
        await self.trainee.send(embed=trainee_embed)
        await self.manager.guild.role_manager.add_role(
            self.trainee.user, RoleType.StaffMain 
        )
        
        if self.trainee.profile.post_message is not None:
            await self.manager.guild.role_manager.add_role_manual(
                self.trainee.user, self.position.linked_role
            )
    
################################################################################
