from __future__ import annotations

from typing import TYPE_CHECKING, Optional, TypeVar, Dict, Type, List, Any, Tuple

from discord import EmbedField, Interaction, User, Embed, SelectOption
from discord.ext.pages import Page

from Assets import BotEmojis
from UI.Training import TrainerDashboardButtonView, TrainingUpdateView
from Utilities import Utilities as U, RequirementLevel

if TYPE_CHECKING:
    from Classes import Position, TUser, TrainingBot, Requirement
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
    )

################################################################################
    def __init__(
        self,
        _id: str,
        position: Position,
        trainee: TUser,
        trainer: Optional[TUser] = None,
        overrides: Optional[Dict[str, RequirementLevel]] = None
    ) -> None:

        self._id: str = _id
        self._position: Position = position

        self._trainee: TUser = trainee
        self._trainer: Optional[TUser] = trainer

        self._overrides: Dict[str, RequirementLevel] = overrides or {}

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

        return cls(data[0], position, trainee, trainer, overrides)

################################################################################
    def __eq__(self, other: Training) -> bool:

        return self._id == other.id
    
################################################################################
    @property
    def bot(self) -> TrainingBot:

        return self._trainee.bot

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
    def delete(self) -> None:

        self.bot.database.delete.training(self)

################################################################################
    def update(self) -> None:

        self.bot.database.update.training(self)

################################################################################
    async def set_trainer(self, trainer: Optional[TUser]) -> None:

        self._trainer = trainer
        self.update()
        
        confirm = U.make_embed(
            title="Training Updated",
            description=(
                f"Your training for `{self._position.name}` has been\n"
                f"updated with a new trainer.\n\n"
                
                f"Your trainer is now `{self._trainer.name}`!\n\n"
                
                "They will be in touch shortly about your next steps!\n"
                f"{U.draw_line(extra=25)}\n"
            ),
        )
        
        try:
            await self._trainee.user.send(embed=confirm)
        except:
            pass
        
################################################################################
    def status_page(self, owner: User) -> Page:
        
        description = f"**Position:** `{self._position.name}`"
        embed = U.make_embed(
            title=f"Training Status for {self._trainee.name}",
            description=(
                f"{description}\n"
                f"{U.draw_line(text=description)}\n"
            ),
            fields=[self.requirements_status(emoji=True)]
        )
        view = TrainerDashboardButtonView(owner, self)
        
        return Page(embeds=[embed], custom_view=view)
    
################################################################################
    def requirements_status(self, emoji: bool = False) -> EmbedField:
        
        requirements = self._position.manager.global_requirements.copy()
        requirements.extend(self._position.requirements)
        
        value = ""
        for requirement in requirements:
            value += self._requirement_line(emoji, requirement) + "\n"

        return EmbedField(
            name="__Requirements__",
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
        
        for requirement in self._position.requirements:
            # checked = (
            #     requirement.id in self._overrides and 
            #     self._overrides[requirement.id] == RequirementLevel.Complete
            # )
            checked = False
            ret.append(requirement.select_option(checked))
            
        return ret
    
################################################################################
    