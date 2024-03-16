from __future__ import annotations

from typing import TYPE_CHECKING, Type, TypeVar, Any, Tuple, List

from discord import Interaction

from UI.Training import WeekdaySelectView, TimeSelectView
from Utilities import Utilities as U, Weekday
from .VenueAvailability import VenueAvailability

if TYPE_CHECKING:
    from Classes import VenueDetails
################################################################################

__all__ = ("VenueHours",)

VH = TypeVar("VH", bound="VenueHours")

################################################################################
class VenueHours:

    __slots__ = (
        "_parent",
        "_availability",
    )

################################################################################
    def __init__(self, parent: VenueDetails, availability: List[VenueAvailability] = None) -> None:
        
        self._parent: VenueDetails = parent
        self._availability: List[VenueAvailability] = availability or []
        
################################################################################
    @classmethod
    def load(cls: Type[VH], parent: VenueDetails, data: List[Tuple[Any, ...]]) -> VH:
        
        self = cls.__new__(cls)
        
        self._parent = parent
        self._availability = [VenueAvailability.load(self, i) for i in data]
        
        return self
        
################################################################################
    def format(self) -> str:

        if not self._availability:
            return "`Not Set`"

        ret = ""

        for i in [w for w in Weekday if w.value != 0]:
            if i.value not in [a.day.value for a in self._availability]:
                ret += f"{i.proper_name}: `Not Open`\n"
            else:
                a = [a for a in self._availability if a.day == i][0]
                ret += (
                    f"{a.day.proper_name}: "
                    f"{a.start_timestamp} - {a.end_timestamp}\n"
                )

        return ret

################################################################################
    async def set_availability(self, interaction: Interaction) -> None:

        status = U.make_embed(
            title="Set Availability",
            description=(
                "Please select the appropriate day from the initial\n"
                "selector, followed by your available time frame.\n\n"

                "Please note, you can set your timezone\n"
                "by using the `/training config` command.\n"
                f"{U.draw_line(extra=25)}"
            )
        )
        view = WeekdaySelectView(interaction.user)

        await interaction.respond(embed=status, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        weekday = view.value

        prompt = U.make_embed(
            title="Set Availability Start",
            description=(
                f"Please select the beginning of your availability for `{weekday.proper_name}`..."
            )
        )
        view = TimeSelectView(interaction.user)

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        start_time = view.value if view.value != -1 else None
        end_time = None

        if start_time is not None:
            prompt = U.make_embed(
                title="Set Availability End",
                description=(
                    f"Please select the end of your availability for `{weekday.proper_name}`..."
                )
            )
            view = TimeSelectView(interaction.user)

            await interaction.respond(embed=prompt, view=view)
            await view.wait()

            if not view.complete or view.value is False:
                return

            end_time = view.value

        for i, a in enumerate(self._availability):
            if a.day == weekday:
                self._availability.pop(i).delete()

        if start_time is not None:
            availability = VenueAvailability.new(self._parent, weekday, start_time, end_time)
            self._availability.append(availability)

################################################################################
