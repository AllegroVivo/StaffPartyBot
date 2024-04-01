from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Any, Type, TypeVar, Dict, Tuple, List

from discord import (
    User,
    NotFound,
    Interaction,
    Colour,
    Attachment,
    Embed,
    ForumChannel,
    Forbidden,
    EmbedField,
    Message,
    Thread
)
from UI.Common.CloseMessageView import CloseMessageView
from UI.Profiles import AdditionalImageCaptionModal
from Utilities import (
    Utilities as U,
    FroggeColor,
    ImageType,
    TooManyImagesError,
    NS,
    CharNameNotSetError,
    ExceedsMaxLengthError,
    ChannelTypeError,
    InsufficientPermissionsError
)
from .ProfileAtAGlance import ProfileAtAGlance
from .ProfileDetails import ProfileDetails
from .ProfileImages import ProfileImages
from .ProfilePersonality import ProfilePersonality
from Assets import BotEmojis, BotImages

if TYPE_CHECKING:
    from Classes import ProfileManager, TrainingBot
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
        
        try:
            user = await mgr.bot.fetch_user(profile[1])
        except NotFound:
            return
        
        self: P = cls.__new__(cls)
        
        self._mgr = mgr
        self._user = user
        self._id = profile[0]
        
        self._details = await ProfileDetails.load(self, profile[3:9])
        self._personality = ProfilePersonality.load(self, profile[9:13])
        self._aag = ProfileAtAGlance.load(self, profile[13:23])
        self._images = ProfileImages.load(self, profile[23:25], addl_imgs)
        
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
    def id(self) -> str:
        
        return self._id
    
################################################################################
    @property
    def user(self) -> User:
        
        return self._user
    
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
            self._images.add_additional(image_url, modal.value)
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
                "Run the `/profile images` command to view the changes!"
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
    async def post(self, interaction: Interaction, channel: ForumChannel) -> None:
        
        # Check for unset character name
        if self.char_name == str(NS):
            error = CharNameNotSetError()
            await interaction.response.send_message(embed=error, ephemeral=True)
            return
    
        main_profile, aboutme = self.compile()
        # Check for content length
        if len(main_profile) > 5999:
            error = ExceedsMaxLengthError(len(main_profile))
            await interaction.response.send_message(embed=error, ephemeral=True)
            return
    
        # Prepare embeds
        embeds = [main_profile] + ([aboutme] if aboutme else [])
    
        # Attempt to edit an existing post
        if self.post_message:
            try:
                await self.post_message.edit(embeds=embeds)
                await interaction.respond(embed=self.success_message())
                return
            except NotFound:
                self.post_message = None  # Proceed to post anew if not found
    
        # Check channel type
        if not isinstance(channel, ForumChannel):
            error = ChannelTypeError(channel, "ForumChannel")
            await interaction.respond(embed=error, ephemeral=True)
            return
    
        # Handling threads
        matching_thread = next((t for t in channel.threads if t.name.lower() == self.char_name.lower()), None)
        if matching_thread:
            # Clear history in the matching thread
            async for m in matching_thread.history():
                await m.delete()
            action = matching_thread.send  # type: ignore
        else:
            # Or create a new thread if no matching one
            action = lambda **kw: channel.create_thread(name=self.char_name, **kw)
    
        # Post or create thread and handle permissions error
        try:
            result = await action(embeds=embeds)
            if isinstance(result, Thread):
                self.post_message = await result.fetch_message(result.last_message_id)
            else:
                self.post_message = result
            await interaction.respond(embed=self.success_message())
        except Forbidden:
            error = InsufficientPermissionsError(channel, "Send Messages")
            await interaction.respond(embed=error, ephemeral=True)

################################################################################
    def compile(self) -> Tuple[Embed, Optional[Embed]]:

        char_name, url, color, jobs, rates_field = self._details.compile()
        ataglance = self._aag.compile()
        likes, dislikes, personality, aboutme = self._personality.compile()
        thumbnail, main_image, additional_imgs = self._images.compile()

        if char_name is None:
            char_name = f"Character Name: {str(NS)}"
        elif url is not None:
            char_name = f"{BotEmojis.Envelope}  {char_name}  {BotEmojis.Envelope}"

        description = "** **"
        if jobs is not NS:
            description = (
                f"{U.draw_line(text=jobs)}\n"
                f"{jobs}\n"
                f"{U.draw_line(text=jobs)}"
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

        return main_profile, aboutme
    
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
                f"({self._details.post_message})  {BotEmojis.ArrowLeft}\n"
                f"{U.draw_line(extra=16)}"
            ),
            thumbnail_url=BotImages.ThumbsUpFrog,
            footer_text="By Allegro#6969",
            footer_icon=BotImages.ThumbsUpFrog,
            timestamp=True
        )

################################################################################
