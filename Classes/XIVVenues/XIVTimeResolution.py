from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING, Dict, Any

if TYPE_CHECKING:
    pass
################################################################################

__all__ = ("XIVTimeResolution",)

################################################################################
class XIVTimeResolution:
    
    __slots__ = (
        "start",
        "end",
        "now",
        "in_week",
    )

################################################################################
    def __init__(self, **kwargs):
        
        self.start: datetime = kwargs.get("start")
        self.end: datetime = kwargs.get("end")
        self.now: bool = kwargs.get("now", False)
        self.in_week: bool = kwargs.get("in_week", False)
        
################################################################################
    @classmethod
    def from_data(cls, data: Dict[str, Any]) -> XIVTimeResolution:
        
        return cls(
            start=datetime.fromisoformat(data.get("start")),
            end=datetime.fromisoformat(data.get("end")),
            now=data.get("isNow"),
            in_week=data.get("isWithinWeek")
        )
    
################################################################################
