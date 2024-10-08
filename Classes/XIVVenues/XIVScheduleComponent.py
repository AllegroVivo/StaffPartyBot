from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Type, TypeVar, Any, Dict

from .XIVTimeResolution import XIVTimeResolution
from .XIVTime import XIVTime
from .XIVUTCTime import XIVUTCTime
from .XIVTimeInterval import XIVTimeInterval

if TYPE_CHECKING:
    pass
################################################################################

__all__ = ("XIVScheduleComponent",)

SC = TypeVar("SC", bound="XIVScheduleComponent")

################################################################################
class XIVScheduleComponent:
    
    __slots__ = (
        "commencing",
        "day",
        "start",
        "end",
        "interval",
        "location",
        "resolution",
        "utc",
    )
    
################################################################################
    def __init__(self, **kwargs):
        
        self.commencing: Optional[Any] = kwargs.pop("commencing")
        self.day: str = kwargs.pop("day")
        self.start: XIVTime = kwargs.pop("start")
        self.end: XIVTime = kwargs.pop("end")
        self.interval: XIVTimeInterval = kwargs.pop("interval")
        self.location: Optional[str] = kwargs.pop("location")
        self.resolution: XIVTimeResolution = kwargs.pop("resolution")
        self.utc: XIVUTCTime = kwargs.pop("utc")
        
################################################################################
    @classmethod
    def from_data(cls: Type[SC], data: Dict[str, Any]) -> SC:
        
        return cls(
            commencing=data.get("commencing"),
            day=data.get("day"),
            start=XIVTime.from_data(data.get("start")),
            end=XIVTime.from_data(data.get("end")) if data.get("end") else None,
            interval=XIVTimeInterval.from_data(data.get("interval")),
            location=data.get("location"),
            resolution=XIVTimeResolution.from_data(data.get("resolution")),
            utc=XIVUTCTime.from_data(data.get("utc"))
        )
    
################################################################################
