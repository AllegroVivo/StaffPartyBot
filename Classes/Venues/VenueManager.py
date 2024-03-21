from __future__ import annotations

from typing import TYPE_CHECKING, List, Any, Dict, Optional

from discord import Interaction, User, TextChannel
from discord.ext.pages import Page, PageGroup

from UI.Common import ConfirmCancelView, Frogginator
from UI.Venues import VenueStatusView
from Utilities import (
    Utilities as U, VenueExistsError, 
    VenueDoesntExistError,
    UnauthorizedError,
    ChannelTypeError,
)
from .Venue import Venue

if TYPE_CHECKING:
    from Classes import GuildData, TrainingBot
################################################################################

__all__ = ("VenueManager",)

################################################################################
class VenueManager:

    __slots__ = (
        "_guild",
        "_venues",
        "_channel",
    )

################################################################################
    def __init__(self, guild: GuildData) -> None:

        self._guild: GuildData = guild
        
        self._venues: List[Venue] = []
        self._channel: Optional[TextChannel] = None
        
################################################################################
    async def _load_all(self, data: Dict[str, Any]) -> None:

        venue_channel = data["bot_config"][4]
        if venue_channel is not None:
            venue_channel = await self.bot.get_or_fetch_channel(venue_channel)

        self._channel = venue_channel

        for _, venue_data in data["venues"].items():
            self._venues.append(await Venue.load(self, venue_data))
        
################################################################################
    @property
    def bot(self) -> TrainingBot:
        
        return self._guild.bot

################################################################################
    @property
    def guild(self) -> GuildData:
        
        return self._guild
    
################################################################################
    @property
    def guild_id(self) -> int:
        
        return self._guild.guild_id
    
################################################################################
    @property
    def post_channel(self) -> Optional[TextChannel]:
        
        return self._channel
    
################################################################################
    @property
    def venues(self) -> List[Venue]:
        
        return self._venues
    
################################################################################
    def get_venue(self, name: str) -> Optional[Venue]:
        
        for venue in self._venues:
            if venue.name.lower() == name.lower():
                return venue
    
################################################################################
    def update(self) -> None:
        
        self.bot.database.update.venue_post_channel(
            self.guild_id, self._channel.id if self._channel else None
        )
        
################################################################################
    async def add_venue(self, interaction: Interaction, name: str, user: User) -> None:
        
        venue = self.get_venue(name)
        if venue is not None:
            error = VenueExistsError(name)
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        venue = Venue.new(self, name)
        venue.add_user(user)
        self._venues.append(venue)
        
        confirm = U.make_embed(
            title="Venue Added",
            description=(
                f"Venue `{name}` has been added to the bot.\n\n"
                
                "You can assign additional authorized users to this\n"
                "venue using the `/admin venue_user` command."
            )
        )
        
        await interaction.respond(embed=confirm, ephemeral=True)
        await self.guild.log.venue_created(venue)

################################################################################
    async def add_user(self, interaction: Interaction, name: str, user: User) -> None:

        venue = self.get_venue(name)
        if venue is None:
            error = VenueDoesntExistError(name)
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        if user in venue._users:
            embed = U.make_embed(
                title="User Already Authorized",
                description=(
                    f"User {user.mention} is already authorized to access venue `{name}`."
                )
            )
            await interaction.respond(embed=embed, ephemeral=True)
            return
        
        prompt = U.make_embed(
            title="Authorize User",
            description=(
                f"Are you sure you want to authorize {user.mention} to\n"
                f"access venue `{name}`?\n\n"
                
                "This will allow them to change all aspects of the venue\n"
                "aside from authorized users."
            )
        )
        view = ConfirmCancelView(interaction.user)
        
        await interaction.respond(embed=prompt, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            return
        
        venue.add_user(user)
        
        confirm = U.make_embed(
            title="User Authorized",
            description=(
                f"User {user.mention} has been authorized to access venue `{name}`."
            )
        )
        await interaction.followup.send(embed=confirm, ephemeral=True)
        await self.guild.log.venue_user_added(venue, user)

################################################################################
    async def venue_menu(self, interaction: Interaction, name: str, admin: bool = False) -> None:

        venue = self.get_venue(name)
        if venue is None:
            error = VenueDoesntExistError(name)
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        if not admin:
            if not await self.authenticate(venue, interaction.user, interaction):
                return
            
        embed = venue.status()
        view = VenueStatusView(interaction.user, venue)
        
        await interaction.respond(embed=embed, view=view)
        await view.wait()

################################################################################
    @staticmethod
    async def authenticate(venue: Venue, user: User, interaction: Interaction) -> bool:
        
        if user not in venue.authorized_users:
            error = UnauthorizedError()
            await interaction.respond(embed=error, ephemeral=True)
            return False
        
        return True

################################################################################
    async def set_venue_channel(self, interaction: Interaction, channel: TextChannel) -> None:

        if not isinstance(channel, TextChannel):
            embed = ChannelTypeError(channel, "TextChannel")
        else:
            self._channel = channel
            self.update()
            embed = U.make_embed(
                title="Venue Channel Set!",
                description=f"Venue channel has been set to {channel.mention}!"
            )

        await interaction.respond(embed=embed, ephemeral=True)

################################################################################
    async def post_venue(self, interaction: Interaction, name: str) -> None:

        venue = self.get_venue(name)
        if venue is None:
            error = VenueDoesntExistError(name)
            await interaction.respond(embed=error, ephemeral=True)
            return

        if not await self.authenticate(venue, interaction.user, interaction):
            return
        
        await venue.post(interaction, self._channel)

################################################################################
    async def venue_report(self, interaction: Interaction) -> None:
        
        def _get_initial(name: str) -> str:
            ignored_words = ['The', 'A', 'An']
            words = name.split()
            first_word = (
                words[0] if words[0] not in ignored_words 
                else words[1] if len(words) > 1 else words[0]
            )
            return first_word[0].upper()

        sorted_venues = {}
        for venue in self._venues:
            initial = _get_initial(venue.name)
            if initial not in sorted_venues:
                sorted_venues[initial] = []
            sorted_venues[initial].append(venue)
            
        page_groups = self._get_venue_page_groups(sorted_venues)
        frogginator = Frogginator(
            pages=page_groups,
            show_menu=True,
            menu_placeholder="Select a Letter..."
        )
        
        await frogginator.respond(interaction)
            
################################################################################
    @staticmethod
    def _get_venue_page_groups(venues: Dict[str, List[Venue]]) -> List[PageGroup]:
        
        ret = []
        xyz_group = []
        
        for initial, venue_list in venues.items():
            if initial in ['X', 'Y', 'Z']:
                xyz_group.extend(venue_list)
                continue
            
            pages = []
            fields = []
            for venue in venue_list:
                field = venue._authorized_users_field(inline=True)
                field.name = venue.name
                fields.append(field)
                
                if len(fields) >= 9:
                    embed = U.make_embed(
                        title=f"Venues - {initial.upper()}",
                        fields=fields
                    )
                    page = Page(embeds=[embed])
                    pages.append(page)
                    fields = []

            embed = U.make_embed(
                title=f"Venues - {initial.upper()}",
                fields=fields
            )
            page = Page(embeds=[embed])
            pages.append(page)            
            group = PageGroup(pages=pages, label=initial.upper())
            ret.append(group)
    
        if xyz_group:
            pages = []
            fields = []
            for venue in xyz_group:
                field = venue._authorized_users_field(inline=True)
                field.name = venue.name
                fields.append(field)
    
                if len(fields) >= 9:
                    embed = U.make_embed(title="Venues - XYZ", fields=fields)
                    page = Page(embeds=[embed])
                    pages.append(page)
                    fields = []
    
            if fields:  # Check if there are leftover fields not yet added to a page
                embed = U.make_embed(title="Venues - XYZ", fields=fields)
                page = Page(embeds=[embed])
                pages.append(page)
    
            xyz_group = PageGroup(pages=pages, label="XYZ")
            ret.append(xyz_group)
        
        ret.sort(key=lambda x: x.label)
        return ret
    
################################################################################
    