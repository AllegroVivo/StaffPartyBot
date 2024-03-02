from __future__ import annotations

from typing import TYPE_CHECKING, Type, TypeVar, Tuple, Any

from discord import User

from Utilities import TrainingLevel

if TYPE_CHECKING:
    from Classes import Position, TrainingBot, TrainingManager
################################################################################

__all__ = ("Qualification", )

Q = TypeVar("Q", bound="Qualification")

################################################################################
class Qualification:
    """Represents a user's qualification for a job position.
    
    Attributes:
    -----------
    _manager: :class:`TrainingManager`
        The manager that created this qualification.
    _id: :class:`str`
        The unique identifier for this qualification.
    _position: :class:`Position`
        The position this qualification is for.
    _level: :class:`TrainingLevel`
        The level of training the user has for this position.
    """

    __slots__ = (
        "_manager",
        "_id",
        "_position",
        "_level",
    )

################################################################################
    def __init__(self, mgr: TrainingManager, _id: str, position: Position, level: TrainingLevel) -> None:

        self._manager: TrainingManager = mgr
        self._id: str = _id

        self._position: Position = position
        self._level: TrainingLevel = level

################################################################################
    @classmethod
    def new(cls: Type[Q], mgr: TrainingManager, user: User, position: Position, level: TrainingLevel) -> Q:

        new_id = mgr.bot.database.insert.qualification(mgr.guild_id, user.id, position, level)
        return cls(mgr, new_id, position, level)

################################################################################
    @classmethod
    def load(cls: Type[Q], mgr: TrainingManager, data: Tuple[Any, ...]) -> Q:
        """Load a qualification from a database record.
        
        Parameters:
        -----------
        mgr: :class:`TrainingManager`
            The manager that created this qualification.
        data: Tuple[Any, ...]
            The database record to load.
            
        Returns:
        --------
        :class:`Qualification`
            The loaded qualification instance.
        """

        pos = mgr.guild.position_manager.get_position(data[3])
        return cls(mgr, data[0], pos, TrainingLevel(data[4]))

################################################################################
    @property
    def bot(self) -> TrainingBot:

        return self._manager.bot

################################################################################
    @property
    def id(self) -> str:

        return self._id

################################################################################
    @property
    def position(self) -> Position:

        return self._position

################################################################################
    @property
    def level(self) -> TrainingLevel:

        return self._level

################################################################################
    def update(self, level: TrainingLevel) -> None:
        """Update the user's qualification level.
        
        Parameters:
        -----------
        level: :class:`TrainingLevel`
            The new level of training the user has for this position.
        """

        self._level = level
        self.bot.database.update.qualification(self)

################################################################################
    def delete(self) -> None:
        """Delete this qualification from its user and the database."""

        self.bot.database.delete.qualification(self)

################################################################################
