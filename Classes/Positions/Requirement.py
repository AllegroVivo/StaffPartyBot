from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from Classes import TrainingBot
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
