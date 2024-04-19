from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import time
from typing import TYPE_CHECKING, List, Type, TypeVar, Any, Tuple, Union

from Utilities import Utilities as U, Weekday

if TYPE_CHECKING:
    from Classes import Profile, ServiceProfile, TUser
################################################################################

__all_ = ("Availability",)

A = TypeVar("A", bound="Availability")

################################################################################
class Availability(ABC):

    __slots__ = (
        "_parent",
        "_day",
        "_start",
        "_end",
    )

################################################################################
    def __init__(
        self, 
        parent: Union[Profile, ServiceProfile, TUser], 
        day: Weekday, 
        start: time, 
        end: time
    ) -> None:

        self._parent: Union[Profile, ServiceProfile, TUser] = parent

        self._day: Weekday = day
        self._start: time = start
        self._end: time = end

################################################################################
    @classmethod
    @abstractmethod
    def new(
        cls: Type[A],
        parent: Union[Profile, ServiceProfile, TUser],
        day: Weekday,
        start: time,
        end: time
    ) -> A:

        raise NotImplementedError

################################################################################
    @classmethod
    def load(cls: Type[A], parent: Union[Profile, ServiceProfile, TUser], data: Tuple[Any, ...]) -> A:

        return cls(
            parent,
            Weekday(data[1]),
            data[2],
            data[3]
        )

################################################################################
    @property
    def parent(self) -> Union[Profile, ServiceProfile, TUser]:

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
    def long_availability_status(availability: List[Availability]) -> str:

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
    def short_availability_status(availability: List[Availability]) -> str:

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
    @abstractmethod
    def delete(self) -> None:

        raise NotImplementedError

################################################################################
    def contains(self, range_start: time, range_end: time) -> bool:

        return self._start <= range_start and self._end >= range_end

################################################################################
    