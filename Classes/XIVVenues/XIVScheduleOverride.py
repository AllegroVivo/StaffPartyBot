from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional, Type, TypeVar, Any, Dict

from .XIVTimeResolution import XIVTimeResolution
from .XIVTime import XIVTime
from .XIVUTCTime import XIVUTCTime

if TYPE_CHECKING:
    pass
################################################################################

__all__ = ("XIVScheduleOverride",)

SO = TypeVar("SO", bound="XIVScheduleOverride")

################################################################################
class XIVScheduleOverride:
    
    __slots__ = (
        "open",
        "start",
        "end",
        "now",
    )
    
################################################################################
    def __init__(self, **kwargs):
        
        self.open: bool = kwargs.pop("open")
        self.start: datetime = kwargs.pop("start")
        self.end: datetime = kwargs.pop("end")
        self.now: bool = kwargs.pop("now")
        
################################################################################
    @classmethod
    def from_data(cls: Type[SO], data: Dict[str, Any]) -> SO:
        
        return cls(
            open=data.get("open"),
            start=datetime.fromisoformat(data.get("start")),
            end=datetime.fromisoformat(data.get("end")),
            now=data.get("isNow")
        )
    
################################################################################
