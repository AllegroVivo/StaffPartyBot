from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Tuple, Any, List

from .JobPosting import JobPosting

if TYPE_CHECKING:
    from Classes import GuildData
################################################################################

__all__ = ("JobPostingManager",)

################################################################################
class JobPostingManager:
    
    __slots__ = (
        "_guild",
        "_postings",
    )
    
################################################################################
    def __init__(self, guild: GuildData):
        
        self._guild: GuildData = guild
        self._postings: List[JobPosting] = []
        
################################################################################
