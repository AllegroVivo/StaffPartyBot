from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Type, TypeVar, Any, Tuple

from discord import Interaction, Embed, EmbedField

from UI.Venues import (
    VenueLocationStatusView,
    DataCenterSelectView,
    HousingZoneSelectView,
    LocationElementModal,
    HomeWorldSelectView,
)
from Assets import BotEmojis
from Utilities import (
    Utilities as U,
    DataCenter,
    GameWorld,
    HousingZone,
    InvalidLocationValueError,
)

if TYPE_CHECKING:
    from Classes import Venue, StaffPartyBot, XIVLocation
################################################################################

__all__ = ("VenueLocation",)

VL = TypeVar("VL", bound="VenueLocation")

################################################################################
class VenueLocation:

    __slots__ = (
        "_parent",
        "_dc",
        "_world",
        "_zone",
        "_ward",
        "_plot",
        "_apartment",
        "_room",
        "_subdivision"
    )

################################################################################
    def __init__(self, parent: Venue, **kwargs) -> None:

        self._parent: Venue = parent
        
        self._dc: Optional[DataCenter] = kwargs.get("data_center", None)
        self._world: Optional[GameWorld] = kwargs.get("world", None)
        self._zone: Optional[HousingZone] = kwargs.get("zone", None)
        self._ward: Optional[int] = kwargs.get("ward", None)
        self._plot: Optional[int] = kwargs.get("plot", None)
        self._subdivision: Optional[bool] = kwargs.get("subdivision", False)
        self._apartment: Optional[int] = kwargs.get("apartment", None)
        self._room: Optional[int] = kwargs.get("room", None)

################################################################################
    @classmethod
    def load(cls: Type[VL], parent: Venue, data: Tuple[Any, ...]) -> VL:
        
        return cls(
            parent,
            data_center=DataCenter(data[0]) if data[0] else None,
            world=GameWorld(data[1]) if data[1] else None,
            zone=HousingZone(data[2]) if data[2] else None,
            ward=data[3],
            plot=data[4],
            apartment=data[5],
            room=data[6],
            subdivision=data[7]
        )
    
################################################################################
    @property
    def venue_id(self) -> str:
        
        return self._parent.id
    
################################################################################
    @property
    def bot(self) -> StaffPartyBot:
        
        return self._parent.bot

################################################################################
    @property
    def data_center(self):
        
        return self._dc
    
    @data_center.setter
    def data_center(self, value: Optional[DataCenter]):
        
        self._dc = value
        self.update()
        
################################################################################
    @property
    def world(self):
        
        return self._world
    
    @world.setter
    def world(self, value: Optional[GameWorld]):
        
        self._world = value
        self.update()
        
################################################################################
    @property
    def zone(self):
        
        return self._zone
    
    @zone.setter
    def zone(self, value: Optional[HousingZone]):
        
        self._zone = value
        self.update()

################################################################################
    @property
    def ward(self):
        
        return self._ward
    
    @ward.setter
    def ward(self, value: Optional[int]):
        
        self._ward = value
        self.update()
        
################################################################################
    @property
    def plot(self):
        
        return self._plot
    
    @plot.setter
    def plot(self, value: Optional[int]):
        
        self._plot = value
        self.update()
        
################################################################################
    @property
    def apartment(self):
            
        return self._apartment
    
    @apartment.setter
    def apartment(self, value: Optional[int]):
        
        self._apartment = value
        self.update()
        
################################################################################
    @property
    def room(self):
        
        return self._room
    
    @room.setter
    def room(self, value: Optional[int]):
        
        self._room = value
        self.update()
        
################################################################################
    @property
    def subdivision(self):
        
        return self._subdivision
    
    @subdivision.setter
    def subdivision(self, value: Optional[bool]):
        
        self._subdivision = value
        self.update()
        
################################################################################
    def update(self) -> None:
        
        self.bot.database.update.venue_location(self)

################################################################################
    def format(self) -> str:
        
        ret = ""
        
        if self.data_center:
            ret += f"{self.data_center.name}"
        if self.world:
            ret += f", {self.world.name}"
        if self.zone:
            ret += f", {self.zone.proper_name}"
        if self.ward:
            ret += f", Ward {self.ward}"
        if self.subdivision:
            ret += " (Sub)"
        if self.plot:
            ret += f", Plot {self.plot}"
        if self.apartment:
            ret += f", Apt. {self.apartment}"
        if self.room:
            ret += f", Room {self.room}"
            
        if not ret:
            ret = "`Not Set`"
        
        return ret

################################################################################
    def update_from_xiv_venue(self, xiv: XIVLocation) -> None:
        
        self._dc = DataCenter.from_xiv(xiv.data_center)
        self._world = GameWorld.from_xiv(xiv.world)
        self._zone = HousingZone.from_xiv(xiv.district)
        self._ward = xiv.ward
        self._plot = xiv.plot
        self._apartment = xiv.apartment if xiv.apartment != 0 else None
        self._room = xiv.room if xiv.room != 0 else None
        self._subdivision = xiv.subdivision
        
        self.update()

################################################################################
    def status(self) -> Embed:
        
        fields = [
            EmbedField(
                name="__Data Center__",
                value=f"`{self.data_center.proper_name}`" if self.data_center else "`Not Set`",
                inline=True
            ),
            EmbedField(
                name="__World__",
                value=f"`{self.world.proper_name}`" if self.world else "`Not Set`",
                inline=True
            ),
            EmbedField(
                name="__Housing Zone__",
                value=f"`{self.zone.proper_name}`" if self.zone else "`Not Set`",
                inline=True
            ),
            EmbedField(
                name="__Ward__",
                value=f"`{self.ward}`" if self.ward else "`Not Set`",
                inline=True
            ),
            EmbedField(
                name="__Subdivision__",
                value=str(BotEmojis.Check) if self.subdivision else str(BotEmojis.Cross),
                inline=True
            ),
            EmbedField(
                name="__Plot__",
                value=f"`{self.plot}`" if self.plot else "`Not Set`",
                inline=True
            ),
            EmbedField(
                name="__Apartment__",
                value=f"`{self.apartment}`" if self.apartment else "`Not Set`",
                inline=True
            ),
            EmbedField(
                name="__Room__",
                value=f"`{self.room}`" if self.room else "`Not Set`",
                inline=True
            )
        ]
        
        return U.make_embed(
            title="Location Status",
            description=f"Current location for `{self._parent.name}`\n{U.draw_line(extra=20)}",
            fields=fields
        )
    
################################################################################
    async def menu(self, interaction: Interaction) -> None:
        
        embed = self.status()
        view = VenueLocationStatusView(interaction.user, self)
        
        await interaction.respond(embed=embed, view=view)
        await view.wait()

################################################################################    
    async def set_data_center(self, interaction: Interaction) -> None:
        
        prompt = U.make_embed(
            title="Data Center Selection",
            description="Please select the Data Center for the venue location."
        
        )
        view = DataCenterSelectView(interaction.user)
        
        await interaction.respond(embed=prompt, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            return
        
        self.data_center = view.value
        
################################################################################
    async def set_world(self, interaction: Interaction) -> None:
        
        prompt = U.make_embed(
            title="World Selection",
            description="Please select the World for the venue location."
        
        )
        view = HomeWorldSelectView(interaction.user, self.data_center)
        
        await interaction.respond(embed=prompt, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            return
        
        self.world = view.value
        
################################################################################
    async def set_zone(self, interaction: Interaction) -> None:
        
        prompt = U.make_embed(
            title="Housing Zone Selection",
            description="Please select the Housing Zone for the venue location."
        
        )
        view = HousingZoneSelectView(interaction.user)
        
        await interaction.respond(embed=prompt, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            return
        
        self.zone = view.value
        
################################################################################
    async def toggle_subdivision(self, interaction: Interaction) -> None:
        
        self.subdivision = not self.subdivision
        await interaction.respond("** **", delete_after=0.1)
        
################################################################################
    async def set_location_element(self, interaction: Interaction, element: str) -> None:
        
        modal = LocationElementModal(element, getattr(self, element.lower()))
        
        await interaction.response.send_modal(modal)
        await modal.wait()
        
        if not modal.complete:
            return
        
        if modal.value == -1:
            error = InvalidLocationValueError(element, modal.children[1].value)
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        setattr(self, element.lower(), modal.value)
        
################################################################################
