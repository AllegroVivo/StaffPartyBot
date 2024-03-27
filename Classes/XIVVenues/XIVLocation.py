from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Any, Type, TypeVar, Dict

if TYPE_CHECKING:
    pass
################################################################################

__all__ = ("XIVLocation",)

L = TypeVar("L", bound="XIVLocation")

################################################################################
class XIVLocation:
    
    __slots__ = (
        "data_center",
        "world",
        "district",
        "ward",
        "plot",
        "apartment",
        "room",
        "subdivision",
        "shard",
        "override"
    )

################################################################################
    def __init__(self, **kwargs):
        
        self.data_center: str = kwargs.pop("dc")
        self.world: str = kwargs.pop("world")
        self.district: str = kwargs.pop("district")
        self.ward: int = kwargs.pop("ward")
        self.plot: int = kwargs.pop("plot")
        self.apartment: int = kwargs.pop("apt")
        self.room: int = kwargs.pop("room")
        self.subdivision: bool = kwargs.pop("subdivision")
        self.shard: Optional[int] = kwargs.pop("shard")
        self.override: Optional[Any] = kwargs.pop("override")
        
################################################################################
    @classmethod
    def from_data(cls: Type[L], data: Dict[str, Any]) -> L:
        
        return cls(
            dc=data.get("dataCenter"),
            world=data.get("world"),
            district=data.get("district"),
            ward=data.get("ward"),
            plot=data.get("plot"),
            apt=data.get("apartment"),
            room=data.get("room"),
            subdivision=data.get("subdivision"),
            shard=data.get("shard"),
            override=data.get("override")
        )
    
################################################################################
