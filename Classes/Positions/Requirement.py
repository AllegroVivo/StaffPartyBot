from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, Type, Tuple

from discord import SelectOption

from Utilities import log

if TYPE_CHECKING:
    from Classes import StaffPartyBot, PositionManager
################################################################################

__all__ = ("Requirement", )

R = TypeVar("R", bound="Requirement")

################################################################################
class Requirement:
    
    __slots__ = (
        "_state",
        "_id",
        "_parent_id",
        "_description"
    )
    
################################################################################
    def __init__(self, bot: StaffPartyBot, _id: str, pos_id: str, description: str) -> None:
        
        self._state: StaffPartyBot = bot
        
        self._id: str = _id
        self._parent_id: str = pos_id
        self._description: str = description
    
################################################################################
    @classmethod
    def new(cls: Type[R], mgr: PositionManager, position: str, description: str) -> R:

        log.info("Training", f"Creating new requirement for position {position} in guild {mgr.guild_id}")

        new_id = mgr.bot.database.insert.requirement(mgr.guild_id, position, description)
        return cls(mgr.bot, new_id, position, description)
    
################################################################################
    @classmethod
    def load(cls: Type[R], bot: StaffPartyBot, data: Tuple[str, int, str, str]) -> R:

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

        label = self.description if len(self.description) <= 50 else f"{self.description[:47]}..."
        return SelectOption(label=label, value=self.id, default=checked)
        
################################################################################
    def delete(self) -> None:

        self._state.database.delete.requirement(self.id)

################################################################################
    def update(self) -> None:

        self._state.database.update.requirement(self)

################################################################################
