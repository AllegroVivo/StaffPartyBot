from __future__ import annotations

from typing import TYPE_CHECKING, Optional, List
from discord import User

from .PayRate import PayRate
from Utilities import JobPostingType

if TYPE_CHECKING:
    from Classes import JobPostingManager, Availability, Position, Venue
################################################################################

__all__ = ("JobPosting",)

################################################################################
class JobPosting:
    
    __slots__ = (
        "_id",
        "_mgr",
        "_venue",
        "_user",
        "_type",
        "_position",
        "_salary",
        "_hours",
        "_description",
    )
    
################################################################################
    def __init__(self, mgr: JobPostingManager, **kwargs) -> None:
        
        self._mgr: JobPostingManager = mgr
        
        self._id: str = kwargs.pop("_id")
        self._venue: Venue = kwargs.pop("venue")
        self._user: User = kwargs.pop("user")
        
        self._type: Optional[JobPostingType] = kwargs.pop("type", None)
        self._position: Optional[Position] = kwargs.pop("position", None)
        self._salary: Optional[PayRate] = kwargs.pop("salary", None)
        self._hours: List[Availability] = kwargs.pop("hours", None) or []
        self._description: Optional[str] = kwargs.pop("description", None)
        
################################################################################
