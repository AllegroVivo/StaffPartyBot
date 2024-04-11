from typing import TYPE_CHECKING

from discord import (
    ApplicationContext,
    Cog,
    SlashCommandGroup,
    Option,
    SlashCommandOptionType,
    OptionChoice,
    guild_only,
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
        description="Commands for venue- and internship-related tasks and queries.",
        guild_only=True
    )

################################################################################
    @venues.command(
        name="profile",
        description="View and edit your venue's internship profile & status."
    )
    @guild_only()
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
        name="signup",
        description="Sign up a new venue for the internship program."
    )
    @guild_only()
    async def signup_venue(
        self,
        ctx: ApplicationContext,
        name: Option(
            SlashCommandOptionType.string,
            name="name",
            description="The name of the new venue.",
            required=True
        ),
        user1: Option(
            SlashCommandOptionType.user,
            name="manager_2",
            description="An alternate user that can make edits to the venue listing.",
            required=False
        ),
        user2: Option(
            SlashCommandOptionType.user,
            name="manager_3",
            description="An alternate user that can make edits to the venue listing.",
            required=False
        ),
        user3: Option(
            SlashCommandOptionType.user,
            name="manager_4",
            description="An alternate user that can make edits to the venue listing.",
            required=False
        )
    ) -> None:

        guild = self.bot[ctx.guild_id]
        await guild.venue_manager.signup(ctx.interaction, name, user1, user2, user3)
        
################################################################################
    @venues.command(
        name="add_user",
        description="Add and Owner or Authorized User to a venue listing."
    )
    @guild_only()
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
        )
    ) -> None:

        guild = self.bot[ctx.guild_id]
        await guild.venue_manager.add_user(ctx.interaction, venue, user)
        
################################################################################
    @venues.command(
        name="import",
        description="Import a venue from the FFXIV Venues API."
    )
    @guild_only()
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
    @venues.command(
        name="toggle_user_mute",
        description="Toggle whether a user will hear about a venue's job postings."
    )
    @guild_only()
    async def venue_toggle_user_mute(
        self,
        ctx: ApplicationContext,
        name: Option(
            SlashCommandOptionType.string,
            name="venue_name",
            description="The name of the venue to mute the user for.",
            required=True
        ),
        user: Option(
            SlashCommandOptionType.user,
            name="user",
            description="The user to un/mute.",
            required=True
        )
    ) -> None:

        guild = self.bot[ctx.guild_id]
        await guild.venue_manager.toggle_user_mute(ctx.interaction, name, user)
        
################################################################################  
def setup(bot: "TrainingBot") -> None:

    bot.add_cog(Venues(bot))

################################################################################
