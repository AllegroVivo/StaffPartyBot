from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Any, Optional
from .XIVTime import XIVTime

if TYPE_CHECKING:
    pass
################################################################################

__all__ = ("XIVUTCTime",)

################################################################################
class XIVUTCTime:
    
    __slots__ = (
        "from_value",
        "day",
        "start",
        "end",
        "location",
    )

################################################################################
    def __init__(self, **kwargs):
        
        self.from_value: Optional[Any] = kwargs.pop("_from")
        self.day: int = kwargs.pop("day")
        self.start: XIVTime = kwargs.pop("start")
        self.end: XIVTime = kwargs.pop("end")
        self.location: Optional[Any] = kwargs.pop("location")
        
################################################################################
    @classmethod
    def from_data(cls, data: Dict[str, Any]) -> XIVUTCTime:
        
        return cls(
            _from=data.get("from"),
            day=data.get("day"),
            start=XIVTime.from_data(data.get("start")),
            end=XIVTime.from_data(data.get("end")) if data.get("end") else None,
            location=data.get("location")
        )
    
################################################################################
