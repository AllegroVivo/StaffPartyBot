from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Any

from discord import User, ButtonStyle, Role

from Assets import BotEmojis
from UI.Common import FroggeView, CloseMessageButton, FroggeButton
from Utilities import FroggeColor

if TYPE_CHECKING:
    from Classes import HireableService
################################################################################

__all__ = ("HireableServiceStatusView",)

################################################################################
class FroggleButton(FroggeButton):
    
    def set_style(self, attribute: Optional[Any]) -> None:
        if not attribute:
            self.style = ButtonStyle.danger
            self.emoji = None
        else:
            self.style = ButtonStyle.success
            self.emoji = BotEmojis.Check
        
################################################################################
class HireableServiceStatusView(FroggeView):

    def __init__(self, user: User, service: HireableService):
        
        super().__init__(user, close_on_complete=True)
        
        self.service: HireableService = service
        
        button_list = [
            NameButton(),
            ColorButton(service.color),
            RoleButton(service.role),
            NSFWToggleButton(service.configuration.nsfw),
            RatesToggleButton(service.configuration.rates),
            StyleToggleButton(service.configuration.style),
            URLsButton(service.configuration.urls),
            ImagesButton(service.configuration.images),
            ScheduleButton(service.configuration.schedule),
            CloseMessageButton(),
        ]
        for btn in button_list:
            self.add_item(btn)
        
################################################################################
class NameButton(FroggeButton):
    
    def __init__(self):
        
        super().__init__(
            style=ButtonStyle.primary,
            label="Name",
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction):
        await self.view.service.set_name(interaction)
        await interaction.edit(embed=self.view.service.status())
        
################################################################################
class ColorButton(FroggeButton):
    
    def __init__(self, color: Optional[FroggeColor]):
        
        super().__init__(
            label="Color",
            disabled=False,
            row=0
        )
        
        self.set_style(color)
        
    async def callback(self, interaction):
        await self.view.service.set_color(interaction)
        self.set_style(self.view.service.color)
        
        await interaction.edit(embed=self.view.service.status(), view=self.view)
        
################################################################################
class RoleButton(FroggeButton):
    
    def __init__(self, role: Optional[Role]):
        
        super().__init__(
            label="Role",
            disabled=False,
            row=0
        )
        
        self.set_style(role)
        
    async def callback(self, interaction):
        await self.view.service.set_role(interaction)
        self.set_style(self.view.service.role)
        
        await self.view.edit_message_helper(
            interaction, embed=self.view.service.status(), view=self.view
        )
        
################################################################################
class NSFWToggleButton(FroggleButton):
    
    def __init__(self, nsfw: bool):
        
        super().__init__(
            label="NSFW",
            disabled=False,
            row=1
        )
        
        self.set_style(nsfw)
        
    async def callback(self, interaction):
        self.view.service.toggle_nsfw()
        self.set_style(self.view.service.configuration.nsfw)
        
        await interaction.edit(embed=self.view.service.status(), view=self.view)
        
################################################################################
class RatesToggleButton(FroggleButton):
    
    def __init__(self, rates: bool):
        
        super().__init__(
            label="Rates",
            disabled=False,
            row=1
        )
        
        self.set_style(rates)
        
    async def callback(self, interaction):
        self.view.service.toggle_rates()
        self.set_style(self.view.service.configuration.rates)
        
        await interaction.edit(embed=self.view.service.status(), view=self.view)
        
################################################################################
class StyleToggleButton(FroggleButton):
    
    def __init__(self, style: bool):
        
        super().__init__(
            label="Style",
            disabled=False,
            row=1
        )
        
        self.set_style(style)
        
    async def callback(self, interaction):
        self.view.service.toggle_style()
        self.set_style(self.view.service.configuration.style)
        
        await interaction.edit(embed=self.view.service.status(), view=self.view)
        
################################################################################
class URLsButton(FroggleButton):
    
    def __init__(self, urls: bool):
        
        super().__init__(
            label="URLs",
            disabled=False,
            row=2
        )
        
        self.set_style(urls)
        
    async def callback(self, interaction):
        self.view.service.toggle_urls()
        self.set_style(self.view.service.configuration.urls)
        
        await interaction.edit(embed=self.view.service.status(), view=self.view)
        
################################################################################
class ImagesButton(FroggleButton):
    
    def __init__(self, images: bool):
        
        super().__init__(
            label="Images",
            disabled=False,
            row=2
        )
        
        self.set_style(images)
        
    async def callback(self, interaction):
        self.view.service.toggle_images()
        self.set_style(self.view.service.configuration.images)
        
        await interaction.edit(embed=self.view.service.status(), view=self.view)
        
################################################################################
class ScheduleButton(FroggleButton):
    
    def __init__(self, schedule: bool):
        
        super().__init__(
            label="Schedule",
            disabled=False,
            row=2
        )
        
        self.set_style(schedule)
        
    async def callback(self, interaction):
        self.view.service.toggle_schedule()
        self.set_style(self.view.service.configuration.schedule)
        
        await interaction.edit(embed=self.view.service.status(), view=self.view)
        
################################################################################

        