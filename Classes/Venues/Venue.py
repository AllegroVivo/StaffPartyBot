from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Any, Dict, Type, TypeVar

from discord import (
    User,
    Embed,
    EmbedField,
    Interaction,
    TextChannel,
    Message,
    HTTPException
)

from Assets import BotEmojis
from Utilities import (
    Utilities as U,
    RPLevel,
    VenueSize,
    VenueStyle,
    VenueChannelNotSetError
)
from .InternshipManager import InternshipManager
from .VenueDetails import VenueDetails

if TYPE_CHECKING:
    from Classes import TrainingBot, VenueManager, Position, GuildData
################################################################################

__all__ = ("Venue",)

V = TypeVar("V", bound="Venue")

################################################################################
class Venue:

    __slots__ = (
        "_id",
        "_mgr",
        "_details",
        "_users",
        "_intern_mgr",
    )

################################################################################
    def __init__(
        self,
        mgr: VenueManager, 
        venue_id: str,
        name: str,
        details: Optional[VenueDetails] = None,
        users: Optional[List[User]] = None,
        intern_mgr: Optional[InternshipManager] = None,
    ) -> None:
        
        self._mgr: VenueManager = mgr
        self._id: str = venue_id
        
        self._details = details or VenueDetails(self, name=name)
        self._users: List[User] = users or []
        self._intern_mgr: InternshipManager = intern_mgr or InternshipManager(self)
    
################################################################################
    @classmethod
    def new(cls: Type[V], mgr: VenueManager, name: str) -> V:
        
        new_id = mgr.bot.database.insert.venue(mgr.guild_id, name)
        return cls(mgr, new_id, name)
        
################################################################################    
    @classmethod
    async def load(cls: Type[V], mgr: VenueManager, data: Dict[str, Any]) -> V:
        
        users = []
        if data["user_ids"]:
            for user_id in data["user_ids"]:
                user = await mgr.bot.get_or_fetch_user(user_id)
                if user is not None:
                    users.append(user)
        
        self: V = cls.__new__(cls)
        
        self._mgr = mgr
        self._id = data["details"][0]
        
        self._details = await VenueDetails.load(self, data)
        self._users = users
        self._intern_mgr = InternshipManager.load(self, data["positions"])
        
        return self
    
################################################################################
    @property
    def bot(self) -> TrainingBot:
        
        return self._mgr.bot
    
################################################################################
    @property
    def guild(self) -> GuildData:
        
        return self._mgr.guild 
    
################################################################################
    @property
    def guild_id(self) -> int:
        
        return self._mgr.guild_id
    
################################################################################
    @property
    def id(self) -> str:
        
        return self._id
    
################################################################################
    @property
    def name(self) -> str:
        
        return self._details.name
    
################################################################################
    @property
    def authorized_users(self) -> List[User]:
        
        return self._users
    
################################################################################
    @property
    def nsfw(self) -> bool:
        
        return self._details.aag.nsfw
    
################################################################################
    @property
    def description(self) -> Optional[str]:
        
        return self._details.description
    
################################################################################
    @property
    def rp_level(self) -> Optional[RPLevel]:
        
        return self._details.aag.level
    
################################################################################
    @property
    def style(self) -> Optional[VenueStyle]:
        
        return self._details.aag.style
    
################################################################################
    @property
    def size(self) -> Optional[VenueSize]:
        
        return self._details.aag.size
    
################################################################################
    @property
    def accepting_interns(self) -> bool:
        
        return self._details.accepting
    
################################################################################
    @property
    def post_message(self) -> Optional[Message]:
        
        return self._details.post_message
    
################################################################################
    @post_message.setter
    def post_message(self, value: Optional[Message]) -> None:
        
        self._details.post_message = value
        self._details.update()
        
################################################################################
    @property
    def logo_url(self) -> Optional[str]:
        
        return self._details.logo_url
    
################################################################################
    @property
    def sponsored_positions(self) -> List[Position]:
        
        return self._intern_mgr.sponsored_positions

################################################################################
    @property
    def ataglance_complete(self) -> bool:
        
        return (
            self._details.aag.level is not None and
            self._details.aag.style is not None and
            self._details.aag.size is not None
        ) 
    
################################################################################
    @property
    def discord_url(self) -> Optional[str]:
        
        return self._details.discord_url
    
################################################################################
    @property
    def website_url(self) -> Optional[str]:
        
        return self._details.website_url
    
################################################################################
    def status(self) -> Embed:
        
        return U.make_embed(
            title=f"Venue Profile: __{self._details.name}__",
            description=(
                (self._details.description or "`No description provided.`")
                + f"\n{U.draw_line(extra=33)}"
            ),
            thumbnail_url=self._details.logo_url if self._details.logo_url else None,
            fields=[
                self._authorized_users_field(),
                self._venue_hours_field(),
                self._accepting_field(),
                self._venue_location_field(),
                self._ataglance_field(),
                self._urls_field(),
                self._sponsored_positions_field(),
            ]
        )
    
################################################################################
    def _authorized_users_field(self) -> EmbedField:
        
        return EmbedField(
            name="__Authorized Users__",
            value=(
                ("\n".join([f"• {user.mention}" for user in self._users]))
                if self._users
                else "`No authorized users.`"
            ) + "\n" + U.draw_line(extra=15),
            inline=False,
        )
    
################################################################################
    def _venue_location_field(self) -> EmbedField:
        
        return EmbedField(
            name="__Location__",
            value=self._details.location.format() + "\n" + U.draw_line(extra=15),
            inline=False,
        )
    
################################################################################
    def _venue_hours_field(self) -> EmbedField:
        
        value = self._details.hours.format()
        if not value.endswith("\n"):
            value += "\n"
        
        return EmbedField(
            name="__Open Hours__",
            value=value + U.draw_line(extra=15),
            inline=True,
        )

################################################################################
    def _ataglance_field(self) -> EmbedField:
        
        return EmbedField(
            name=f"{BotEmojis.Eyes} __At a Glance__ {BotEmojis.Eyes}",
            value=self._details.aag.compile(),
            inline=True,
        )
    
################################################################################
    def _accepting_field(self) -> EmbedField:
        
        return EmbedField(
            name="__Accepting Internships__",
            value=(
                f"{BotEmojis.Check}" if self._details.accepting else f"{BotEmojis.Cross}"
            ),
            inline=True,
        )
    
################################################################################
    def _sponsored_positions_field(self) -> EmbedField:
        
        if self.accepting_interns:
            value = (
                (", ".join([f"`{pos.name}`" for pos in self.sponsored_positions]))
                if self.sponsored_positions
                else "`No sponsored positions.`"
            )
        else:
            value = "`Not accepting internships.`"
        
        return EmbedField(
            name="__Sponsored Positions__",
            value=value + "\n" + U.draw_line(extra=15),
            inline=False,
        )
    
################################################################################
    def _urls_field(self, post: bool = False) -> EmbedField:
        
        value = (self._details.discord_url or '`No Discord server provided.`') + "\n\n"
        if self._details.website_url or not post:
            value += "__**Webpage**__\n"
            value += (self._details.website_url or '`No webpage provided.`')
                
        return EmbedField(
            name="__Discord Server__",
            value=value,
            inline=True,
        )

################################################################################
    def add_user(self, user: User) -> None:
        
        self._users.append(user)
        self.update()

################################################################################
    def update(self) -> None:
        
        self.bot.database.update.venue(self)
        
################################################################################
    async def set_name(self, interaction: Interaction) -> None:

        await self._details.set_name(interaction)
        
################################################################################
    async def set_description(self, interaction: Interaction) -> None:

        await self._details.set_description(interaction)
        
################################################################################
    async def set_level(self, interaction: Interaction) -> None:

        await self._details.aag.set_level(interaction)
        
################################################################################
    async def toggle_nsfw(self, interaction: Interaction) -> None:

        await self._details.aag.toggle_nsfw(interaction)
        
################################################################################
    async def set_style(self, interaction: Interaction) -> None:

        await self._details.aag.set_style(interaction)
        
################################################################################
    async def set_size(self, interaction: Interaction) -> None:

        await self._details.aag.set_size(interaction)
        
################################################################################
    async def set_location(self, interaction: Interaction) -> None:

        await self._details.location.menu(interaction)
        
################################################################################
    async def set_hours(self, interaction: Interaction) -> None:

        await self._details.hours.set_availability(interaction)

################################################################################
    async def set_discord_url(self, interaction: Interaction) -> None:
            
        await self._details.set_discord_url(interaction)
        
################################################################################
    async def set_website_url(self, interaction: Interaction) -> None:
    
        await self._details.set_website_url(interaction)
        
################################################################################
    def fmt_location(self) -> str:
        
        return self._details._location.format()

################################################################################
    def fmt_hours(self) -> str:
        
        return self._details._hours.format()

################################################################################
    async def toggle_accepting(self, interaction: Interaction) -> None:

        await self._details.toggle_accepting(interaction)
        
################################################################################
    async def post(self, interaction: Interaction, post_channel: Optional[TextChannel]) -> None:

        if not self.post_message and not post_channel:
            error = VenueChannelNotSetError()
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        if self.post_message is None:
            self.post_message = await post_channel.send(embed=self.compile())
        else:
            try:
                await self.post_message.edit(embed=self.compile())
            except HTTPException:
                self.post_message = await post_channel.send(embed=self.compile())
                
        confirm = U.make_embed(
            title="Venue Profile Posted",
            description=(
                f"The profile for `{self._details.name}` has been posted/updated!\n\n"

                f"{BotEmojis.ArrowRight}  [Check It Out HERE!]"
                f"({self.post_message.jump_url})  {BotEmojis.ArrowLeft}\n"
                f"{U.draw_line(extra=16)}"
            )
        
        )
        
        await interaction.respond(embed=confirm)
        
################################################################################
    async def set_logo(self, interaction: Interaction) -> None:

        await self._details.set_logo(interaction)
        
################################################################################
    def compile(self) -> Embed:
        
        fields = [
            self._venue_hours_field(),
            self._accepting_field(),
            self._venue_location_field(),
            self._ataglance_field(),
            self._sponsored_positions_field(),
        ]
        
        if self._details.discord_url or self._details.website_url:
            fields.insert(4, self._urls_field(post=True))

        return U.make_embed(
            title=f"__{self._details.name}__",
            description=(
                (self._details.description or "`No description provided.`")
                + f"\n{U.draw_line(extra=33)}"
            ),
            thumbnail_url=self._details.logo_url if self._details.logo_url else None,
            fields=fields
        )
    
################################################################################
    async def set_sponsored_positions(self, interaction: Interaction) -> None:

        await self._intern_mgr.set_sponsored_positions(interaction)
        
################################################################################
