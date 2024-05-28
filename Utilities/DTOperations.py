from __future__ import annotations

from discord import Interaction
from datetime import datetime, time
from typing import Optional, Tuple
from .Enums import Timezone, Weekday
from .Utilities import Utilities
from UI.Guild import TZWeekdaySelectView, TimeSelectView
from .Errors import DateTimeFormatError, DateTimeMismatchError, DateTimeBeforeNowError, TimeRangeError
################################################################################

__all__ = ("DTOperations",)

################################################################################
class DTOperations:

    @staticmethod
    async def collect_single_datetime(
        interaction: Interaction,
        current_value: Optional[datetime] = None,
    ) -> Optional[Tuple[Timezone, Optional[datetime]]]:
    
        from UI.Guild import SingleDTModal
        from UI.Common import TimezoneSelectView
    
        prompt = Utilities.make_embed(
            title="Select your Timezone",
            description=(
                "You can select the timezone that will correspond to your datetime"
                "entry from the selector below."
            ),
        )
        view = TimezoneSelectView(interaction.user)
    
        await interaction.respond(embed=prompt, view=view)
        await view.wait()
    
        if not view.complete or view.value is False:
            return
    
        timezone, inter = view.value
        localized_dt = (
            Utilities.TIMEZONE_OFFSETS[timezone].localize(current_value)
            if current_value else None
        )
        modal = SingleDTModal(localized_dt, "Enter a Date and Time")
    
        await inter.response.send_modal(modal)
        await modal.wait()
    
        if not modal.complete:
            return
    
        try:
            return timezone, datetime.strptime(modal.value, "%m/%d/%y %I:%M %p")
        except ValueError:
            error = DateTimeFormatError(modal.value)
            await interaction.respond(embed=error, ephemeral=True)
            return
    
################################################################################
    @staticmethod
    async def collect_single_time(
        interaction: Interaction,
        current_value: Optional[time] = None,
    ) -> Optional[Tuple[Timezone, Optional[time]]]:
    
        from UI.Guild import SingleTimeModal
        from UI.Common import TimezoneSelectView
    
        prompt = Utilities.make_embed(
            title="Select your Timezone",
            description=(
                "You can select the timezone that will correspond to your upcoming time"
                "entry from the selector below."
            ),
        )
        view = TimezoneSelectView(interaction.user)
    
        await interaction.respond(embed=prompt, view=view)
        await view.wait()
    
        if not view.complete or view.value is False:
            return
    
        timezone, inter = view.value
        if current_value:
            localized_time = timezone.localize(datetime.combine(datetime.today(), current_value))
        else:
            localized_time = None
    
        modal = SingleTimeModal(localized_time, "Enter a Time")
    
        await inter.response.send_modal(modal)
        await modal.wait()
    
        if not modal.complete:
            return
    
        try:
            return_dt = datetime.strptime(modal.value, "%I:%M %p")
        except ValueError:
            error = DateTimeFormatError(modal.value)
            await interaction.respond(embed=error, ephemeral=True)
            return
        else:
            return timezone, return_dt.time()
    
################################################################################
    @staticmethod
    async def collect_double_datetime(
        interaction: Interaction,
        current_value_a: Optional[datetime] = None,
        current_value_b: Optional[datetime] = None,
        max_duration: Optional[int] = None,
    ) -> Optional[Tuple[Timezone, Optional[datetime], Optional[datetime]]]:
    
        from UI.Guild import DoubleDTModal
        from UI.Common import TimezoneSelectView
    
        prompt = Utilities.make_embed(
            title="Select your Timezone",
            description=(
                "You can select the timezone that will correspond to your datetime"
                "entry from the selector below."
            ),
        )
        view = TimezoneSelectView(interaction.user)
    
        await interaction.respond(embed=prompt, view=view)
        await view.wait()
    
        if not view.complete or view.value is False:
            return
    
        timezone, inter = view.value
        localized_dt_a = (
            Utilities.TIMEZONE_OFFSETS[timezone].localize(current_value_a)
            if current_value_a else None
        )
        localized_dt_b = (
            Utilities.TIMEZONE_OFFSETS[timezone].localize(current_value_b)
            if current_value_b else None
        )
        modal = DoubleDTModal(localized_dt_a, localized_dt_b)
    
        await inter.response.send_modal(modal)
        await modal.wait()
    
        if not modal.complete:
            return
    
        try:
            raw_start = datetime.strptime(modal.value[0], "%m/%d/%y %I:%M %p")
        except ValueError:
            error = DateTimeFormatError(modal.value[0])
            await interaction.respond(embed=error, ephemeral=True)
            return
        else:
            start_dt = Utilities.TIMEZONE_OFFSETS[timezone].localize(
                datetime(
                    raw_start.year,
                    raw_start.month,
                    raw_start.day,
                    raw_start.hour,
                    raw_start.minute
                )
            )
    
        try:
            raw_end = datetime.strptime(modal.value[1], "%m/%d/%y %I:%M %p")
        except ValueError:
            error = DateTimeFormatError(modal.value[1])
            await interaction.respond(embed=error, ephemeral=True)
            return
        else:
            end_dt = Utilities.TIMEZONE_OFFSETS[timezone].localize(
                datetime(
                    raw_end.year,
                    raw_end.month,
                    raw_end.day,
                    raw_end.hour,
                    raw_end.minute
                )
            )
    
        if end_dt <= start_dt:
            error = DateTimeMismatchError(start_dt, end_dt)
            await interaction.respond(embed=error, ephemeral=True)
            return
    
        if datetime.now().timestamp() > end_dt.timestamp():
            error = DateTimeBeforeNowError(start_dt)
            await interaction.respond(embed=error, ephemeral=True)
            return
    
        if (end_dt - start_dt).total_seconds() < 7200 or (end_dt - start_dt).total_seconds() > (max_duration * 86400):
            error = TimeRangeError("2 Hours", f"{max_duration} Days")
            await interaction.respond(embed=error, ephemeral=True)
            return
    
        return timezone, start_dt, end_dt
    
################################################################################
    @staticmethod
    async def collect_double_time(
        interaction: Interaction,
        current_value_a: Optional[time] = None,
        current_value_b: Optional[time] = None,
    ) -> Optional[Tuple[Timezone, Optional[time], Optional[time]]]:
    
        from UI.Guild import DoubleTimeModal
        from UI.Common import TimezoneSelectView
    
        prompt = Utilities.make_embed(
            title="Select your Timezone",
            description=(
                "You can select the timezone that will correspond to your time"
                "entries from the selector below."
            ),
        )
        view = TimezoneSelectView(interaction.user)
    
        await interaction.respond(embed=prompt, view=view)
        await view.wait()
    
        if not view.complete or view.value is False:
            return
    
        timezone, inter = view.value
        if current_value_a:
            localized_time_a = timezone.localize(datetime.combine(datetime.today(), current_value_a))
        else:
            localized_time_a = None
        if current_value_b:
            localized_time_b = timezone.localize(datetime.combine(datetime.today(), current_value_b))
        else:
            localized_time_b = None
    
        modal = DoubleTimeModal(localized_time_a, localized_time_b)
    
        await inter.response.send_modal(modal)
        await modal.wait()
    
        if not modal.complete:
            return
    
        try:
            raw_start = datetime.strptime(modal.value[0], "%I:%M %p")
        except ValueError:
            error = DateTimeFormatError(modal.value[0])
            await interaction.respond(embed=error, ephemeral=True)
            return
        else:
            start_dt = Utilities.TIMEZONE_OFFSETS[timezone].localize(
                datetime(
                    raw_start.year,
                    raw_start.month,
                    raw_start.day,
                    raw_start.hour,
                    raw_start.minute
                )
            )
    
        try:
            raw_end = datetime.strptime(modal.value[1], "%I:%M %p")
        except ValueError:
            error = DateTimeFormatError(modal.value[1])
            await interaction.respond(embed=error, ephemeral=True)
            return
        else:
            end_dt = Utilities.TIMEZONE_OFFSETS[timezone].localize(
                datetime(
                    raw_end.year,
                    raw_end.month,
                    raw_end.day,
                    raw_end.hour,
                    raw_end.minute
                )
            )
    
        return timezone, start_dt.time(), end_dt.time()
    
################################################################################
    @staticmethod
    async def collect_availability(
        interaction: Interaction
    ) -> Optional[Tuple[Timezone, Weekday, Optional[time], Optional[time]]]:

        status = Utilities.make_embed(
            title="Set Availability",
            description=(
                "Please select your timezone initial selector, followed by the "
                "day to set availability for, and finally the available time frame."
            )
        )
        view = TZWeekdaySelectView(interaction.user)

        await interaction.respond(embed=status, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        tz, weekday = view.value

        prompt = Utilities.make_embed(
            title="Set Availability Start",
            description=(
                f"Please select the beginning of your availability "
                f"for `{weekday.proper_name}`..."
            )
        )
        view = TimeSelectView(interaction.user)

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        start_time = view.value if view.value != -1 else None

        if start_time is None:
            return tz, weekday, None, None
            
        prompt = Utilities.make_embed(
            title="Set Availability End",
            description=(
                f"Please select the end of your availability "
                f"for `{weekday.proper_name}`..."
            )
        )
        view = TimeSelectView(interaction.user)

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        end_time = view.value
            
        today = datetime.now().date()
        py_tz = Utilities.TIMEZONE_OFFSETS[tz]
        utc_tz = Utilities.TIMEZONE_OFFSETS[Timezone.GMT]
        
        start_dt = utc_tz.normalize(
            py_tz.localize(
                datetime(
                    today.year,
                    today.month,
                    today.day,
                    start_time.hour,
                    start_time.minute
                )
            )
        )
        end_dt = utc_tz.normalize(
            py_tz.localize(
                datetime(
                    today.year,
                    today.month,
                    today.day,
                    end_time.hour,
                    end_time.minute
                )
            )
        )

        return tz, weekday, start_dt.time(), end_dt.time()
            
################################################################################
    