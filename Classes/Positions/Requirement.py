from __future__ import annotations

from discord import SelectOption
from typing import TYPE_CHECKING, TypeVar, Type, Tuple, Optional

from Assets import BotEmojis
from Utilities import RequirementLevel

if TYPE_CHECKING:
    from Classes import TrainingBot, PositionManager
################################################################################

__all__ = ("Requirement", )

R = TypeVar("R", bound="Requirement")

################################################################################
class Requirement:
    """A class to represent a training requirement for a job position.
    
    Attributes:
    -----------
    _state: :class:`TrainingBot`
        The bot instance that created this object.
    _id: :class:`str`
        The unique identifier for this requirement.
    _parent_id: :class:`str`
        The unique identifier for the position this requirement is associated with.
    _description: :class:`str`
        The description of the requirement.
    """
    
    __slots__ = (
        "_state",
        "_id",
        "_parent_id",
        "_description"
    )
    
################################################################################
    def __init__(self, bot: TrainingBot, _id: str, pos_id: str, description: str) -> None:
        
        self._state: TrainingBot = bot
        
        self._id: str = _id
        self._parent_id: str = pos_id
        self._description: str = description
    
################################################################################
    @classmethod
    def new(cls: Type[R], mgr: PositionManager, position: str, description: str) -> R:

        new_id = mgr.bot.database.insert.requirement(mgr.guild_id, position, description)
        return cls(mgr.bot, new_id, position, description)
    
################################################################################
    @classmethod
    def load(cls: Type[R], bot: TrainingBot, data: Tuple[str, int, str, str]) -> R:

        # (data[1] is the guild_id, which we don't use here.)
        return cls(bot, data[0], data[2], data[3])

################################################################################
    @property
    def id(self) -> str:
        
        return self._id
    
################################################################################
    @property
    def parent_id(self) -> str:
        
        return self._parent_id
    
################################################################################
    @property
    def description(self) -> str:
        
        return self._description
    
################################################################################
    def select_option(self, checked: bool = False) -> SelectOption:
        """Return a SelectOption object for this requirement.
        
        If the description is longer than 50 characters, it will be truncated to
        47 characters and have "..." appended to the end.
        
        Returns:
        --------
        :class:`SelectOption`
            The SelectOption object for this requirement.
        """

        label = self.description if len(self.description) <= 50 else f"{self.description[:47]}..."
        return SelectOption(label=label, value=self.id, default=checked)
        
################################################################################
    def delete(self) -> None:
        """Delete this requirement from the database."""

        self._state.database.delete.requirement(self.id)

################################################################################
    def update(self) -> None:
        """Update this requirement in the database."""

        self._state.database.update.requirement(self)

################################################################################
    def is_complete(self, level: Optional[RequirementLevel]) -> bool:
        
        if level is None:
            return False
        
        pass

################################################################################
