from typing import TYPE_CHECKING

from discord import (
    ApplicationContext,
    Cog,
    SlashCommandGroup,
    Option,
    SlashCommandOptionType,
    OptionChoice
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
    @venues.command(
        name="add_user",
        description="Add and Owner or Authorized User to a venue listing."
    )
    async def venue_add_user(
        self,
        ctx: ApplicationContext,
        venue: Option(
            SlashCommandOptionType.string,
            name="venue",
            description="The name of the venue.",
            required=True
        ),
        user: Option(
            SlashCommandOptionType.user,
            name="user",
            description="The user to add to the venue's authorized user list.",
            required=True
        ),
        _type: Option(
            SlashCommandOptionType.string,
            name="user_type",
            description="The user type to assign the user as.",
            required=True,
            choices=[
                OptionChoice(name="Owner", value="Owner"),
                OptionChoice(name="Authorized User", value="AuthUser")
            ]
        )
    ) -> None:

        guild = self.bot[ctx.guild_id]
        await guild.venue_manager.add_user(ctx.interaction, venue, user, _type)
        
################################################################################
    @venues.command(
        name="import",
        description="Import a venue from the XIV Venues API."
    )
    async def venue_import(
        self,
        ctx: ApplicationContext,
        name: Option(
            SlashCommandOptionType.string,
            name="name",
            description="The name of the venue to import.",
            required=True
        )
    ) -> None:

        guild = self.bot[ctx.guild_id]
        await guild.venue_manager.import_venue(ctx.interaction, name)
        
################################################################################  
def setup(bot: "TrainingBot") -> None:

    bot.add_cog(Venues(bot))

################################################################################
