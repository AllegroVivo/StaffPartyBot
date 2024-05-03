from __future__ import annotations

from typing import TYPE_CHECKING, List, Any, Dict, Optional

from discord import Interaction, User, ForumChannel, Member, File
from discord.ext.pages import Page, PageGroup

from UI.Common import ConfirmCancelView, Frogginator
from UI.Venues import VenueStatusView, VenueOwnerView
from Utilities import (
    Utilities as U, VenueExistsError, 
    VenueDoesntExistError,
    UnauthorizedError,
    ChannelTypeError,
    TooManyUsersError,
    VenuePendingApprovalError,
    CannotRemoveUserError,
    VenueImportNotFoundError,
    VenueImportError,
    VenueChannelNotSetError,
    RoleType,
)
from .Venue import Venue
from .VenueTag import VenueTag

if TYPE_CHECKING:
    from Classes import GuildData, StaffPartyBot, XIVVenue
################################################################################

__all__ = ("VenueManager",)

################################################################################
class VenueManager:

    __slots__ = (
        "_guild",
        "_venues",
        "_tags",
        "__etiquette_file",
    )
    
    VENUE_ETIQUETTE = (
        "https://canary.discord.com/channels/955933227372122173/"
        "957656105092272208/1231769147113738260"
    )

################################################################################
    def __init__(self, guild: GuildData) -> None:

        self._guild: GuildData = guild
        
        self._venues: List[Venue] = []
        self._tags: List[VenueTag] = []
        self.__etiquette_file: Optional[File] = None
        
################################################################################
    async def _load_all(self, data: Dict[str, Any]) -> None:

        for vdata in data["venues"]:
            self._venues.append(await Venue.load(self, vdata))
            
        for venue in self._venues:
            await venue._update_post_components()
        
################################################################################
    def __getitem__(self, venue_id: str) -> Venue:
        
        for venue in self._venues:
            if venue.id == venue_id:
                return venue
    
################################################################################
    @property
    def bot(self) -> StaffPartyBot:
        
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
    def post_channel(self) -> Optional[ForumChannel]:
        
        return self.guild.channel_manager.venues_channel
    
################################################################################
    @property
    def venues(self) -> List[Venue]:
        
        self._venues.sort(key=lambda x: x.name.lower())
        return self._venues
    
################################################################################
    def get_venue(self, name: str) -> Optional[Venue]:
        
        for venue in self._venues:
            if venue.name.lower() == name.lower():
                return venue
    
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
    async def add_user(
        self, 
        interaction: Interaction, 
        name: str, 
        user: User,
        admin: bool = False
    ) -> None:

        venue = self.get_venue(name)
        if venue is None:
            error = VenueDoesntExistError(name)
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        if len(venue.authorized_users) >= 5 and not admin:
            error = TooManyUsersError(name)
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        if not admin:
            if not await self.authenticate(venue, interaction.user, interaction):
                return
        
        if user in venue.authorized_users:
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
                
                "This will allow them to freely change all elements of the "
                "venue's profile."
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
        
        if venue.pending:
            if admin:
                await venue.approve(interaction)
            else:
                error = VenuePendingApprovalError(name)
                await interaction.respond(embed=error, ephemeral=True)
                return
            
        if not admin:
            if not await self.authenticate(venue, interaction.user, interaction):
                return
            
        await venue.menu(interaction)

################################################################################
    @staticmethod
    async def authenticate(venue: Venue, user: User, interaction: Interaction) -> bool:
        
        if user not in venue.authorized_users:
            error = UnauthorizedError()
            await interaction.respond(embed=error, ephemeral=True)
            return False
        
        return True

################################################################################
    async def post_venue(self, interaction: Interaction, name: str) -> None:

        venue = self.get_venue(name)
        if venue is None:
            error = VenueDoesntExistError(name)
            await interaction.respond(embed=error, ephemeral=True)
            return

        if venue.pending:
            error = VenuePendingApprovalError(name)
            await interaction.respond(embed=error, ephemeral=True)
            return

        if not await self.authenticate(venue, interaction.user, interaction):
            return
        
        await venue.post(interaction, self.post_channel)

################################################################################
    async def venue_report(self, interaction: Interaction) -> None:

        frogginator = Frogginator(
            pages=self._get_venue_page_groups(),
            show_menu=True,
            menu_placeholder="Select a Letter..."
        )
        
        await frogginator.respond(interaction)
            
################################################################################
    def _get_venue_page_groups(self) -> List[PageGroup]:
    
        def _get_initial(name: str) -> str:
            ignored_words = ['The', 'A', 'An']
            words = name.split()
            first_word = (
                words[0] if words[0] not in ignored_words
                else words[1] if len(words) > 1 else words[0]
            )
            return first_word[0].upper()
    
        venues = {}
        for venue in self.venues:
            initial = _get_initial(venue.name)
            if initial not in venues:
                venues[initial] = []
            venues[initial].append(venue)
        
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
                field.name = venue.name + " - (Pending)" if venue.pending else venue.name
                fields.append(field)
                
                if len(fields) >= 12:
                    embed = U.make_embed(
                        title=f"Venues - {initial.upper()}",
                        fields=fields
                    )
                    page = Page(embeds=[embed])
                    pages.append(page)
                    fields = []
    
            if fields:
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
                field.name = venue.name + " - (Pending)" if venue.pending else venue.name
                fields.append(field)
    
                if len(fields) >= 12:
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
    async def signup(
        self, 
        interaction: Interaction,
        name: str,
        user1: Optional[User],
        user2: Optional[User],
        user3: Optional[User]
    ) -> None:

        venue = self.get_venue(name)
        if venue is not None:
            error = VenueExistsError(name)
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        prompt = U.make_embed(
            title="User Confirmation",
            description=(
                "Are you the owner of this venue, or are you making this\n"
                "posting on behalf of the venue owner?"
            )
        )
        view = VenueOwnerView(interaction.user)
        
        await interaction.respond(embed=prompt, view=view)
        await view.wait()
        
        if not view.complete or view.value is None:
            return
        
        if user1 and user2 and user3 and not view.value:
            error = TooManyUsersError(name)
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        venue = Venue.new(self, name)
        venue.add_user(interaction.user)
        self._venues.append(venue)
        
        if user1 is not None:
            venue.add_user(user1)
        if user1 is not None:
            venue.add_user(user1)
        if user2 is not None:
            venue.add_user(user2)
        if user3 is not None:
            venue.add_user(user3)

        confirm = U.make_embed(
            title="Venue Submitted",
            description=(
                f"Venue `{name}` has been submitted for approval.\n\n"

                "Please wait for further instructions from staff on how to\n"
                "proceed with the venue registration process."
            )
        )

        await interaction.respond(embed=confirm, ephemeral=True)
        await self.guild.log.venue_created(venue)
    
################################################################################
    async def remove_user(self, interaction: Interaction, name: str, user: User) -> None:

        venue = self.get_venue(name)
        if venue is None:
            error = VenueDoesntExistError(name)
            await interaction.respond(embed=error, ephemeral=True)
            return

        if not await self._remove_user_error_check(interaction, name, user, venue):
            return
        
        venue.remove_user(user)
        
        confirm = U.make_embed(
            title="User Removed",
            description=(
                f"User {user.mention} has been removed from venue `{name}`."
            )
        )
        await interaction.respond(embed=confirm, ephemeral=True)
        await self.guild.log.venue_user_removed(venue, user)
        
################################################################################
    @staticmethod
    async def _remove_user_error_check(
        interaction: Interaction,
        name: str,
        user: User,
        venue: Venue
    ) -> bool:

        if len(venue.authorized_users) == 0:
            error = CannotRemoveUserError("There are no users on this venue.")
            await interaction.respond(embed=error, ephemeral=True)
            return False

        if user not in venue.authorized_users:
            error = CannotRemoveUserError(f"User {user.mention} is not authorized to access venue `{name}`.")
            await interaction.respond(embed=error, ephemeral=True)
            return False

        if len(venue.authorized_users) == 1:
            error = CannotRemoveUserError("You cannot remove the only user on a venue.")
            await interaction.respond(embed=error, ephemeral=True)
            return False
        
        return True
        
################################################################################
    async def remove_venue(self, interaction: Interaction, name: str) -> None:
        
        venue = self.get_venue(name)
        if venue is None:
            error = VenueDoesntExistError(name)
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        prompt = U.make_embed(
            title="Remove Venue",
            description=(
                f"Are you __**sure**__ you want to remove venue `{name}` "
                f"from the bot?\n\n"
                
                "__This action cannot be undone.__"
            )
        )
        view = ConfirmCancelView(interaction.user)
        
        await interaction.respond(embed=prompt, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            return
        
        await venue.delete()
        
        confirm = U.make_embed(
            title="Venue Removed",
            description=f"Venue `{name}` has been removed from the bot."
        )
        await interaction.followup.send(embed=confirm, ephemeral=True)
        await self.guild.log.venue_removed(venue)
    
################################################################################
    async def import_venue(self, interaction: Interaction, name: str) -> None:
        
        exists = self.get_venue(name)
        if exists:
            error = VenueExistsError(name)
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        final_line = f"Are you sure you want to import venue __`{name}`__?"
        prompt = U.make_embed(
            title="Confirm Venue Import",
            description=(
                "The following venue information will be imported from your "
                "XIV Venues listing into this server, so long as your Discord "
                "user is listed as a manager for the venue.\n\n"

                "* Manager List\n"
                "* Banner Image\n"
                "* Description\n"
                "* Location\n"
                "* Website\n"
                "* Discord\n"
                "* Hiring Status\n"
                "* SFW Status\n"
                "* Tags\n"
                "* Mare ID\n"
                "* Mare Password\n"
                "* Normal Operating Schedule\n"
                "*(Schedule overrides are not imported.)*\n"
                f"{U.draw_line(text=final_line, extra=-2)}\n"
                f"{final_line}"
            )
        )
        view = ConfirmCancelView(interaction.user)
        
        await interaction.respond(embed=prompt, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            return
        
        msg = await interaction.followup.send("Please wait...")
        
        results = [
            v for v in
            await self.bot.veni_client.get_venues_by_manager(interaction.user.id)
            if v.name.lower() == name.lower()
        ]
        
        await msg.delete()
            
        if len(results) == 0:
            error = VenueImportNotFoundError()
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        if len(results) > 1:
            error = VenueImportError()
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        xiv_venue = results[0]
        venue = Venue.new(self, xiv_venue.name)
        await venue.update_from_xiv_venue(interaction, xiv_venue)
        self._venues.append(venue)
        
        await self.guild.log.venue_created(venue)
        
        for auth_user in venue.authorized_users:
            await self.guild.role_manager.add_role(auth_user, RoleType.VenueManagement)
            await self.guild.role_manager.remove_role(auth_user, RoleType.VenuePending)
        
        await venue.menu(interaction)
    
################################################################################
    async def toggle_user_mute(self, interaction: Interaction, name: str, user: User) -> None:

        venue = self.get_venue(name)
        if venue is None:
            error = VenueDoesntExistError(name)
            await interaction.respond(embed=error, ephemeral=True)
            return

        if not await self.authenticate(venue, interaction.user, interaction):
            return
        
        await venue.toggle_user_mute(interaction, user)

################################################################################
    def get_venues_by_user(self, user_id: int) -> List[Venue]:
        
        return [
            v for v in self.venues 
            if user_id in [u.id for u in v.authorized_users]
        ]

################################################################################
    async def on_member_leave(self, member: Member) -> bool:
        """Returns True if a venue was deleted as a result of the member leaving."""
        
        for v in self.venues:
            if member in v.authorized_users:
                if len(v.authorized_users) == 1:
                    self._venues.remove(v)
                    await v.delete()
                    return True
                else:
                    v.remove_user(member._user)
        
        return False

################################################################################
    async def venue_etiquette(self, interaction: Interaction) -> None:
        
        if self.__etiquette_file is None:
            channel = await self.bot.fetch_channel(int(self.VENUE_ETIQUETTE.split("/")[-2]))
            msg = await channel.fetch_message(int(self.VENUE_ETIQUETTE.split("/")[-1]))
            self.__etiquette_file = await msg.attachments[0].to_file()
        
        await interaction.respond(file=self.__etiquette_file, delete_after=60)

################################################################################
    async def bulk_update(self, interaction: Interaction) -> None:
        
        prompt = U.make_embed(
            title="Bulk Update",
            description=(
                "This tool will perform a hard update on all venues, resetting "
                "all data governed by the FFXIV Venues API to the values received "
                "in the transaction and updating all profile components accordingly.\n\n"
                
                "__These values are as follows:__\n"
                "* Manager List\n"
                "* Banner Image\n"
                "* Description\n"
                "* Location\n"
                "* Website\n"
                "* Discord\n"
                "* Hiring Status\n"
                "* SFW Status\n"
                "* Tags\n"
                "* Mare ID\n"
                "* Mare Password\n"
                "* Normal Operating Schedule\n"
                "*(Schedule overrides are not imported.)*\n\n"
                
                "This will take **SOME TIME.** Please confirm that you wish "
                "to proceed with this action."
            )
        )
        view = ConfirmCancelView(interaction.user)
        
        await interaction.respond(embed=prompt, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            return
        
        msg = await interaction.followup.send("Please wait...")
        
        count = 0
        for venue in self.venues:
            await venue.update_from_xiv_venue(interaction)
            await venue._update_post_components()
            count += 1
        
        await msg.delete()
        
        confirm = U.make_embed(
            title="Bulk Update Complete",
            description=f"Successfully updated {count} venues."
        )
        await interaction.respond(embed=confirm)
        
################################################################################
        