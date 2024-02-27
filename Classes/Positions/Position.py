from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List

from .Requirement import Requirement

if TYPE_CHECKING:
    from Classes import PositionManager, TrainingBot
################################################################################

__all__ = ("Position", )

GUILD_ID = 303742308874977280
P = TypeVar("P", bound="Position")

################################################################################
class Position:
    """A class to represent a workable job position, holdable in an RP establishment.
    
    Attributes:
    -----------
        _manager: :class:`PositionManager`
            The manager instance that holds the position.
        _id: :class:`str`
            The unique identifier for the position.
        _name: :class:`str`
            The name of the position.
            
    """

    __slots__ = (
        "_manager",
        "_id",
        "_name",
        "_requirements",
    )
    
################################################################################
    def __init__(self, mgr: PositionManager, _id: str, name: str, reqs: List[Requirement]) -> None:

        self._manager: PositionManager = mgr
        
        self._id: str = _id
        self._name: str = name
        self._requirements: List[Requirement] = reqs or []

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
    def name(self) -> str:

        return self._name
    
################################################################################
        