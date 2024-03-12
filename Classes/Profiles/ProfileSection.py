from __future__ import annotations

from discord import User
from typing import TYPE_CHECKING, List, Any, Optional
from Assets import BotEmojis
if TYPE_CHECKING:
    from Classes import Profile
################################################################################

__all__ = ("ProfileSection",)

################################################################################
class ProfileSection:
    
    __slots__ = (
        "_parent",
    )

################################################################################
    def __init__(self, parent: Profile) -> None:
        
        self._parent: Profile = parent
        
################################################################################
    @property
    def parent(self) -> Profile:
        
        return self._parent
    
################################################################################
    @property
    def user(self) -> User:
        
        return self._parent.user
    
################################################################################
    @property
    def profile_id(self) -> str:
        
        return self._parent.id
    
################################################################################
    @staticmethod
    def progress_emoji(attribute: Optional[Any]) -> str:

        return str(BotEmojis.Cross) if not attribute else str(BotEmojis.Check)

################################################################################
