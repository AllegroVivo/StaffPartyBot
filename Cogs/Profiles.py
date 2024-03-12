from typing import TYPE_CHECKING

from discord import (
    ApplicationContext,
    Cog,
    SlashCommandGroup,
    Option,
    OptionChoice,
    SlashCommandOptionType,
)

from Utilities import ImageType

if TYPE_CHECKING:
    from Classes import TrainingBot
################################################################################
class Profiles(Cog):

    def __init__(self, bot: "TrainingBot"):

        self.bot: "TrainingBot" = bot

################################################################################

    profiles = SlashCommandGroup(
        name="profile",
        description="Commands for Profile creation and management."
    )

################################################################################
    @profiles.command(
        name="details",
        description="View and edit Name, URL, Color, Jobs, and Rates."
    )
    async def profile_details(self, ctx: ApplicationContext) -> None:

        profile = self.bot[ctx.guild_id].get_profile(ctx.user)
        await profile.set_details(ctx.interaction)

################################################################################
    @profiles.command(
        name="ataglance",
        description="View and edit Gender, Age, Height, and more."
    )
    async def profile_ataglance(self, ctx: ApplicationContext) -> None:

        profile = self.bot[ctx.guild_id].get_profile(ctx.user)
        await profile.set_ataglance(ctx.interaction)

################################################################################
    @profiles.command(
        name="personality",
        description="View and edit Personality, Likes, Dislikes, and Bio."
    )
    async def profile_personality(self, ctx: ApplicationContext) -> None:

        profile = self.bot[ctx.guild_id].get_profile(ctx.user)
        await profile.set_personality(ctx.interaction)
        
################################################################################
    @profiles.command(
        name="images",
        description="View and edit Thumbnail, Main Image, and Additional Images."
    )
    async def profile_personality(self, ctx: ApplicationContext) -> None:

        profile = self.bot[ctx.guild_id].get_profile(ctx.user)
        await profile.set_images(ctx.interaction)

################################################################################
    @profiles.command(
        name="add_image",
        description="Add a Thumbnail, Main Image, or Additional Image to your profile."
    )
    async def profile_add_image(
        self,
        ctx: ApplicationContext,
        section: Option(
            name="field",
            description="Which profile field you want to set with the provided image.",
            choices=[
                OptionChoice(
                    name=ImageType.Thumbnail.proper_name,
                    value=str(ImageType.Thumbnail.value)  # type: ignore
                ),
                OptionChoice(
                    name=ImageType.MainImage.proper_name,
                    value=str(ImageType.MainImage.value)  # type: ignore
                ),
                OptionChoice(
                    name=ImageType.AdditionalImage.proper_name,
                    value=str(ImageType.AdditionalImage.value)  # type: ignore
                )
            ],
            required=True
        ),
        file: Option(
            SlashCommandOptionType.attachment,
            name="file",
            description="The image file to set in the specified field.",
            required=True
        )
    ):

        profile = self.bot[ctx.guild_id].get_profile(ctx.user)
        await profile.assign_image(ctx.interaction, ImageType(int(section)), file)

################################################################################
    @profiles.command(
        name="progress",
        description="A command to view a progress dialog for your profile."
    )
    async def profile_progress(self, ctx: ApplicationContext) -> None:

        profile = self.bot[ctx.guild_id].get_profile(ctx.user)
        await profile.progress(ctx.interaction)

################################################################################
    @profiles.command(
        name="finalize",
        description="Finalize and post/update your profile"
    )
    async def profile_finalize(
        self, 
        ctx: ApplicationContext,
        channel: Option(
            SlashCommandOptionType.channel,
            name="channel",
            description="The channel to post your profile in.",
            required=True
        )
    ) -> None:

        profile = self.bot[ctx.guild_id].get_profile(ctx.user)
        await profile.post(ctx.interaction, channel)

        return

################################################################################
def setup(bot: "TrainingBot") -> None:

    bot.add_cog(Profiles(bot))

################################################################################
