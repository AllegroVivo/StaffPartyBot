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
    @venues.command(
        name="signup",
        description="Sign up a new venue for the internship program."
    )
    async def signup_venue(
        self,
        ctx: ApplicationContext,
        name: Option(
            SlashCommandOptionType.string,
            name="name",
            description="The name of the new venue.",
            required=True
        ),
        owner2: Option(
            SlashCommandOptionType.user,
            name="alt_owner",
            description="A alternate user to register as owner of the venue.",
            required=False
        ),
        user1: Option(
            SlashCommandOptionType.user,
            name="auth_user_1",
            description="An alternate user that can make edits to the venue listing.",
            required=False
        ),
        user2: Option(
            SlashCommandOptionType.user,
            name="auth_user_2",
            description="An alternate user that can make edits to the venue listing.",
            required=False
        ),
        user3: Option(
            SlashCommandOptionType.user,
            name="auth_user_3",
            description="An alternate user that can make edits to the venue listing.",
            required=False
        )
    ) -> None:

        guild = self.bot[ctx.guild_id]
        await guild.venue_manager.signup(
            ctx.interaction, name, owner2, user1, user2, user3
        )
        
################################################################################  
def setup(bot: "TrainingBot") -> None:

    bot.add_cog(Venues(bot))

################################################################################
