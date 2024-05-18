from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional, List, Type, TypeVar, Any, Dict

from discord import User

from .XIVLocation import XIVLocation
from .XIVScheduleComponent import XIVScheduleComponent
from .XIVScheduleOverride import XIVScheduleOverride
from .XIVTimeResolution import XIVTimeResolution

if TYPE_CHECKING:
    from Classes import StaffPartyBot
################################################################################

__all__ = ("XIVVenue",)

V = TypeVar("V", bound="XIVVenue")

################################################################################
class XIVVenue:
    
    __slots__ = (
        "id",
        "name",
        "banner",
        "added",
        "description",
        "location",
        "website",
        "discord",
        "hiring",
        "sfw",
        "schedule",
        "schedule_overrides",
        "managers",
        "tags",
        "approved",
        "modified",
        "mare_id",
        "mare_pass",
        "resolution",
    )
    
################################################################################
    def __init__(self, **kwargs):
        
        self.id: str = kwargs.pop("id")
        self.name: str = kwargs.pop("name")
        self.banner: Optional[str] = kwargs.pop("banner")
        self.added: datetime = kwargs.pop("added")
        self.description: List[str] = kwargs.pop("description")
        self.location: XIVLocation = kwargs.pop("location")
        self.website: Optional[str] = kwargs.pop("website")
        self.discord: Optional[str] = kwargs.pop("discord")
        self.hiring: bool = kwargs.pop("hiring")
        self.sfw: bool = kwargs.pop("sfw")
        self.schedule: List[XIVScheduleComponent] = kwargs.pop("schedule")
        self.schedule_overrides: List[XIVScheduleOverride] = kwargs.pop("schedule_overrides")
        self.managers: List[int] = kwargs.pop("managers")
        self.tags: List[str] = kwargs.pop("tags")
        self.approved: bool = kwargs.pop("approved")
        self.modified: Optional[datetime] = kwargs.pop("modified")
        self.mare_id: Optional[str] = kwargs.pop("mare_id")
        self.mare_pass: Optional[str] = kwargs.pop("mare_pass")
        self.resolution: XIVTimeResolution = kwargs.pop("resolution")
        
################################################################################
    @classmethod
    def from_data(cls: Type[V], data: Dict[str, Any]) -> V:

        return cls(
            id=data["id"],
            name=data["name"],
            banner=data.get("bannerUri"),
            added=datetime.fromisoformat(data["added"]),
            description=data.get("description", []),
            location=XIVLocation.from_data(data["location"]),
            website=data.get("website"),
            discord=data.get("discord"),
            hiring=data.get("hiring", False),
            sfw=data.get("sfw", False),
            schedule=[XIVScheduleComponent.from_data(x) for x in data.get("schedule", [])],
            schedule_overrides=[
                XIVScheduleOverride.from_data(x) for x in data.get("scheduleOverrides", [])
            ],
            managers=[int(m) for m in data["managers"]],
            tags=[t for t in data.get("tags", []) if t is not None],
            approved=data.get("approved", False),
            modified=(
                datetime.fromisoformat(data["lastModified"]) if "lastModified" in data
                and data["lastModified"] is not None
                else None
            ),
            mare_id=data.get("mareCode"),
            mare_pass=data.get("marePassword"),
            resolution=(
                XIVTimeResolution.from_data(data["resolution"])
                if "resolution" in data and data["resolution"]
                else None
            )
        )

################################################################################
    def to_itinerary_string(self) -> str:
        
        return (
            f"{self.name}::{self.location.to_itinerary_string()}"
        )

################################################################################
