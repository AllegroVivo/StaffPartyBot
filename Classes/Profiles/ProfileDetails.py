from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional, Type, TypeVar, Any, Tuple, Dict

import pytz
from discord import (
    Colour, 
    Embed, 
    Interaction, 
    EmbedField, 
    Message,
    SelectOption, 
    Thread,
    NotFound,
)

from Assets import BotEmojis
from UI.Training import TimeSelectView, WeekdayTZSelectView
from UI.Profiles import (
    ProfileDetailsStatusView,
    ProfileNameModal,
    ProfileURLModal,
    ProfileColorModal,
    ProfileJobsModal,
    ProfileRatesModal
)
from UI.Venues import PositionSelectView
from Utilities import Utilities as U, NS, MalformedURLError
from .PAvailability import PAvailability
from .ProfileSection import ProfileSection

if TYPE_CHECKING:
    from Classes import Profile, Position
################################################################################

__all__ = ("ProfileDetails",)

PD = TypeVar("PD", bound="ProfileDetails")

################################################################################
class ProfileDetails(ProfileSection):
    
    __slots__ = (
        "_name",
        "_url",
        "_color",
        "_jobs",
        "_rates",
        "_post_msg",
        "_positions",
        "_availability",
        "_dm_pref",
    )

################################################################################
    def __init__(self, parent: Profile, **kwargs) -> None:
        
        super().__init__(parent)

        self._name: Optional[str] = kwargs.pop("name", None)
        self._url: Optional[str] = kwargs.pop("url", None) or kwargs.pop("custom_url", None)
        self._color: Optional[Colour] = kwargs.pop("color", None) or kwargs.pop("colour", None)
        self._jobs: List[str] = kwargs.pop("jobs", None) or []
        self._rates: Optional[str] = kwargs.pop("rates", None)
        self._post_msg: Optional[Message] = kwargs.pop("post_msg", None)
        self._positions: List[Position] = kwargs.pop("positions", None) or []
        self._availability: List[PAvailability] = kwargs.pop("availability", None) or []
        self._dm_pref: bool = kwargs.pop("dm_preference", False)

################################################################################
    @classmethod
    async def load(
        cls: Type[PD], 
        parent: Profile,
        data: Tuple[Any, ...], 
        hours: Tuple[Tuple[Any, ...]]
    ) -> PD:

        post_msg = None
        try:
            url_parts = data[5].split("/") if data[5] else []
            if len(url_parts) >= 2:
                if thread := await parent.bot.get_or_fetch_channel(int(url_parts[-2])):
                    post_msg = await thread.fetch_message(int(url_parts[-1]))
        except NotFound:
            pass
        
        return cls(
            parent=parent,
            name=data[0],
            url=data[1],
            color=Colour(data[2]) if data[2] is not None else None,
            jobs=data[3] or [],
            rates=data[4],
            post_msg=post_msg,
            positions=[
                parent.manager.guild.position_manager.get_position(p) 
                for p in data[6]
            ] if data[6] else [],
            availability=[PAvailability.load(parent, h) for h in hours],
            dm_preference=data[7]
        )
    
################################################################################
    @property
    def name(self) -> str:
        
        return self._name or str(NS)
    
    @name.setter
    def name(self, value: Optional[str]) -> None:
        
        self._name = value
        self.update()
        
################################################################################    
    @property
    def url(self) -> Optional[str]:
        
        return self._url
    
    @url.setter
    def url(self, value: Optional[str]) -> None:
        
        self._url = value
        self.update()
        
################################################################################    
    @property
    def color(self) -> Optional[Colour]:
        
        return self._color
    
    @color.setter
    def color(self, value: Optional[Colour]) -> None:
        
        self._color = value
        self.update()
        
################################################################################    
    @property
    def jobs(self) -> List[str]:
        
        return self._jobs
    
    @jobs.setter
    def jobs(self, value: List[str]) -> None:
        
        self._jobs = value
        self.update()
        
################################################################################    
    @property
    def rates(self) -> Optional[str]:
        
        return self._rates

    @rates.setter
    def rates(self, value: Optional[str]) -> None:
        
        self._rates = value
        self.update()
        
################################################################################    
    @property
    def post_message(self) -> Optional[Message]:
        
        return self._post_msg
    
    @post_message.setter
    def post_message(self, value: Optional[Message]) -> None:
        
        self._post_msg = value
        self.update()
        
################################################################################
    @property
    def positions(self) -> List[Position]:
        
        return self._positions
    
    @positions.setter
    def positions(self, value: List[Position]) -> None:
        
        self._positions = value
        self.update()
        
################################################################################
    @property
    def availability(self) -> List[PAvailability]:
        
        self._availability.sort(key=lambda x: x.day.value)
        return self._availability
    
################################################################################
    @property
    def dm_preference(self) -> bool:
        
        return self._dm_pref
    
    @dm_preference.setter
    def dm_preference(self, value: bool) -> None:
        
        self._dm_pref = value
        self.update()
        
################################################################################
    def update(self) -> None:
        
        self.parent.bot.database.update.profile_details(self)
        
################################################################################
    async def menu(self, interaction: Interaction) -> None:
        
        embed = self.status()
        view = ProfileDetailsStatusView(interaction.user, self)
        
        await interaction.respond(embed=embed, view=view)
        await view.wait()
    
################################################################################
    def status(self) -> Embed:

        url_field = str(self.url) if self.url is not None else str(NS)
        jobs = "- " + "\n- ".join(self._jobs) if self._jobs else str(NS)
        rates = str(self.rates) if self.rates is not None else str(NS)

        if self._color is not None:
            color_field = f"{BotEmojis.ArrowLeft} -- (__{str(self.color).upper()}__)"
        else:
            color_field = str(NS)

        positions = str(NS)
        if self.positions:
            # Group the positions in chunks of 4, then join each chunk 
            # with a comma and each group with "\n"
            positions = "\n".join(
                ", ".join(f"`{p.name}`" for p in self.positions[i:i+3])
                for i in range(0, len(self.positions), 3)
            )

        fields = [
            EmbedField("__Color__", color_field, True),
            EmbedField("__Jobs__", jobs, True),
            EmbedField("__Custom URL__", url_field, False),
            EmbedField("__Employable Positions__", positions, True),
            EmbedField(
                name="__DM Preference__", 
                value=(
                    (str(BotEmojis.Check) if self._dm_pref else str(BotEmojis.Cross)) +
                    "\n*(This indicates whether\n"
                    "venue owners are encouraged\n"
                    "to DM you about work.)*"
                ), 
                inline=True
            ),
            EmbedField(
                name="__Availability__", 
                value=PAvailability.short_availability_status(self._availability), 
                inline=False
            ),
            EmbedField("__Freelance Rates__", rates, False)
        ]

        name = f"`{str(self.name)}`" if self.name is not None else str(NS)
        char_name = f"**Character Name:** {name}"

        return U.make_embed(
            title="Profile Details",
            color=self.color,
            description=(
                f"{U.draw_line(text=char_name)}\n"
                f"{char_name}\n"
                f"{U.draw_line(text=char_name)}\n"
                "Select a button to add/edit the corresponding profile attribute."
            ),
            fields=fields
        )
        
################################################################################
    async def set_name(self, interaction: Interaction) -> None:
        
        modal = ProfileNameModal(self._name)
        
        await interaction.response.send_modal(modal)
        await modal.wait()
        
        if not modal.complete:
            return
        
        self.name = modal.value
    
################################################################################
    async def set_url(self, interaction: Interaction) -> None:
        
        modal = ProfileURLModal(self.url)
        
        await interaction.response.send_modal(modal)
        await modal.wait()
        
        if not modal.complete:
            return
        
        if not modal.value.startswith("https://"):
            error = MalformedURLError(modal.value)
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        self.url = modal.value
    
################################################################################
    async def set_color(self, interaction: Interaction) -> None:
        
        modal = ProfileColorModal(self.color)
        
        await interaction.response.send_modal(modal)
        await modal.wait()
        
        if not modal.complete:
            return
        
        self.color = Colour(modal.value)
    
################################################################################
    async def set_jobs(self, interaction: Interaction) -> None:

        modal = ProfileJobsModal(self.jobs)

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.jobs = modal.value
    
################################################################################
    async def set_rates(self, interaction: Interaction) -> None:

        modal = ProfileRatesModal(self.rates)

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.rates = modal.value

################################################################################
    def progress(self) -> str:

        em_color = self.progress_emoji(self._color)
        em_name = self.progress_emoji(self._name)
        em_url = self.progress_emoji(self._url)
        em_jobs = self.progress_emoji(self._jobs)
        em_hours = self.progress_emoji(self._availability)
        em_rates = self.progress_emoji(self._rates)

        return (
            f"{U.draw_line(extra=15)}\n"
            "__**Details**__\n"
            f"{em_name} -- Character Name\n"
            f"{em_url} -- Custom URL\n"
            f"{em_color} -- Accent Color\n"
            f"{em_jobs} -- Jobs List\n"
            f"{em_hours} -- Availability\n"
            f"{em_rates} -- Rates Field\n"
        )

################################################################################
    def compile(
            self
    ) -> Tuple[
        str,
        Optional[str],
        Optional[Colour],
        Optional[str],
        Optional[EmbedField],
        Embed,
        bool
    ]:

        return (
            self.name,
            self.url,
            self.color,
            "/".join(self._jobs) if self._jobs else None,
            self.rates_field(),
            self._compile_availability(),
            self._dm_pref,
        )
    
################################################################################
    def rates_field(self) -> Optional[EmbedField]:

        if self.rates is None:
            return

        return EmbedField(
            name=f"{BotEmojis.FlyingMoney} __Freelance Rates__ {BotEmojis.FlyingMoney}",
            value=(
                f"{self.rates}\n"
                f"{U.draw_line(extra=15)}"
            ),
            inline=False
        )

################################################################################
    def _dms_field(self) -> EmbedField:
        
        return EmbedField(
            name="__DM Preference__",
            value=(
                f"{BotEmojis.Check if self._dm_pref else BotEmojis.Cross}"
            ),
            inline=True
        )
    
################################################################################
    async def set_positions(self, interaction: Interaction) -> None:
        
        base_options = self._parent.manager.guild.position_manager.select_options()
        options = [
            SelectOption(
                label=option.label,
                value=option.value,
                default=option.value in [p.id for p in self.positions]
            ) for option in base_options
        ]
        
        prompt = U.make_embed(
            title="Set Positions",
            description="Please select the positions you are qualified to work."
        )
        view = PositionSelectView(interaction.user, options)
        
        await interaction.respond(embed=prompt, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            return
        
        self.positions = [
            self._parent.manager.guild.position_manager.get_position(p)
            for p in view.value
        ]
    
################################################################################
    def _to_dict(self) -> Dict[str, Any]:
        
        return {
            "name": self._name,
            "url": self._url,
            "color": self._color.value if self._color is not None else None,
            "jobs": self._jobs,
            "rates": self._rates,
        }
    
################################################################################
    async def set_availability(self, interaction: Interaction) -> None:

        footer = "Current Time EST: " + datetime.now(pytz.timezone("US/Eastern")).strftime("%I:%M %p")
        status = U.make_embed(
            title="Set Availability",
            description=(
                "Please select the appropriate day from the initial selector, "
                "followed by your timezone, and finally available time frame.\n\n"

                "(__**PLEASE NOTE: ALL TIME INPUTS ARE IN EASTERN STANDARD TIME**__.)\n"
                f"{U.draw_line(extra=46)}"
            ),
            footer_text=footer
        )
        view = WeekdayTZSelectView(interaction.user)

        await interaction.respond(embed=status, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        # weekday, tz = view.value
        weekday = view.value

        prompt = U.make_embed(
            title="Set Availability Start",
            description=(
                f"Please select the beginning of your availability "
                f"for `{weekday.proper_name}`...\n\n"

                "(__**PLEASE NOTE: ALL TIME INPUTS ARE IN EASTERN STANDARD TIME**__.)\n"
            ),
            footer_text=footer
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
                    f"Please select the end of your availability "
                    f"for `{weekday.proper_name}`...\n\n"

                    "(__**PLEASE NOTE: ALL TIME INPUTS ARE IN EASTERN STANDARD TIME**__.)\n"
                ),
                footer_text=footer
            )
            view = TimeSelectView(interaction.user)

            await interaction.respond(embed=prompt, view=view)
            await view.wait()

            if not view.complete or view.value is False:
                return

            end_time = view.value

        for i, a in enumerate(self.availability):
            if a.day == weekday:
                self._availability.pop(i).delete()

        if start_time is not None:
            availability = PAvailability.new(self.parent, weekday, start_time, end_time)
            self._availability.append(availability)
        
################################################################################
    def _compile_availability(self) -> Embed:
        
        position_str = ", ".join([f"`{p.name}`" for p in self.positions])
        return U.make_embed(
            color=self.color,
            title="__Availability__",
            description=(
                f"{PAvailability.long_availability_status(self.availability)}\n"
                
                "**__Employable Positions__**\n"
                f"{position_str}"
            ),
            footer_text=self._url
        )
    
################################################################################
    def toggle_dm_preference(self) -> None:
        
        self.dm_preference = not self.dm_preference
        
################################################################################
