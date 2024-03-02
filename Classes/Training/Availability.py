from __future__ import annotations

from datetime import time
from typing import TYPE_CHECKING, List, Type, TypeVar, Any, Tuple

from Utilities import Utilities as U, Weekday

if TYPE_CHECKING:
    from Classes import TUser
################################################################################

__all_ = ("Availability",)

A = TypeVar("A", bound="Availability")

################################################################################
class Availability:
    """A class to represent a user's availability for training.
    
    Attributes:
    -----------
    _parent: :class:`TUser`
        The user this availability belongs to.
    _day: :class:`Weekday`
        The day of the week this availability is for.
    _start: :class:`time`
        The time this availability starts.
    _end: :class:`time`
        The time this availability ends.
    """

    __slots__ = (
        "_parent",
        "_day",
        "_start",
        "_end",
    )

################################################################################
    def __init__(self, parent: TUser, day: Weekday, start: time, end: time) -> None:

        self._parent: TUser = parent

        self._day: Weekday = day
        self._start: time = start
        self._end: time = end

################################################################################
    @classmethod
    def new(cls, parent: TUser, day: Weekday, start: time, end: time) -> A:

        parent.bot.database.insert.availability(parent.user_id, parent.guild_id, day, start, end)
        return cls(parent, day, start, end)

################################################################################
    @classmethod
    def load(cls: Type[A], parent: TUser, data: Tuple[Any, ...]) -> A:

        return cls(
            parent,
            Weekday(data[2]),
            data[3],
            data[4]
        )

################################################################################
    @property
    def parent(self) -> TUser:

        return self._parent

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
    def availability_status(availability: List[Availability]) -> str:

        if not availability:
            return "`No Availability Set`"

        ret = ""

        for i in [w for w in Weekday if w.value != 0]:
            if i.value not in [a.day.value for a in availability]:
                ret += f"{i.proper_name}: `Not Available`\n"
            else:
                a = [a for a in availability if a.day == i][0]
                ret += (
                    f"{a.day.proper_name}: "
                    f"{a.start_timestamp} - {a.end_timestamp}\n"
                )

        return ret

################################################################################
    def delete(self) -> None:

        self._parent.bot.database.delete.availability(self)

################################################################################
        