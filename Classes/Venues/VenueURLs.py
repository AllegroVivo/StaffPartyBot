from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Type, TypeVar, Any, Dict

from discord import Interaction, NotFound

from UI.Venues import VenueDiscordURLModal, VenueWebsiteURLModal, VenueApplicationURLModal
from Utilities import Utilities as U, FroggeColor

if TYPE_CHECKING:
    from Classes import Venue, TrainingBot, XIVVenue
################################################################################

__all__ = ("VenueURLs",)

VD = TypeVar("VD", bound="VenueDetails")

################################################################################
class VenueURLs:

    __slots__ = (
        "_parent",
        "_logo_url",
        "_discord_url",
        "_website_url",
        "_banner_url",
        "_app_url",
    )

################################################################################
    def __init__(self,  parent: Venue, **kwargs) -> None:
        
        self._parent: Venue = parent

        self._discord_url: Optional[str] = kwargs.pop("discord", None)
        self._website_url: Optional[str] = kwargs.pop("website", None)
        self._logo_url: Optional[str] = kwargs.pop("logo", None)
        self._banner_url: Optional[str] = kwargs.pop("banner", None)
        self._app_url: Optional[str] = kwargs.pop("app", None)
    
################################################################################
    @classmethod
    def load(cls: Type[VD], parent: Venue, data: Dict[str, Any]) -> VD:

        return cls(
            parent,
            discord=data.get("discord", None),
            website=data.get("website", None),
            logo=data.get("logo", None),
            banner=data.get("banner", None),
            app=data.get("app", None),
        )
    
################################################################################    
    def __getitem__(self, item: str) -> Optional[str]:
        
        return getattr(self, f"_{item}_url")
        
################################################################################
    def __setitem__(self, key: str, value: Optional[str]):
        
        setattr(self, f"_{key}_url", value)
        self.update()
        
################################################################################    
    @property
    def bot(self) -> TrainingBot:
        
        return self._parent.bot
    
################################################################################
    @property
    def guild_id(self) -> int:
        
        return self._parent.guild_id
    
################################################################################
    @property
    def venue_id(self) -> str:
        
        return self._parent.id

################################################################################
    def update(self) -> None:
        
        self.bot.database.update.venue_urls(self)

################################################################################
    def update_from_xiv_venue(self, venue: XIVVenue) -> None:
        
        self._discord_url = venue.discord
        self._website_url = venue.website
        self._banner_url = venue.banner
        
        self.update()

################################################################################
    async def set_discord_url(self, interaction: Interaction) -> None:
        
        modal = VenueDiscordURLModal(self._discord_url)
        
        await interaction.response.send_modal(modal)
        await modal.wait()
        
        if not modal.complete:
            return
        
        self._discord_url = modal.value
        self.update()

################################################################################
    async def set_website_url(self, interaction: Interaction) -> None:
        
        modal = VenueWebsiteURLModal(self._website_url)
        
        await interaction.response.send_modal(modal)
        await modal.wait()
        
        if not modal.complete:
            return
        
        self._website_url = modal.value
        self.update()

################################################################################
    async def set_application_url(self, interaction: Interaction) -> None:
        
        modal = VenueApplicationURLModal(self._app_url)
        
        await interaction.response.send_modal(modal)
        await modal.wait()
        
        if not modal.complete:
            return
        
        self._app_url = modal.value
        self.update()
        
################################################################################
    async def set_logo(self, interaction: Interaction) -> None:
        
        prompt = U.make_embed(
            title="Set Venue Logo",
            description=(
                "Please upload the image you would like to use as\n"
                "your venue's logo to this channel now.\n\n"
                
                "Please note that for best results, the image\n"
                "should be a square image.\n\n"
                
                "**(The bot is currently listening and will cache the next\n"
                "`.GIF`, `.PNG`, or `.JPG` image you upload to this channel.)**\n"
                f"{U.draw_line(extra=35)}\n"
                "*(Type 'Cancel' to cancel this operation.)*"
            )
        )
        response = await interaction.respond(embed=prompt)

        def check(m):
            return (
                m.author == interaction.user and (
                    (
                        len(m.attachments) > 0 
                        and m.attachments[0].content_type in (
                            "image/png", "image/jpeg", "image/gif"
                        )
                    )
                    or m.content.lower() == "cancel"
                )
            )

        try:
            message = await self.bot.wait_for("message", check=check, timeout=300)
        except TimeoutError:
            embed = U.make_embed(
                title="Timeout",
                description=(
                    "You took too long to upload an image. Please try again."
                ),
                color=FroggeColor.brand_red()
            )
            await interaction.respond(embed=embed)
            return
        
        if message.content.lower() != "cancel":
            self._logo_url = await self.bot.dump_image(message.attachments[0])
            self.update()

        try:
            await message.delete()
        except NotFound:
            pass
        
        try:
            await response.delete_original_response()
        except NotFound:
            pass

################################################################################
