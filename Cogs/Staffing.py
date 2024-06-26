from typing import TYPE_CHECKING

from discord import (
    ApplicationContext,
    Cog,
    SlashCommandGroup,
    Option,
    OptionChoice,
    SlashCommandOptionType,
    guild_only,
)

from Utilities import ImageType

if TYPE_CHECKING:
    from Classes import StaffPartyBot
################################################################################
class Profiles(Cog):

    def __init__(self, bot: "StaffPartyBot"):

        self.bot: "StaffPartyBot" = bot

################################################################################

    staffing = SlashCommandGroup(
        name="staffing",
        description="Commands for staffing sign-up and management.",
        guild_only=True
    )

################################################################################
    @staffing.command(
        name="add_profile_image",
        description="Add a Thumbnail, Main Image, or Additional Image to your staff profile."
    )
    @guild_only()
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

        profile = self.bot[ctx.guild_id].get_or_create_profile(ctx.user)
        await profile.assign_image(ctx.interaction, ImageType(int(section)), file)

################################################################################
    @staffing.command(
        name="profile",
        description="View and edit your staff profile."
    )
    @guild_only()
    async def profile_menu(self, ctx: ApplicationContext):

        profile = self.bot[ctx.guild_id].get_or_create_profile(ctx.user)
        await profile.main_menu(ctx.interaction)
        
################################################################################
def setup(bot: "StaffPartyBot") -> None:

    bot.add_cog(Profiles(bot))

################################################################################
