from __future__ import annotations

from discord import Colour, Embed, Interaction, EmbedField, Message, SelectOption
from typing import TYPE_CHECKING, List, Optional, Type, TypeVar, Any, Tuple

from Assets import BotEmojis
from .ProfileSection import ProfileSection
from UI.Profiles import (
    ProfileDetailsStatusView,
    ProfileNameModal,
    ProfileURLModal,
    ProfileColorModal,
    ProfileJobsModal,
    ProfileRatesModal
)
from UI.Venues import PositionSelectView
from Utilities import Utilities as U, NS

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

################################################################################
    @classmethod
    async def load(cls: Type[PD], parent: Profile, data: Tuple[Any, ...]) -> PD:

        post_msg = None
        try:
            url_parts = data[5].split("/") if data[5] else []
            if len(url_parts) >= 2:
                channel = await parent.bot.fetch_channel(int(url_parts[-2]))
                if channel.threads:
                    named_threads = [
                        t for t in channel.threads 
                        if t.name.lower() == data[0].lower()
                    ] if data[0] else []
                    post_msg = named_threads[0].last_message if named_threads else None
        except:
            pass
        
        positions = [
            parent.manager.guild.position_manager.get_position(p) for p in data[6]
        ] if data[6] else []
            
        return cls(
            parent=parent,
            name=data[0],
            url=data[1],
            color=Colour(data[2]) if data[2] is not None else None,
            jobs=data[3] or [],
            rates=data[4],
            post_msg=post_msg,
            positions=positions
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
                ", ".join(f"`{p.name}`" for p in self.positions[i:i+4])
                for i in range(0, len(self.positions), 4)
            )

        fields = [
            EmbedField("__Color__", color_field, True),
            EmbedField("__Jobs__", jobs, True),
            EmbedField("__Custom URL__", url_field, False),
            EmbedField("__Employable Positions__", positions, False),
            EmbedField("__Rates__", rates, False)
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
        
        modal = ProfileNameModal(self.name)
        
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
        em_rates = self.progress_emoji(self._rates)

        return (
            f"{U.draw_line(extra=15)}\n"
            "__**Details**__\n"
            f"{em_name} -- Character Name\n"
            f"{em_url} -- Custom URL\n"
            f"{em_color} -- Accent Color\n"
            f"{em_jobs} -- Jobs List\n"
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
        Optional[EmbedField]
    ]:

        return (
            self.name,
            self.url,
            self.color,
            "/".join(self._jobs) if self._jobs else None,
            self.rates_field()
        )
    
################################################################################
    def rates_field(self) -> Optional[EmbedField]:

        if self.rates is None:
            return

        return EmbedField(
            name=f"{BotEmojis.FlyingMoney} __Rates__ {BotEmojis.FlyingMoney}",
            value=(
                f"{self.rates}\n"
                f"{U.draw_line(extra=15)}"
            ),
            inline=False
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
    