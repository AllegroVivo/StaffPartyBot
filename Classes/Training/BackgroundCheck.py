from __future__ import annotations

from typing import TYPE_CHECKING, List, Type, TypeVar, Any, Tuple

from discord import User

from Utilities import TrainingLevel
from .BGCheckVenue import BGCheckVenue

if TYPE_CHECKING:
    from Classes import Position, TrainingBot, TUser
################################################################################

__all__ = ("BackgroundCheck",)

BC = TypeVar("BC", bound="BackgroundCheck")

################################################################################
class BackgroundCheck:

    __slots__ = (
        "_parent",
        "_agree",
        "_names",
        "_venues",
        "_positions",
        "_approved"
    )

################################################################################
    def __init__(self, parent: TUser, **kwargs) -> None:

        self._parent: TUser = parent
        
        self._agree: bool = kwargs.get("agree", False)
        self._names: List[str] = kwargs.get("names", [])
        self._venues: List[BGCheckVenue] = kwargs.get("venues", [])
        self._positions: List[Position] = kwargs.get("roles", [])
        
        self._approved: bool = kwargs.get("approved", False)

################################################################################
    @classmethod
    def load(cls: Type[BC], parent: TUser, data: Tuple[Any, ...]) -> BC:
        
        return cls(
            parent=parent,
            agree=data[1],
            names=data[2],
            venues=(
                [BGCheckVenue.from_db_string(v) for v in data[3]] 
                if data[3] is not None else None
            ),
            positions=data[4],
            approved=data[5]
        )
    
################################################################################
    @property
    def bot(self) -> TrainingBot:
        
        return self._parent.bot
    
################################################################################
    @property
    def user_id(self) -> int:
        
        return self._parent.user_id
    
################################################################################
    @property
    def parent(self) -> TUser:
        
        return self._parent
    
################################################################################
    @property
    def agree(self) -> bool:
        
        return self._agree
    
    @agree.setter
    def agree(self, value: bool) -> None:
        
        self._agree = value
        self.update()
        
################################################################################
    @property
    def names(self) -> List[str]:
        
        return self._names
    
    @names.setter
    def names(self, value: List[str]) -> None:
        
        self._names = value
        self.update()
        
################################################################################
    @property
    def venues(self) -> List[BGCheckVenue]:
        
        return self._venues
        
################################################################################
    @property
    def positions(self) -> List[Position]:
        
        return self._positions
        
################################################################################
    @property
    def approved(self) -> bool:
        
        return self._approved
    
    @approved.setter
    def approved(self, value: bool) -> None:
        
        self._approved = value
        self.update()
        
################################################################################
    def update(self) -> None:
        
        self.bot.database.update.background_check(self)
        
################################################################################
        