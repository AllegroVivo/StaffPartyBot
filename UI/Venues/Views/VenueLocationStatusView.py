from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Any

from discord import Interaction, User, ButtonStyle
from discord.ui import Button

from UI.Common import FroggeView, CloseMessageButton, FroggeButton
from Utilities import edit_message_helper, DataCenter, GameWorld, HousingZone

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
            WorldButton(self.location.world, self.location.data_center is None),
            ZoneButton(self.location.zone),
            WardPlotButton(self.location.plot),
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
        await self.view.location.set_data_centers(interaction)
        self.set_style(self.view.location.data_center)

        self.view.children[1].disabled = self.view.location.data_center is None

        await edit_message_helper(
            interaction, embed=self.view.location.status(), view=self.view
        )

################################################################################
class WorldButton(FroggeButton):

    def __init__(self, world: Optional[GameWorld], disabled: bool) -> None:

        super().__init__(
            label="World",
            disabled=disabled,
            row=0
        )
        
        self.set_style(world)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.location.set_world(interaction)
        self.set_style(self.view.location.world)

        await edit_message_helper(
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
        
        await edit_message_helper(
            interaction, embed=self.view.location.status(), view=self.view
        )

################################################################################
class WardPlotButton(FroggeButton):

    def __init__(self, plot: Optional[int]) -> None:

        super().__init__(
            disabled=False,
            label="Ward/Plot",
            row=0
        )
        
        self.set_style(plot)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.location.set_ward_and_plot(interaction)
        self.set_style(self.view.location.plot)

        await edit_message_helper(
            interaction, embed=self.view.location.status(), view=self.view
        )

################################################################################
