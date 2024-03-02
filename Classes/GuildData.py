from __future__ import annotations

from typing import TYPE_CHECKING, List, Any, Dict
from discord import Guild

from Classes.Positions.PositionManager import PositionManager
from Classes.Training.TrainingManager import TrainingManager

if TYPE_CHECKING:
    from Classes import TrainingBot
################################################################################

__all__ = ("GuildData",)

################################################################################
class GuildData:
    """A container for bot-specific guild data and settings."""

    __slots__ = (
        "_state",
        "_parent",
        "_pos_mgr",
        "_training_mgr",
    )

################################################################################
    def __init__(self, bot: TrainingBot, parent: Guild):

        self._state: TrainingBot = bot
        self._parent: Guild = parent
        
        self._pos_mgr: PositionManager = PositionManager(self)
        self._training_mgr: TrainingManager = TrainingManager(self)

################################################################################
    async def load_all(self, data: Dict[str, Any]) -> None:
        
        self._pos_mgr._load_all(data)
        await self._training_mgr._load_all(data)
        
################################################################################
    @property
    def bot(self) -> TrainingBot:
        
        return self._state
    
################################################################################
    @property
    def parent(self) -> Guild:
        
        return self._parent
    
################################################################################
    @property
    def guild_id(self) -> int:
        
        return self._parent.id
    
################################################################################
    @property
    def position_manager(self) -> PositionManager:

        return self._pos_mgr

################################################################################
    @property
    def training_manager(self) -> TrainingManager:

        return self._training_mgr

################################################################################
