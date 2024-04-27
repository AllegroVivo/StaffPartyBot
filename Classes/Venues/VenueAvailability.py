from __future__ import annotations

from datetime import time
from typing import TYPE_CHECKING, List, Optional, Any, Dict, Type, TypeVar, Tuple

from discord import User

from .InternshipManager import InternshipManager
from Utilities import Utilities as U, Weekday

if TYPE_CHECKING:
    from Classes import StaffPartyBot, VenueManager, VenueURLs
################################################################################

__all__ = ("VenueAvailability",)

VA = TypeVar("VA", bound="VenueAvailability")

################################################################################
class VenueAvailability:

    __slots__ = (
        "_parent",
        "_weekday",
        "_open",
        "_close",
    )

################################################################################
    def __init__(
        self,
        parent: VenueURLs,
        weekday: Weekday,
        open_time: time,
        close_time: time,
    ) -> None:
        
        self._parent: VenueURLs = parent
        
        self._weekday: Weekday = weekday
        self._open: time = open_time
        self._close: time = close_time
    
################################################################################
    @classmethod
    def new(cls: Type[VA], parent: VenueURLs, weekday: Weekday, open_time: time, close_time: time) -> VA:
        
        parent.bot.database.insert.venue_hours(parent, weekday, open_time, close_time)
        return cls(parent, weekday, open_time, close_time)
    
################################################################################
    @classmethod
    def load(cls: Type[VA], parent: VenueURLs, data: Tuple[Any, ...]) -> VA:
        
        return cls(parent, Weekday(data[2]), data[3], data[4])
    
################################################################################
    @property
    def bot(self) -> StaffPartyBot:
        
        return self._parent.bot
    
################################################################################    
    @property
    def venue_id(self) -> str:
        
        return self._parent.venue_id
    
################################################################################
    @property
    def day(self) -> Weekday:
        
        return self._weekday

    @day.setter
    def day(self, value: Weekday) -> None:
        
        self._weekday = value
        self.update()
        
################################################################################        
    @property
    def open_time(self) -> time:
        
        return self._open
    
    @open_time.setter
    def open_time(self, value: time) -> None:
        
        self._open = value
        self.update()
        
################################################################################
    @property
    def close_time(self) -> time:
        
        return self._close
    
    @close_time.setter
    def close_time(self, value: time) -> None:
        
        self._close = value
        self.update()
        
################################################################################
    def update(self) -> None:
        
        self.bot.database.update.venue_hours(self)
        
################################################################################
    @property
    def start_timestamp(self) -> str:

        return U.format_dt(U.time_to_datetime(self._open), "t")

################################################################################
    @property
    def end_timestamp(self) -> str:

        return U.format_dt(U.time_to_datetime(self._close), "t")

################################################################################
    def delete(self) -> None:

        self._parent.bot.database.delete.venue_availability(self)

################################################################################
        