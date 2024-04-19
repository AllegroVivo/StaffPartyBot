from __future__ import annotations

from datetime import time
from typing import TYPE_CHECKING, Type, TypeVar

from Classes.Common import Availability
from Utilities import Weekday

if TYPE_CHECKING:
    from Classes import ServiceProfile
################################################################################

__all__ = ("SAvailability",)

SA = TypeVar("SA", bound="SAvailability")

################################################################################
class SAvailability(Availability):

    @classmethod
    def new(cls: Type[SA], parent: ServiceProfile, day: Weekday, start: time, end: time) -> SA:

        parent.bot.database.insert.sp_availability(parent.id, day, start, end)
        return cls(parent=parent, day=day, start=start, end=end)

################################################################################
    def delete(self) -> None:

        self._parent.bot.database.delete.sp_availability(self)

################################################################################
    