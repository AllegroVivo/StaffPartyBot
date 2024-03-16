from typing import TYPE_CHECKING

from discord import (
    ApplicationContext,
    Cog,
    SlashCommandGroup,
    Option,
    SlashCommandOptionType
)

if TYPE_CHECKING:
    from Classes import TrainingBot
################################################################################
class Venues(Cog):

    def __init__(self, bot: "TrainingBot"):

        self.bot: "TrainingBot" = bot

################################################################################

    venues = SlashCommandGroup(
        name="venue",
        description="Commands for venue- and internship-related tasks and queries."
    )

################################################################################
    @venues.command(
        name="profile",
        description="View and edit your venue's internship profile & status."
    )
    async def venue_profile(
        self,
        ctx: ApplicationContext,
        name: Option(
            SlashCommandOptionType.string,
            name="name",
            description="The name of the venue.",
            required=True
        )
    ) -> None:

        guild = self.bot[ctx.guild_id]
        await guild.venue_manager.venue_menu(ctx.interaction, name)

################################################################################
    @venues.command(
        name="post",
        description="Post or update your venue internship profile."
    )
    async def post_venue(
        self,
        ctx: ApplicationContext,
        name: Option(
            SlashCommandOptionType.string,
            name="name",
            description="The name of the venue.",
            required=True
        )
    ) -> None:

        guild = self.bot[ctx.guild_id]
        await guild.venue_manager.post_venue(ctx.interaction, name)
        
################################################################################  
def setup(bot: "TrainingBot") -> None:

    bot.add_cog(Venues(bot))

################################################################################
