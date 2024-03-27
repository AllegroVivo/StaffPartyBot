from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Any

if TYPE_CHECKING:
    pass
################################################################################

__all__ = ("XIVTime",)

################################################################################
class XIVTime:
    
    __slots__ = (
        "hour",
        "minute",
        "timezone",
        "next_day"
    )

################################################################################
    def __init__(self, **kwargs):
        
        self.hour: int = kwargs.pop("hour")
        self.minute: int = kwargs.pop("minute")
        self.timezone: str = kwargs.pop("timezone")
        self.next_day: bool = kwargs.pop("next_day")
        
################################################################################
    @classmethod
    def from_data(cls, data: Dict[str, Any]) -> XIVTime:
        
        return cls(
            hour=data.get("hour"),
            minute=data.get("minute"),
            timezone=data.get("timeZone"),
            next_day=data.get("nextDay")
        )
    
################################################################################
