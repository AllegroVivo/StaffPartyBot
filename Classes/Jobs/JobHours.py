from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, TypeVar, Optional

from discord import Embed

from Utilities import Utilities as U

if TYPE_CHECKING:
    from Classes import JobPosting
################################################################################

__all_ = ("JobHours",)

JH = TypeVar("JH", bound="JobHours")

################################################################################
class JobHours:

    __slots__ = (
        "_parent",
        "_start",
        "_end",
    )

################################################################################
    def __init__(
        self,
        parent: JobPosting, 
        start: Optional[datetime] = None, 
        end: Optional[datetime] = None
    ) -> None:

        self._parent: JobPosting = parent

        self._start: Optional[datetime] = start
        self._end: Optional[datetime] = end

################################################################################
    @property
    def parent(self) -> JobPosting:

        return self._parent

################################################################################
    @property
    def job_id(self) -> str:
        
        return self._parent.id
    
################################################################################
    @property
    def start_time(self) -> Optional[datetime]:

        return self._start

################################################################################
    @property
    def end_time(self) -> Optional[datetime]:

        return self._end

################################################################################
    def status(self) -> Embed:
        
        pass
    
################################################################################
    