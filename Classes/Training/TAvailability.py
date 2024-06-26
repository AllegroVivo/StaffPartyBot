from __future__ import annotations

from datetime import time, datetime, timedelta
from typing import TYPE_CHECKING, List, Type, TypeVar, Any, Tuple, Dict

from Classes.Common import Availability
from Utilities import Utilities as U, Weekday

if TYPE_CHECKING:
    from Classes import TUser
################################################################################

__all_ = ("TAvailability",)

TA = TypeVar("TA", bound="TAvailability")

################################################################################
class TAvailability(Availability):
    
    @classmethod
    def new(cls: Type[TA], parent: TUser, day: Weekday, start: time, end: time) -> TA:

        parent.bot.database.insert.availability(parent.user_id, parent.guild_id, day, start, end)
        return cls(parent, day, start, end)

################################################################################
    @classmethod
    def load(cls: Type[TA], parent: TUser, data: Tuple[Any, ...]) -> TA:

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
    @staticmethod
    def availability_status(availability: List[TAvailability]) -> str:

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
    def delete(self) -> None:

        self._parent.bot.database.delete.availability(self)

################################################################################
    @staticmethod
    def combine_availability(user1: TUser, user2: TUser) -> Dict[Weekday, List[Tuple[time, time]]]:

        def time_difference(start: time, end: time) -> timedelta:
            """Calculate the difference between two time objects, considering the end time might be midnight."""
            # If end time is midnight, treat it as 24 hours (end of the day)
            if end == time(0, 0):  # time(0, 0) represents midnight
                end = time(23, 59)  # Adjust to one minute before midnight for calculation
                return datetime.combine(datetime.today(), end) - datetime.combine(datetime.today(), start) + timedelta(minutes=1)
            else:
                return datetime.combine(datetime.today(), end) - datetime.combine(datetime.today(), start)

        common_availability = {}
        # Extract and map availabilities by day for easier comparison
        user1_avail_by_day = {a.day: (a.start_time, a.end_time) for a in user1.availability}
        user2_avail_by_day = {a.day: (a.start_time, a.end_time) for a in user2.availability}
    
        # Iterate through the availability of the first user
        for day, time_range_user1 in user1_avail_by_day.items():
            # Check if the second user has availability on the same day
            if day in user2_avail_by_day:
                time_range_user2 = user2_avail_by_day[day]
                # Calculate the overlap between the two users' time ranges
                start_max = max(time_range_user1[0], time_range_user2[0])
                end_min = min(time_range_user1[1], time_range_user2[1])
    
                # Check if there's at least an hour overlap
                if time_difference(start_max, end_min) >= timedelta(hours=1):
                    if day not in common_availability:
                        common_availability[day] = []
                    common_availability[day].append((start_max, end_min))
    
        return common_availability

################################################################################
    