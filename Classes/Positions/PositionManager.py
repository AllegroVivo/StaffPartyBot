from __future__ import annotations

from typing import TYPE_CHECKING, List

from .Position import Position
from .Requirement import Requirement

if TYPE_CHECKING:
    from Classes import TrainingBot
################################################################################

__all__ = ("PositionManager", )

################################################################################
class PositionManager:
    """A class to manage job positions and position training requirements.
    
    Attributes:
    -----------
    _state : :class:`TrainingBot`
        The bot instance that the manager is associated with.
    _positions : List[:class:`Position`]
        A list of all the positions.
    _requirements : List[:class:`Requirement`]
        A list of all the global training requirements.

    """

    __slots__ = (
        "_state",
        "_positions",
        "_requirements",
    )
    
################################################################################
    def __init__(self, state: TrainingBot) -> None:
    
        self._state: TrainingBot = state
    
        self._positions: List[Position] = []
        self._requirements: List[Requirement] = []
        
################################################################################
        