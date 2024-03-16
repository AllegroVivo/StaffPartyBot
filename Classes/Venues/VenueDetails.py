from __future__ import annotations
from asyncio import TimeoutError
from typing import TYPE_CHECKING, Optional, Type, TypeVar, Any, Dict

from discord import Interaction, Message

from UI.Venues import VenueNameModal, VenueDescriptionModal
from Utilities import Utilities as U
from .VenueAtAGlance import VenueAtAGlance
from .VenueHours import VenueHours
from .VenueLocation import VenueLocation

if TYPE_CHECKING:
    from Classes import Venue, TrainingBot
################################################################################

__all__ = ("VenueDetails",)

VD = TypeVar("VD", bound="VenueDetails")

################################################################################
class VenueDetails:

    __slots__ = (
        "_parent",
        "_name",
        "_description",
        "_location",
        "_hours",
        "_aag",
        "_accepting",
        "_post_msg",
        "_logo_url",
    )

################################################################################
    def __init__(
        self, 
        parent: Venue,
        name: Optional[str] = None,
        description: Optional[str] = None,
        location: Optional[VenueLocation] = None,
        hours: Optional[VenueHours] = None,
        aag: Optional[VenueAtAGlance] = None,
        accepting: bool = True,
        post_msg: Optional[Message] = None,
        logo_url: Optional[str] = None
    ) -> None:
        
        self._parent: Venue = parent
        
        self._name: Optional[str] = name
        self._description: Optional[str] = description
        self._accepting: bool = accepting
        self._post_msg: Optional[Message] = post_msg
        self._logo_url: Optional[str] = logo_url
        
        self._location: VenueLocation = location or VenueLocation(self)
        self._hours: VenueHours = hours or VenueHours(self)
        self._aag: VenueAtAGlance = aag or VenueAtAGlance(self)
    
################################################################################
    @classmethod
    async def load(cls: Type[VD], parent: Venue, data: Dict[str, Any]) -> VD:

        details = data["details"]
        
        post_url = details[5]
        message = None
        
        if post_url:
            url_parts = post_url.split("/")
            channel = await parent.bot.get_or_fetch_channel(int(url_parts[-2]))
            if channel is not None:
                try:
                    message = await channel.fetch_message(int(url_parts[-1]))  # type: ignore
                except:
                    pass
        
        self: VD = cls.__new__(cls)
        
        self._parent = parent
        
        self._name = details[2]
        self._description = details[3]
        self._accepting = details[4]
        self._logo_url = details[6]
        self._post_msg = message
        
        self._hours = VenueHours.load(self, data["hours"])
        self._location = VenueLocation.load(self, data["location"])
        self._aag = VenueAtAGlance.load(self, data["aag"])
        
        return self
        
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
    def venue(self) -> Venue:
        
        return self._parent
    
################################################################################
    @property
    def venue_id(self) -> str:
        
        return self._parent.id
    
################################################################################
    @property
    def aag(self) -> VenueAtAGlance:
        
        return self._aag 

################################################################################
    @property
    def name(self) -> str:
        
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        
        self._name = value
        self.update()
        
################################################################################
    @property
    def description(self) -> Optional[str]:
        
        return self._description
    
    @description.setter
    def description(self, value: Optional[str]) -> None:
        
        self._description = value
        self.update()
    
################################################################################
    @property
    def accepting(self) -> bool:
        
        return self._accepting
    
    @accepting.setter
    def accepting(self, value: bool) -> None:
        
        self._accepting = value
        self.update()
        
################################################################################
    @property
    def location(self) -> VenueLocation:
        
        return self._location
    
################################################################################
    @property
    def hours(self) -> VenueHours:
        
        return self._hours
    
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
    def logo_url(self) -> Optional[str]:
        
        return self._logo_url
    
    @logo_url.setter
    def logo_url(self, value: Optional[str]) -> None:
        
        self._logo_url = value
        self.update()
        
################################################################################
    def update(self) -> None:
        
        self.bot.database.update.venue_details(self)
        
################################################################################
    async def set_name(self, interaction: Interaction) -> None:

        modal = VenueNameModal(self.name)
        
        await interaction.response.send_modal(modal)
        await modal.wait()
        
        if not modal.complete:
            return
        
        self.name = modal.value

################################################################################
    async def set_description(self, interaction: Interaction) -> None:
        
        modal = VenueDescriptionModal(self.description)
        
        await interaction.response.send_modal(modal)
        await modal.wait()
        
        if not modal.complete:
            return
        
        self.description = modal.value
        
################################################################################
    async def toggle_accepting(self, interaction: Interaction) -> None:
        
        self.accepting = not self.accepting
        await interaction.respond("** **", delete_after=0.1)
        
################################################################################
    async def set_logo(self, interaction: Interaction) -> None:
        
        prompt = U.make_embed(
            title="Set Logo",
            description=(
                "Please upload the image you would like to use as your "
                "venue's logo to this channel now.\n\n"
                
                "**(The bot is currently listening and will cache the next "
                "`.PNG` or `.JPG` image you upload to this channel.)**\n"
                f"{U.draw_line(extra=30)}"
            )
        )
        
        response = await interaction.respond(embed=prompt)
        
        def check(m):
            return (
                m.author == interaction.user 
                and len(m.attachments) > 0
                and m.attachments[0].content_type in ("image/png", "image/jpeg")
            )
        
        try:
            message = await self.bot.wait_for("message", check=check, timeout=300)
        except TimeoutError:
            embed = U.make_embed(
                title="Timeout",
                description=(
                    "You took too long to upload an image. Please try again."
                )
            )
            await interaction.respond(embed=embed, ephemeral=True)
            return
        
        self.logo_url = await self.bot.dump_image(message.attachments[0])
        
        await message.delete()
        await response.delete_original_response()
        
################################################################################
        