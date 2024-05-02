from __future__ import annotations

import json
import os
from typing import TYPE_CHECKING, Optional, Any, Type, TypeVar, Dict, Tuple, List

from discord import (
    User,
    NotFound,
    Interaction,
    Colour,
    Attachment,
    Embed,
    Forbidden,
    EmbedField,
    Message,
    Thread,
    File,
    SelectOption,
    HTTPException
)
from dotenv import load_dotenv

from Assets import BotEmojis, BotImages
from UI.Common import CloseMessageView, ConfirmCancelView
from UI.Profiles import (
    AdditionalImageCaptionModal, 
    ProfilePreView,
    ProfileMainMenuView,
    VenueMuteSelectView,
    ProfileUserMuteView
)
from Utilities import (
    Utilities as U,
    FroggeColor,
    ImageType,
    TooManyImagesError,
    NS,
    CharNameNotSetError,
    ExceedsMaxLengthError,
    InsufficientPermissionsError,
    ProfileExportError,
    ProfileChannelNotSetError,
    AvailabilityNotCompleteError,
    AboutMeNotSetError,
    NoVenuesFoundError,
    GlobalDataCenter,
    ProfileIncompleteError,
)
from Utilities import log

from .ProfileAtAGlance import ProfileAtAGlance
from .ProfileDetails import ProfileDetails
from .ProfileImages import ProfileImages
from .ProfilePersonality import ProfilePersonality

if TYPE_CHECKING:
    from Classes import ProfileManager, StaffPartyBot, PAvailability, Position
################################################################################

__all__ = ("Profile",)

P = TypeVar("P", bound="Profile")

################################################################################
class Profile:
    
    __slots__ = (
        "_mgr",
        "_user",
        "_id",
        "_details",
        "_aag",
        "_personality",
        "_images",
    )

################################################################################
    def __init__(self, mgr: ProfileManager, user: User, **kwargs) -> None:
        
        self._mgr: ProfileManager = mgr
        self._user: User = user
        self._id: str = kwargs.pop("_id")
        
        self._details: ProfileDetails = ProfileDetails(self, **kwargs)
        self._aag: ProfileAtAGlance = ProfileAtAGlance(self, **kwargs)
        self._personality: ProfilePersonality = ProfilePersonality(self, **kwargs)
        self._images: ProfileImages = ProfileImages(self, **kwargs)
    
################################################################################    
    @classmethod
    def new(cls: Type[P], mgr: ProfileManager, user: User) -> P:
        
        log.info("Profiles", f"New profile created for {user.name} ({user.id})")
        new_id = mgr.bot.database.insert.profile(mgr.guild_id, user.id)
        return cls(mgr, user, _id=new_id)
    
################################################################################
    @classmethod
    async def load(cls: Type[P], mgr: ProfileManager, data: Dict[str, Any]) -> Optional[P]:
        
        profile = data["profile"]
        addl_imgs = data["additional_images"]
        hours = data["availability"]
        
        try:
            user = await mgr.bot.fetch_user(profile[1])
        except NotFound:
            return
        
        self: P = cls.__new__(cls)
        
        self._mgr = mgr
        self._user = user
        self._id = profile[0]
        
        self._details = await ProfileDetails.load(self, profile[3:11], hours)
        self._personality = ProfilePersonality.load(self, profile[11:15])
        self._aag = ProfileAtAGlance.load(self, profile[15:24])
        self._images = ProfileImages.load(self, profile[24:26], addl_imgs)
        
        return self
        
################################################################################
    @property
    def bot(self) -> StaffPartyBot:
        
        return self._mgr.bot
    
################################################################################    
    @property
    def manager(self) -> ProfileManager:
        
        return self._mgr
    
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
    def user(self) -> User:
        
        return self._user
    
################################################################################
    @property
    def user_id(self) -> int:
        
        return self._user.id
    
################################################################################
    @property
    def char_name(self) -> str:
        
        return self._details.name
    
################################################################################
    @property
    def color(self) -> Optional[Colour]:
        
        if self._details.color is not None:
            return self._details.color
        
        return FroggeColor.embed_background()
    
################################################################################
    @property
    def post_message(self) -> Optional[Message]:
        
        return self._details.post_message
    
    @post_message.setter
    def post_message(self, value: Optional[Message]) -> None:
        
        self._details.post_message = value
        self._details.update()
        
################################################################################
    @property
    def availability(self) -> List[PAvailability]:
        
        return self._details.availability
    
################################################################################
    @property
    def aboutme(self) -> Optional[str]:
        
        return self._personality.aboutme
    
################################################################################
    @property
    def data_centers(self) -> List[GlobalDataCenter]:
        
        return self._aag.data_centers
    
################################################################################
    @property
    def is_complete(self) -> bool:
        
        return all([
            self._aag.data_centers,
            self._details.positions,
            self._details.availability,
            self._details.name != str(NS),
        ])
        
################################################################################
    async def set_details(self, interaction: Interaction) -> None:
        
        await self._details.menu(interaction)
        
################################################################################
    async def set_ataglance(self, interaction: Interaction) -> None:
        
        await self._aag.menu(interaction)
        
################################################################################
    async def set_personality(self, interaction: Interaction) -> None:
        
        await self._personality.menu(interaction)
        
################################################################################
    async def set_images(self, interaction: Interaction) -> None:
        
        await self._images.menu(interaction)
        
################################################################################
    async def assign_image(self, interaction: Interaction, img_type: ImageType, file: Attachment) -> None:
        
        log.info(
            "Profiles",
            f"User {interaction.user.name} ({interaction.user.id}) is assigning an image"
        )
        
        if img_type is ImageType.AdditionalImage and len(self._images.additional) >= 10:
            log.warning(
                "Profiles",
                f"User {interaction.user.name} ({interaction.user.id}) attempted to assign too many images"
            )
            error = TooManyImagesError()
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        if img_type is ImageType.AdditionalImage:
            log.info("Profiles", "User is assigning an additional image")
            modal = AdditionalImageCaptionModal()

            await interaction.response.send_modal(modal)
            await modal.wait()
    
            if not modal.complete:
                log.debug("Profiles", "User cancelled additional image assignment")
                return

            image_url = await self.bot.dump_image(file)
            await self._images.add_additional(interaction, image_url, modal.value)
            
            log.info("Profiles", "Additional image assigned")
            return
        
        await interaction.response.defer()
        image_url = await self.bot.dump_image(file)
        
        if img_type is ImageType.Thumbnail:
            log.info("Profiles", "User is assigning a thumbnail image")
            self._images.set_thumbnail(image_url)
        else:
            log.info("Profiles", "User is assigning a main image")
            self._images.set_main_image(image_url)
        
        confirm = U.make_embed(
            color=self.color,
            title="Image Assigned",
            description=(
                f"{img_type.proper_name} has been assigned to your profile.\n"
                "Run the `/staffing profile` command to view the changes!"
            )
        )
        
        await interaction.respond(embed=confirm, ephemeral=True)
        
        log.info("Profiles", "Image assigned")
    
################################################################################
    async def progress(self, interaction: Interaction) -> None:
        
        log.info(
            "Profiles",
            f"User {interaction.user.name} ({interaction.user.id}) is checking profile progress"
        )

        em_final = self._details.progress_emoji(self._details._post_msg)
        value = (
            self._details.progress() +
            self._aag.progress() +
            self._personality.progress() +
            self._images.progress() +
            f"{U.draw_line(extra=15)}\n"
            f"{em_final} -- Finalize"
        )

        progress = U.make_embed(
            color=self.color,
            title="Profile Progress",
            description=value,
            timestamp=False
        )
        view = CloseMessageView(interaction.user)

        await interaction.response.send_message(embed=progress, view=view)
        await view.wait()

################################################################################
    async def post(self, interaction: Interaction) -> None:
        
        log.info(
            "Profiles",
            f"User {interaction.user.name} ({interaction.user.id}) is attempting to post profile"
        )

        await interaction.response.defer(invisible=False)
        
        if self.manager.guild.channel_manager.profiles_channel is None:
            log.warning(
                "Profiles",
                "User attempted to post profile without setting profiles channel"
            )
            error = ProfileChannelNotSetError()
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        # Check profile completion
        if not self.is_complete:
            log.warning(
                "Profiles",
                "User attempted to post incomplete profile"
            )
            error = ProfileIncompleteError()
            await interaction.respond(embed=error, ephemeral=True)
            return
    
        main_profile, availability, aboutme = self.compile()
        # Check for content length
        if len(main_profile) > 5999:
            log.info(
                "Profiles",
                "User attempted to post a profile that exceeds the maximum length"
            )
            error = ExceedsMaxLengthError(len(main_profile))
            await interaction.response.send_message(embed=error, ephemeral=True)
            return
        
        member = self._mgr.guild.parent.get_member(self._user.id)
        log.info(
            "Profiles",
            (
                f"User {interaction.user.name} ({interaction.user.id}) is "
                f"posting profile for {member.display_name}"
            )
        )
        
        load_dotenv()
        if os.getenv("DEBUG") == "False":
            log.debug("Profiles", "Debug mode is off - swapping out roles")
            if self.post_message is None:
                all_pos_roles = [
                    pos.linked_role for pos in self._mgr.guild.position_manager.positions
                    if pos.linked_role is not None
                ]
                log.debug(
                    "Profiles",
                    f"Removing all position roles from {member.display_name}"
                )
                await member.remove_roles(*all_pos_roles)
                
                pos_roles = [
                    pos.linked_role for pos in self._details.positions
                    if pos.linked_role is not None
                ]
                log.debug(
                    "Profiles",
                    (
                        f"Adding position roles to {member.display_name}: "
                        f"{', '.join([r.name for r in pos_roles])}"
                    )
                )
                await member.add_roles(*pos_roles)
    
        # Prepare embeds
        embeds = [main_profile, availability] + ([aboutme] if aboutme else [])
        
        # Prepare persistent view
        view = ProfileUserMuteView(self)

        # Handling threads
        channel = self.manager.guild.channel_manager.profiles_channel
        matching_thread = next((t for t in channel.threads if t.name.lower() == self.char_name.lower()), None)
        
        log.debug(
            "Profiles",
            (
                f"Attempting to post profile for {member.display_name} in {channel.name}, "
                f"{'**creating**' if matching_thread is None else '**editing**'} thread"
            )
        )
        
        # Tags - Start with DM status
        tag_text = "Accepting DMs" if self._details.dm_preference else "Not Accepting DMs"
        tags = [t for t in channel.available_tags if t.name.lower() == tag_text.lower()]
        # Add position tags according to weights
        tags += [
            t for t in channel.available_tags 
            if t.name.lower() in 
            [p.name.lower() for p in self._get_top_positions()]
        ]
        
        log.debug(
            "Profiles",
            f"Tags for profile post: {', '.join([t.name for t in tags])}"
        )
    
        # Attempt to edit an existing post
        if self.post_message:
            log.info("Profiles", "Editing existing profile post")
            try:
                self.bot.add_view(view, message_id=self.post_message.id)
                await self.post_message.channel.edit(applied_tags=tags)
                await self.post_message.edit(embeds=embeds, view=view)
                await interaction.respond(embed=self.success_message())
                log.info("Profiles", "Profile post edited successfully")
                return
            except NotFound:
                log.info("Profiles", "Existing profile post not found")
                self.post_message = None  # Proceed to post anew if not found
        
        if matching_thread:
            # Clear the matching thread
            await matching_thread.edit(applied_tags=tags)
            async for m in matching_thread.history():
                await m.delete()
            action = matching_thread.send  # type: ignore
        else:
            # Or create a new thread if no matching one
            action = lambda **kw: channel.create_thread(name=self.char_name, applied_tags=tags, **kw)  # type: ignore

        self.bot.add_view(view)
        
        # Post or create thread and handle permissions error
        try:
            result = await action(embeds=embeds, view=view)
            if isinstance(result, Thread):
                self.post_message = await result.fetch_message(result.last_message_id)
            else:
                self.post_message = result
            await interaction.respond(embed=self.success_message())
        except Forbidden:
            log.warning(
                "Profiles",
                "User attempted to post profile without sufficient bot permissions"
            )
            error = InsufficientPermissionsError(channel, "Send Messages")
            await interaction.respond(embed=error, ephemeral=True)
        else:
            log.info("Profiles", "Profile post created successfully")

################################################################################
    async def _update_post_components(self, addl_attempt: bool = False) -> None:
        
        log.info(
            "Profiles",
            f"Updating profile post components for {self._user.name} ({self._user.id})"
        )
        
        if self.post_message is None:
            log.debug("Profiles", "Post message not found - skipping update")
            return
        
        view = ProfileUserMuteView(self)
        self.bot.add_view(view, message_id=self.post_message.id)
        
        try:
            await self.post_message.edit(view=view)
        except NotFound:
            log.warning(
                "Profiles",
                "Post message not found - clearing post message object"
            )
            self.post_message = None
        except HTTPException as ex:
            if ex.code != 50083 and not addl_attempt:
                log.critical(
                    "Profiles",
                    f"An uncaught error occurred while updating the post components: {ex}"
                )
            log.warning(
                "Profiles",
                "Thread was archived for exceeding 30 day limit - attempting to revive."
            )
            await self.post_message.channel.send("Hey Ur Cute", delete_after=0.1)
            await self._update_post_components(addl_attempt=True)
        else:
            log.info(
                "Profiles",
                "Profile post components updated successfully"
            )
        
################################################################################
    def compile(self) -> Tuple[Embed, Embed, Optional[Embed]]:
        
        log.debug("Profiles", f"Compiling profile embeds for {self._user.name} ({self._user.id})")

        char_name, url, color, jobs, rates_field, availability, dm_pref = self._details.compile()
        ataglance = self._aag.compile()
        likes, dislikes, personality, aboutme = self._personality.compile()
        thumbnail, main_image, additional_imgs = self._images.compile()

        if char_name is None:
            char_name = f"Character Name: {str(NS)}"
        elif url is not None:
            char_name = f"{BotEmojis.Envelope}  {char_name}  {BotEmojis.Envelope}"
        
        dm_emoji = BotEmojis.Check if dm_pref else BotEmojis.Cross 
        dm_text = str(dm_emoji) + (
            " **Accepting staffing-oriented DMs** " 
            if dm_pref 
            else " **Not accepting staffing-oriented DMs** "
        ) + str(dm_emoji)

        description = dm_text
        if jobs:
            description += (
                f"\n{U.draw_line(text=jobs)}\n"
                f"{jobs}\n"
                f"{U.draw_line(text=jobs)}\n"
            )

        fields: List[EmbedField] = []
        if ataglance is not None:
            fields.append(ataglance)
        if rates_field is not None:
            fields.append(rates_field)
        if likes is not None:
            fields.append(likes)
        if dislikes is not None:
            fields.append(dislikes)
        if personality is not None:
            fields.append(personality)
        if additional_imgs is not None:
            additional_imgs.value += U.draw_line(extra=15)
            fields.append(additional_imgs)

        main_profile = U.make_embed(
            color=color or FroggeColor.embed_background(),
            title=char_name,
            description=description,
            url=url,
            thumbnail_url=thumbnail,
            image_url=main_image,
            fields=fields
        )

        return main_profile, availability, aboutme
    
################################################################################
    def success_message(self) -> Embed:

        return U.make_embed(
            color=Colour.brand_green(),
            title="Profile Posted!",
            description=(
                "Hey, good job, you did it! Your profile was posted successfully!\n"
                f"{U.draw_line(extra=37)}\n"
                f"(__Character Name:__ ***{self.char_name}***)\n\n"

                f"{BotEmojis.ArrowRight}  [Check It Out HERE!]"
                f"({self._details.post_message.jump_url})  {BotEmojis.ArrowLeft}\n"
                f"{U.draw_line(extra=16)}"
            ),
            thumbnail_url=BotImages.ThumbsUpFrog,
            timestamp=True
        )

################################################################################
    def _to_dict(self) -> Dict[str, Dict[str, Any]]:
        
        return {
            "user": self._user.id,
            "details": self._details._to_dict(),
            "ataglance": self._aag._to_dict(),
            "personality": self._personality._to_dict(),
            "images": self._images._to_dict()
        }
        
################################################################################
    async def export(self, interaction: Interaction) -> None:
        
        log.info(
            "Profiles",
            f"User {interaction.user.name} ({interaction.user.id}) is exporting profile"
        )
        
        prompt = U.make_embed(
            color=self.color,
            title="Profile Export",
            description=(
                "This will supply you with your profile data in JSON format.\n"
                "Save the following file and use `/profile import` to restore "
                "it in another server with Frogge.\n"
                "Would you like to export it?"
            )
        )
        view = ConfirmCancelView(interaction.user)
        
        await interaction.respond(embed=prompt, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            log.debug("Profiles", "User cancelled profile export")
            return
        
        with open("profile.json", "w") as f:
            f.write(json.dumps(self._to_dict(), indent=4))
        file = File("profile.json")
        
        confirm = U.make_embed(
            title="Profile Exported",
            description=(
                "Your profile data has been exported successfully to your DMs!\n"
                "Please save the provided file for future use."
            )
        )
        
        try:
            await interaction.user.send(embed=confirm, file=file)
        except Exception as ex:
            log.critical(
                "Profiles",
                f"An error occurred while exporting profile: {ex}"
            )
            error = ProfileExportError()
            await interaction.respond(embed=error, ephemeral=True)
            return
        else:
            log.info("Profiles", "Profile exported successfully")
            await interaction.respond(embed=confirm, ephemeral=True)
        finally:
            os.remove("profile.json")
        
################################################################################
    async def main_menu(self, interaction: Interaction) -> None:
        
        log.info(
            "Profiles",
            f"User {interaction.user.name} ({interaction.user.id}) is accessing profile menu"
        )
        
        prompt = U.make_embed(
            color=self.color,
            title="Profile Menu",
            description=(
                "Select a button below to view or edit the corresponding "
                "section of your profile!\n"
            )
        )
        view = ProfileMainMenuView(interaction.user, self)
        
        await interaction.respond(embed=prompt, view=view)
        await view.wait()
        
################################################################################
    async def preview(self, interaction: Interaction) -> None:
        
        log.info(
            "Profiles",
            f"User {interaction.user.name} ({interaction.user.id}) is previewing profile components"
        )

        prompt = U.make_embed(
            color=self.color,
            title="Preview Profile",
            description=(
                "Select the button below corresponding to the section\n"
                "of your profile you would like to preview."
            ),
            timestamp=False
        )
        view = ProfilePreView(interaction.user, self)
        
        await interaction.respond(embed=prompt, view=view)
        await view.wait()
        
################################################################################
    async def preview_profile(self, interaction: Interaction) -> None:
        
        log.info(
            "Profiles",
            f"User {interaction.user.name} ({interaction.user.id}) is previewing profile"
        )
        
        main_profile, _, _ = self.compile()
        view = CloseMessageView(interaction.user)
        
        await interaction.respond(embed=main_profile, view=view)
        await view.wait()
        
################################################################################
    async def preview_availability(self, interaction: Interaction) -> None:
        
        log.info(
            "Profiles",
            f"User {interaction.user.name} ({interaction.user.id}) is previewing availability"
        )
        
        _, availability, _ = self.compile()
        view = CloseMessageView(interaction.user)
        
        await interaction.respond(embed=availability, view=view)
        await view.wait()
        
################################################################################
    async def preview_aboutme(self, interaction: Interaction) -> None:
        
        log.info(
            "Profiles",
            f"User {interaction.user.name} ({interaction.user.id}) is previewing about me"
        )
        
        _, _, aboutme = self.compile()
        if aboutme is None:
            log.warning(
                "Profiles",
                "User attempted to preview about me without setting it"
            )
            error = AboutMeNotSetError()
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        view = CloseMessageView(interaction.user)
        
        await interaction.respond(embed=aboutme, view=view)
        await view.wait()
        
################################################################################
    async def venue_mute(self, interaction: Interaction) -> None:
        
        log.info(
            "Profiles",
            (
                f"User {interaction.user.name} ({interaction.user.id}) is attempting to "
                f"mute/un-mute {self._user.name} for a venue"
            )
        )
        
        venues = self._mgr.guild.venue_manager.get_venues_by_user(interaction.user.id)
        if not venues:
            log.warning(
                "Profiles",
                (
                    "User attempted to mute/un-mute a user for a venue without being "
                    "assigned to any venues"
                )
            )
            error = NoVenuesFoundError()
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        if len(venues) == 1:
            await venues[0].toggle_user_mute(interaction, self.user)
            log.info(
                "Profiles",
                (
                    f"User {interaction.user.name} ({interaction.user.id}) has "
                    f"muted/un-muted {self._user.name} for venue: {venues[0].name}"
                )
            )
            await interaction.edit()
            return
        
        log.debug("Profiles", "Venue manager is selecting the venue(s) to mute/un-mute for")
        
        options = [
            SelectOption(
                label=venue.name,
                value=str(venue.id),
            ) for venue in venues
        ]
        
        prompt = U.make_embed(
            title="Select Venue",
            description=(
                "Pick a venue from the list below to mute or unmute the user for."
            )
        )
        view = VenueMuteSelectView(interaction.user, options)
        
        await interaction.respond(embed=prompt, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            log.debug("Profiles", "User cancelled venue selection")
            return
        
        for venue_id in view.value:
            venue = self._mgr.guild.venue_manager[venue_id]
            await venue.toggle_user_mute(interaction, self.user)
            log.info(
                "Profiles",
                (
                    f"User {interaction.user.name} ({interaction.user.id}) has "
                    f"muted/un-muted {self._user.name} for venue: {venue.name}"
                )
            )
        
################################################################################
    def _get_top_positions(self) -> List[Position]:

        # Map each position to its weight, defaulting to a high number if not found
        weighted_positions = [
            (job, U.JOB_WEIGHTS.get(job.name.lower(), 100)) 
            for job in self._details.positions
        ]
    
        # Sort positions by weight (ascending order so lower numbers are first)
        weighted_positions.sort(key=lambda x: x[1])
    
        # Extract the top four jobs (or fewer if less than four are provided)
        top_positions = [pos[0] for pos in weighted_positions[:4]]
    
        return top_positions

################################################################################
