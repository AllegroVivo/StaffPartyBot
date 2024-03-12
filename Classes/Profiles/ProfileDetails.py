from __future__ import annotations

from discord import Colour, Embed, Interaction, EmbedField
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
from Utilities import Utilities as U, NS

if TYPE_CHECKING:
    from Classes import Profile
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
        "_post_url"
    )

################################################################################
    def __init__(self, parent: Profile, **kwargs) -> None:
        
        super().__init__(parent)

        self._name: Optional[str] = kwargs.pop("name", None)
        self._url: Optional[str] = kwargs.pop("url", None) or kwargs.pop("custom_url", None)
        self._color: Optional[Colour] = kwargs.pop("color", None) or kwargs.pop("colour", None)
        self._jobs: List[str] = kwargs.pop("jobs", []) or []
        self._rates: Optional[str] = kwargs.pop("rates", None)
        self._post_url: Optional[str] = kwargs.pop("post_url", None)

################################################################################
    @classmethod
    def load(cls: Type[PD], parent: Profile, data: Tuple[Any, ...]) -> PD:
        
        return cls(
            parent=parent,
            name=data[0],
            url=data[1],
            color=Colour(data[2]) if data[2] is not None else None,
            jobs=data[3] or [],
            rates=data[4],
            post_url=data[5]
        )
    
################################################################################
    @property
    def name(self) -> str:
        
        return self._name or str(NS)
    
################################################################################
    @name.setter
    def name(self, value: Optional[str]) -> None:
        
        self._name = value
        self.update()
        
################################################################################    
    @property
    def url(self) -> Optional[str]:
        
        return self._url
    
################################################################################
    @url.setter
    def url(self, value: Optional[str]) -> None:
        
        self._url = value
        self.update()
        
################################################################################    
    @property
    def color(self) -> Optional[Colour]:
        
        return self._color
    
################################################################################
    @color.setter
    def color(self, value: Optional[Colour]) -> None:
        
        self._color = value
        self.update()
        
################################################################################    
    @property
    def jobs(self) -> List[str]:
        
        return self._jobs
    
################################################################################
    @jobs.setter
    def jobs(self, value: List[str]) -> None:
        
        self._jobs = value
        self.update()
        
################################################################################    
    @property
    def rates(self) -> Optional[str]:
        
        return self._rates
    
################################################################################
    @rates.setter
    def rates(self, value: Optional[str]) -> None:
        
        self._rates = value
        self.update()
        
################################################################################    
    @property
    def post_url(self) -> Optional[str]:
        
        return self._post_url
    
################################################################################
    @post_url.setter
    def post_url(self, value: Optional[str]) -> None:
        
        self._post_url = value
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

        fields = [
            EmbedField("__Color__", color_field, True),
            EmbedField("__Jobs__", jobs, True),
            EmbedField("__Custom URL__", url_field, False),
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

        if self.rates is NS:
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
