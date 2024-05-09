from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Any

from discord import Interaction, User, ButtonStyle

from UI.Common import FroggeView, CloseMessageButton, FroggeButton
from Utilities import DataCenter, GameWorld, HousingZone

if TYPE_CHECKING:
    from Classes import VenueLocation
################################################################################

__all__ = ("VenueLocationStatusView",)

################################################################################
class VenueLocationStatusView(FroggeView):

    def __init__(self, user: User, location: VenueLocation) -> None:

        super().__init__(user)

        self.location: VenueLocation = location

        button_list = [
            DataCenterButton(self.location.data_center),
            WorldButton(self.location.world),
            ZoneButton(self.location.zone),
            SubdivisionToggleButton(self.location.subdivision),
            WardButton(self.location.ward),
            PlotButton(self.location.plot),
            ApartmentButton(self.location.apartment),
            RoomButton(self.location.room),
            CloseMessageButton()
        ]
        for btn in button_list:
            self.add_item(btn)

################################################################################
class DataCenterButton(FroggeButton):

    def __init__(self, dc: Optional[DataCenter]) -> None:

        super().__init__(
            label="Data Center",
            disabled=False,
            row=0
        )
        
        self.set_style(dc)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.location.set_data_center(interaction)
        self.set_style(self.view.location.data_center)

        await self.view.edit_message_helper(
            interaction, embed=self.view.location.status(), view=self.view
        )

################################################################################
class WorldButton(FroggeButton):

    def __init__(self, world: Optional[GameWorld]) -> None:

        super().__init__(
            label="World",
            disabled=False,
            row=0
        )
        
        self.set_style(world)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.location.set_world(interaction)
        self.set_style(self.view.location.world)

        await self.view.edit_message_helper(
            interaction, embed=self.view.location.status(), view=self.view
        )

################################################################################
class ZoneButton(FroggeButton):

    def __init__(self, zone: Optional[HousingZone]) -> None:

        super().__init__(
            label="Zone",
            disabled=False,
            row=0
        )
        
        self.set_style(zone)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.location.set_zone(interaction)
        self.set_style(self.view.location.zone)
        
        await self.view.edit_message_helper(
            interaction, embed=self.view.location.status(), view=self.view
        )

################################################################################
class SubdivisionToggleButton(FroggeButton):
    
    def __init__(self, subdiv: bool) -> None:
        
        super().__init__(
            label="Subdivision",
            disabled=False,
            row=0
        )
        
        self.set_style(subdiv)
        
    def set_style(self, attribute: Optional[Any]) -> None:
        
        self.style = ButtonStyle.success if attribute else ButtonStyle.danger

    async def callback(self, interaction: Interaction) -> None:
        await self.view.location.toggle_subdivision(interaction)
        self.set_style(self.view.location.subdivision)

        await self.view.edit_message_helper(
            interaction, embed=self.view.location.status(), view=self.view
        )
        
################################################################################
class WardButton(FroggeButton):

    def __init__(self, ward: Optional[int]) -> None:

        super().__init__(
            disabled=False,
            label="Ward",
            row=1
        )
        
        self.set_style(ward)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.location.set_location_element(interaction, "Ward")
        self.set_style(self.view.location.ward)

        await self.view.edit_message_helper(
            interaction, embed=self.view.location.status(), view=self.view
        )

################################################################################
class PlotButton(FroggeButton):

    def __init__(self, plot: Optional[int]) -> None:

        super().__init__(
            disabled=False,
            label="Plot",
            row=1
        )
        
        self.set_style(plot)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.location.set_location_element(interaction, "Plot")
        self.set_style(self.view.location.plot)

        await self.view.edit_message_helper(
            interaction, embed=self.view.location.status(), view=self.view
        )

################################################################################
class ApartmentButton(FroggeButton):

    def __init__(self, apt: Optional[int]) -> None:

        super().__init__(
            disabled=False,
            label="Apartment",
            row=1
        )
        
        self.set_style(apt)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.location.set_location_element(interaction, "Apartment")
        self.set_style(self.view.location.apartment)

        await self.view.edit_message_helper(
            interaction, embed=self.view.location.status(), view=self.view
        )
        
################################################################################
class RoomButton(FroggeButton):

    def __init__(self, room: Optional[int]) -> None:

        super().__init__(
            disabled=False,
            label="Room",
            row=1
        )
        
        self.set_style(room)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.location.set_location_element(interaction, "Room")
        self.set_style(self.view.location.room)

        await self.view.edit_message_helper(
            interaction, embed=self.view.location.status(), view=self.view
        )
        
################################################################################
