from __future__ import annotations

from datetime import time
from typing import TYPE_CHECKING, List, TypeVar

from Classes.Common import Availability
from Utilities import Weekday

if TYPE_CHECKING:
    from Classes import Profile
################################################################################

__all_ = ("Availability",)

PA = TypeVar("PA", bound="PAvailability")

################################################################################
class PAvailability(Availability):

    @classmethod
    def new(cls, parent: Profile, day: Weekday, start: time, end: time) -> PA:

        parent.bot.database.insert.profile_availability(parent.id, day, start, end)
        return cls(parent, day, start, end)

################################################################################
    @staticmethod
    def long_availability_status(availability: List[PAvailability]) -> str:

        if not availability:
            return "`No Availability Set`"

        ret = ""

        for i in [w for w in Weekday]:
            if i.value not in [a.day.value for a in availability]:
                ret += f"{i.proper_name}: `Not Available`\n"
            else:
                a = [a for a in availability if a.day == i][0]
                ret += (
                    f"{a.day.proper_name}: "
                    f"{a.start_timestamp} - {a.end_timestamp}\n"
                )

        return "*(Times are displayed in\nyour local time zone.)*\n\n" + ret

################################################################################
    @staticmethod
    def short_availability_status(availability: List[PAvailability]) -> str:

        if not availability:
            return "`No Availability Set`"

        ret = ""
        for a in availability:
            ret += (
                f"{a.day.proper_name}: "
                f"{a.start_timestamp} - {a.end_timestamp}\n"
            )

        return ret

################################################################################
    def delete(self) -> None:

        self._parent.bot.database.delete.profile_availability(self)

################################################################################
    