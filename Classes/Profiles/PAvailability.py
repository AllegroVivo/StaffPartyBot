from __future__ import annotations

from datetime import time, datetime, timedelta
from typing import TYPE_CHECKING, List, Type, TypeVar, Any, Tuple, Dict

from Utilities import Utilities as U, Weekday

if TYPE_CHECKING:
    from Classes import Profile
################################################################################

__all_ = ("Availability",)

PA = TypeVar("PA", bound="PAvailability")

################################################################################
class PAvailability:

    __slots__ = (
        "_parent",
        "_day",
        "_start",
        "_end",
    )

################################################################################
    def __init__(self, parent: Profile, day: Weekday, start: time, end: time) -> None:

        self._parent: Profile = parent

        self._day: Weekday = day
        self._start: time = start
        self._end: time = end

################################################################################
    @classmethod
    def new(cls, parent: Profile, day: Weekday, start: time, end: time) -> PA:

        parent.bot.database.insert.profile_availability(parent.id, day, start, end)
        return cls(parent, day, start, end)

################################################################################
    @classmethod
    def load(cls: Type[PA], parent: Profile, data: Tuple[Any, ...]) -> PA:

        return cls(
            parent,
            Weekday(data[1]),
            data[2],
            data[3]
        )

################################################################################
    @property
    def parent(self) -> Profile:

        return self._parent

################################################################################
    @property
    def user_id(self) -> int:
        
        return self._parent.user_id
    
################################################################################
    @property
    def day(self) -> Weekday:

        return self._day

################################################################################
    @property
    def start_time(self) -> time:

        return self._start

################################################################################
    @property
    def end_time(self) -> time:

        return self._end

################################################################################
    @property
    def start_timestamp(self) -> str:

        return U.format_dt(U.time_to_datetime(self._start), "t")

################################################################################
    @property
    def end_timestamp(self) -> str:

        return U.format_dt(U.time_to_datetime(self._end), "t")

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
    def contains(self, range_start: time, range_end: time) -> bool:

        return self._start <= range_start and self._end >= range_end

################################################################################
    