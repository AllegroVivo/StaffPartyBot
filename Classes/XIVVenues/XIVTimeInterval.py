from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Any

if TYPE_CHECKING:
    pass
################################################################################

__all__ = ("XIVTimeInterval",)

################################################################################
class XIVTimeInterval:
    
    __slots__ = (
        "type",
        "arg",
    )

################################################################################
    def __init__(self, **kwargs):
        
        self.type: int = kwargs.get("type", 0)
        self.arg: int = kwargs.get("arg", 0)
        
################################################################################
    @classmethod
    def from_data(cls, data: Dict[str, Any]) -> XIVTimeInterval:
        
        return cls(
            type=data.get("intervalType"),
            arg=data.get("intervalArgument")
        )
    
################################################################################
