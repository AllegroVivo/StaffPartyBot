from __future__ import annotations

from discord import User, Member
from typing import TYPE_CHECKING, List, Optional, Any, Tuple, Dict

from .Profile import Profile

if TYPE_CHECKING:
    from Classes import GuildData, TrainingBot
################################################################################

__all__ = ("ProfileManager",)

################################################################################
class ProfileManager:
    
    __slots__ = (
        "_state",
        "_profiles"
    )
    
################################################################################
    def __init__(self, guild: GuildData) -> None:
        
        self._state: GuildData = guild
        self._profiles: List[Profile] = []
    
################################################################################
    async def _load_all(self, payload: Dict[str, Any]) -> None:
        
        profiles = []
        for p in payload["profiles"]:       
            if profile := await Profile.load(self, p):
                profiles.append(profile)
                
        self._profiles = profiles
        
        for p in self._profiles:
            await p._update_post_components()
        
################################################################################    
    def __getitem__(self, user_id: int) -> Optional[Profile]:
        
        for p in self._profiles:
            if p.user.id == user_id:
                return p
    
################################################################################
    @property
    def bot(self) -> TrainingBot:
        
        return self._state.bot
    
################################################################################
    @property
    def guild(self) -> GuildData:
        
        return self._state
    
################################################################################
    @property
    def guild_id(self) -> int:
        
        return self._state.parent.id
    
################################################################################
    def create_profile(self, user: User) -> Profile:
        
        # Just double checking we don't add an extra record.
        profile = self[user.id]
        if profile is not None:
            return profile
        
        profile = Profile.new(self, user)
        self._profiles.append(profile)
        
        return profile

################################################################################
    async def on_member_leave(self, member: Member) -> bool:
        
        for profile in self._profiles:
            if profile.user.id == member.id:
                self._profiles.remove(profile)
                return True

################################################################################
    