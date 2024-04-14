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
    ForumTag
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
)
from .ProfileAtAGlance import ProfileAtAGlance
from .ProfileDetails import ProfileDetails
from .ProfileImages import ProfileImages
from .ProfilePersonality import ProfilePersonality

if TYPE_CHECKING:
    from Classes import ProfileManager, TrainingBot, PAvailability
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
    def bot(self) -> TrainingBot:
        
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
        
        if img_type is ImageType.AdditionalImage and len(self._images.additional) >= 10:
            error = TooManyImagesError()
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        if img_type is ImageType.AdditionalImage:
            modal = AdditionalImageCaptionModal()

            await interaction.response.send_modal(modal)
            await modal.wait()
    
            if not modal.complete:
                return

            image_url = await self.bot.dump_image(file)
            await self._images.add_additional(interaction, image_url, modal.value)
            return
        
        await interaction.response.defer()
        image_url = await self.bot.dump_image(file)
        
        if img_type is ImageType.Thumbnail:
            self._images.set_thumbnail(image_url)
        else:
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
    
################################################################################
    async def progress(self, interaction: Interaction) -> None:

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

        await interaction.response.defer(invisible=False)
        
        if self.manager.guild.channel_manager.profiles_channel is None:
            error = ProfileChannelNotSetError()
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        # Check for unset character name
        if self.char_name == str(NS):
            error = CharNameNotSetError()
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        if not self.availability:
            error = AvailabilityNotCompleteError()
            await interaction.respond(embed=error, ephemeral=True)
            return
    
        main_profile, availability, aboutme = self.compile()
        # Check for content length
        if len(main_profile) > 5999:
            error = ExceedsMaxLengthError(len(main_profile))
            await interaction.response.send_message(embed=error, ephemeral=True)
            return
        
        member = self._mgr.guild.parent.get_member(self._user.id)
        
        load_dotenv()
        if os.getenv("DEBUG") == "False":
            if self.post_message is None:
                all_pos_roles = [
                    pos.linked_role for pos in self._mgr.guild.position_manager.positions
                    if pos.linked_role is not None
                ]
                await member.remove_roles(*all_pos_roles)
                
                pos_roles = [
                    pos.linked_role for pos in self._details.positions
                    if pos.linked_role is not None
                ]    
                await member.add_roles(*pos_roles)
    
        # Prepare embeds
        embeds = [main_profile, availability] + ([aboutme] if aboutme else [])
        
        # Prepare persistent view
        view = ProfileUserMuteView(self)
    
        # Attempt to edit an existing post
        if self.post_message:
            try:
                self.bot.add_view(view, message_id=self.post_message.id)
                await self.post_message.edit(embeds=embeds, view=view)
                await interaction.respond(embed=self.success_message())
                return
            except NotFound:
                self.post_message = None  # Proceed to post anew if not found
    
        # Handling threads
        channel = self.manager.guild.channel_manager.profiles_channel
        matching_thread = next((t for t in channel.threads if t.name.lower() == self.char_name.lower()), None)
        if matching_thread:
            # Clear history in the matching thread
            async for m in matching_thread.history():
                await m.delete()
            action = matching_thread.send  # type: ignore
        else:
            # Or create a new thread if no matching one
            tag_text = "Accepting DMs" if self._details.dm_preference else "Not Accepting DMs"
            tags = [t for t in channel.available_tags if t.name.lower() == tag_text.lower()]
            action = lambda **kw: channel.create_thread(name=self.char_name, applied_tags=tags, **kw)

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
            error = InsufficientPermissionsError(channel, "Send Messages")
            await interaction.respond(embed=error, ephemeral=True)

################################################################################
    async def _update_post_components(self) -> None:
        
        if self.post_message is None:
            return
        
        view = ProfileUserMuteView(self)
        self.bot.add_view(view, message_id=self.post_message.id)
        
        try:
            await self.post_message.edit(view=view)
        except NotFound:
            self.post_message = None
        
################################################################################
    def compile(self) -> Tuple[Embed, Embed, Optional[Embed]]:

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

        description = "** **"
        if jobs:
            description = (
                f"{dm_text}\n"
                f"{U.draw_line(text=jobs)}\n"
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
        except:
            error = ProfileExportError()
            await interaction.respond(embed=error, ephemeral=True)
            return
        else:
            await interaction.respond(embed=confirm, ephemeral=True)
        finally:
            os.remove("profile.json")
        
################################################################################
    async def main_menu(self, interaction: Interaction) -> None:
        
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
        
        main_profile, _, _ = self.compile()
        view = CloseMessageView(interaction.user)
        
        await interaction.respond(embed=main_profile, view=view)
        await view.wait()
        
################################################################################
    async def preview_availability(self, interaction: Interaction) -> None:
        
        _, availability, _ = self.compile()
        view = CloseMessageView(interaction.user)
        
        await interaction.respond(embed=availability, view=view)
        await view.wait()
        
################################################################################
    async def preview_aboutme(self, interaction: Interaction) -> None:
        
        _, _, aboutme = self.compile()
        if aboutme is None:
            error = AboutMeNotSetError()
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        view = CloseMessageView(interaction.user)
        
        await interaction.respond(embed=aboutme, view=view)
        await view.wait()
        
################################################################################
    async def venue_mute(self, interaction: Interaction) -> None:
        
        venues = self._mgr.guild.venue_manager.get_venues_by_user(interaction.user.id)
        if not venues:
            error = NoVenuesFoundError()
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        if len(venues) == 1:
            await venues[0].toggle_user_mute(interaction, self.user)
            await interaction.edit()
            return
        
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
            return
        
        for venue_id in view.value:
            venue = self._mgr.guild.venue_manager[venue_id]
            await venue.toggle_user_mute(interaction, self.user)
        
################################################################################
        