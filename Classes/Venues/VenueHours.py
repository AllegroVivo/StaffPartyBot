from __future__ import annotations

import pytz
from datetime import time
from typing import TYPE_CHECKING, TypeVar, Any, Tuple, Type

from Utilities import Utilities as U, Weekday

if TYPE_CHECKING:
    from Classes import Venue, XIVScheduleComponent
################################################################################

__all__ = ("VenueHours",)

VH = TypeVar("VH", bound="VenueHours")

################################################################################
class VenueHours:

    __slots__ = (
        "_parent",
        "_day",
        "_open",
        "_close",
    )

################################################################################
    def __init__(self, parent: Venue, **kwargs) -> None:
        
        self._parent: Venue = parent
        
        self._day: Weekday = kwargs.pop("day")
        self._open: time = kwargs.pop("open")
        self._close: time = kwargs.pop("close")
    
################################################################################
    @classmethod
    def new(cls: Type[VH], parent: Venue, day: Weekday, open_time: time, close_time: time) -> VH:
        
        parent.bot.database.insert.venue_hours(parent, day, open_time, close_time)
        return cls(parent, day=day, open=open_time, close=close_time)
    
################################################################################
    @classmethod
    def load(cls: Type[VH], parent: Venue, data: Tuple[Any, ...]) -> VH:
        
        return cls(
            parent,
            day=Weekday(data[2]),
            open=data[3],
            close=data[4]
        )
    
################################################################################
    @classmethod
    def from_xiv_schedule(cls: Type[VH], parent: Venue, xiv: XIVScheduleComponent) -> VH:
   
        day = Weekday(xiv.day)
        open_time = time(hour=xiv.utc.start.hour, minute=xiv.utc.start.minute, tzinfo=pytz.utc)
        close_time = time(hour=xiv.utc.end.hour, minute=xiv.utc.end.minute, tzinfo=pytz.utc)
        
        return VenueHours.new(parent, day, open_time, close_time)
    
################################################################################
    @property
    def venue_id(self) -> str:
        
        return self._parent.id
    
################################################################################
    @property
    def day(self) -> Weekday:
        
        return self._day
    
################################################################################    
    @property
    def open_time(self) -> time:
        
        return self._open
    
################################################################################    
    @property
    def close_time(self) -> time:
        
        return self._close
    
################################################################################
    @property
    def open_ts(self) -> str: 
        
        return U.format_dt(U.time_to_datetime(self.open_time), "t")
    
################################################################################
    @property
    def close_ts(self) -> str:
        
        return U.format_dt(U.time_to_datetime(self.close_time), "t")
    
################################################################################
    def update(self) -> None:
        
        self._parent.bot.database.update.venue_hours(self)
        
################################################################################
    def delete(self) -> None:
        
        self._parent.bot.database.delete.venue_hours(self)

################################################################################
    def format(self) -> str:
        
        return f"{self.day.proper_name}: {self.open_ts} - {self.close_ts}"

################################################################################
