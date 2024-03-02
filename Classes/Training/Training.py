from __future__ import annotations

from typing import TYPE_CHECKING, Optional, TypeVar, Dict, Type, List, Any, Tuple

from Utilities import Utilities as U, RequirementLevel

if TYPE_CHECKING:
    from Classes import Position, TUser, TrainingBot
################################################################################

__all__ = ("Training", )

T = TypeVar("T", bound="Training")

################################################################################
class Training:
    """A class representing a training record in the system.
    
    Attributes:
    -----------
    _id : str
        The unique identifier for the training record.
    _position : :class:`Position`
        The position being trained for.
    _trainee : :class:`Trainee`
        The trainee being trained.
    _trainer : Optional[:class:`Trainer`]
        The trainer for the training.
    _overrides : Dict[:class:`str`, :class:`RequirementLevel`]
        Any overrides for the training requirements.
    """

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
