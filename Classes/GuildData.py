from __future__ import annotations

from typing import TYPE_CHECKING, List, Any, Dict
from discord import Guild, User

from Classes.Profiles.ProfileManager import ProfileManager
from Classes.Positions.PositionManager import PositionManager
from Classes.Training.TrainingManager import TrainingManager
from Classes.Logger import Logger

if TYPE_CHECKING:
    from Classes import TrainingBot, Profile
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
        "_logger",
        "_profile_mgr",
    )

################################################################################
    def __init__(self, bot: TrainingBot, parent: Guild):

        self._state: TrainingBot = bot
        self._parent: Guild = parent
        
        self._logger: Logger = Logger(self)
        
        self._pos_mgr: PositionManager = PositionManager(self)
        self._training_mgr: TrainingManager = TrainingManager(self)
        self._profile_mgr: ProfileManager = ProfileManager(self)

################################################################################
    async def load_all(self, data: Dict[str, Any]) -> None:
        
        await self._logger.load(data["bot_config"][1])
        self._pos_mgr._load_all(data)
        await self._training_mgr._load_all(data)
        await self._profile_mgr._load_all(data)
        
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
    def log(self) -> Logger:
        
        return self._logger
    
################################################################################
    @property
    def position_manager(self) -> PositionManager:

        return self._pos_mgr

################################################################################
    @property
    def training_manager(self) -> TrainingManager:

        return self._training_mgr

################################################################################
    @property
    def profile_manager(self) -> ProfileManager:

        return self._profile_mgr
    
################################################################################
    def get_profile(self, user: User) -> Profile:

        profile = self._profile_mgr[user.id]
        if profile is None:
            profile = self._profile_mgr.create_profile(user)
            
        return profile
    
################################################################################
