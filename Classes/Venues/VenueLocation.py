from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Type, TypeVar, Any, Tuple

from discord import Interaction, Embed, EmbedField

from UI.Venues import (
    VenueLocationStatusView, 
    DataCenterSelectView,
    HousingZoneSelectView,
    WardPlotModal,
    HomeWorldSelectView,
)
from Utilities import (
    Utilities as U,
    DataCenter,
    GameWorld,
    HousingZone
)

if TYPE_CHECKING:
    from Classes import VenueDetails, TrainingBot
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
    )

################################################################################
    def __init__(
        self,
        parent: VenueDetails,
        dc: Optional[DataCenter] = None,
        world: Optional[GameWorld] = None,
        zone: Optional[HousingZone] = None,
        ward: Optional[int] = None,
        plot: Optional[int] = None
    ) -> None:

        self._parent: VenueDetails = parent
        
        self._dc: Optional[DataCenter] = dc
        self._world: Optional[GameWorld] = world
        self._zone: Optional[HousingZone] = zone
        self._ward: Optional[int] = ward
        self._plot: Optional[int] = plot

################################################################################
    @classmethod
    def load(cls: Type[VL], parent: VenueDetails, data: Tuple[Any, ...]) -> VL:
        
        self: VL = cls.__new__(cls)
        
        self._parent = parent
        
        self._dc = DataCenter(data[2]) if data[2] is not None else None
        self._world = GameWorld(data[3]) if data[3] is not None else None
        self._zone = HousingZone(data[4]) if data[4] is not None else None
        self._ward = data[5]
        self._plot = data[6]
        
        return self
    
################################################################################
    @property
    def venue_id(self) -> str:
        
        return self._parent.venue_id
    
################################################################################
    @property
    def bot(self) -> TrainingBot:
        
        return self._parent.bot

################################################################################
    @property
    def data_center(self):
        
        return self._dc
    
    @data_center.setter
    def data_center(self, value):
        
        self._dc = value
        self.update()
        
################################################################################
    @property
    def world(self):
        
        return self._world
    
    @world.setter
    def world(self, value):
        
        self._world = value
        self.update()
        
################################################################################
    @property
    def zone(self):
        
        return self._zone
    
    @zone.setter
    def zone(self, value):
        
        self._zone = value
        self.update()

################################################################################
    @property
    def ward(self):
        
        return self._ward
    
    @ward.setter
    def ward(self, value):
        
        self._ward = value
        self.update()
        
################################################################################
    @property
    def plot(self):
        
        return self._plot
    
    @plot.setter
    def plot(self, value):
        
        self._plot = value
        self.update()
        
################################################################################
    def update(self) -> None:
        
        self.bot.database.update.venue_location(self)
    
################################################################################    
    def status(self) -> Embed:
        
        dc = self._dc.proper_name if self._dc else "`Not Set`"
        world = self._world.proper_name if self._world else "`Not Set`"
        zone = self._zone.proper_name if self._zone else "`Not Set`"
        ward = f"`W{self._ward}`" if self._ward else "`Not Set`"
        plot = f"`P{self._plot}`" if self._plot else "`Not Set`"
        
        return U.make_embed(
            title="Venue Location",
            fields=[
                EmbedField(name="__Data Center__", value=dc, inline=True),
                EmbedField(name="__World__", value=world, inline=True),
                EmbedField(name="__Zone__", value=zone, inline=True),
                EmbedField(name="__Ward__", value=ward, inline=True),
                EmbedField(name="__Plot__", value=plot, inline=True)
            ]
        
        )
    
################################################################################
    def format(self) -> str:
        
        if not (self._dc and self._world and self._zone and self._ward and self._plot):
            return "`Not Set`"
        
        return (
            f"**`{self._dc.proper_name} - {self._world.proper_name} - "
            f"{self._zone.proper_name}: W{self._ward}|P{self._plot}`**"
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
            title="Set Data Center",
            description="Please select a Data Center for this venue."
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
            title="Set World",
            description="Please select this venue's home world."
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
            title="Set Zone",
            description="Please select this venue's housing zone."
        )
        view = HousingZoneSelectView(interaction.user)
        
        await interaction.respond(embed=prompt, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            return
        
        self.zone = view.value
        
################################################################################
    async def set_ward_and_plot(self, interaction: Interaction) -> None:
        
        modal = WardPlotModal(self.ward, self.plot)
        
        await interaction.response.send_modal(modal)
        await modal.wait()
        
        if not modal.complete:
            return
        
        # Update private variable so we don't have to update the database twice
        self._ward = modal.value[0]
        self.plot = modal.value[1]
        
################################################################################
        