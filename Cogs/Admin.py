from discord import (
    ApplicationContext,
    Cog,
    SlashCommandGroup,
    Option,
    SlashCommandOptionType,
    OptionChoice
)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Classes.Bot import TrainingBot
################################################################################
class Admin(Cog):

    def __init__(self, bot: "TrainingBot"):

        self.bot: "TrainingBot" = bot

################################################################################

    admin = SlashCommandGroup(
        name="admin",
        description="Administrator commands for user/system configuration & management."
    )

################################################################################
    @admin.command(
        name="user_status",
        description="View and edit the trainer/trainee profile & status of a user."
    )
    async def user_status(
        self,
        ctx: ApplicationContext,
        user: Option(
            SlashCommandOptionType.user,
            name="user",
            description="The user whose trainer record to view.",
            required=True
        )
    ) -> None:

        guild = self.bot[ctx.guild_id]
        await guild.training_manager.tuser_admin_status(ctx.interaction, user)
        
################################################################################
    @admin.command(
        name="post_signup",
        description="Post the trainer signup message."
    )
    async def post_signup_message(
        self,
        ctx: ApplicationContext,
        channel: Option(
            SlashCommandOptionType.channel,
            name="channel",
            description="The channel to set as the trainer signup message channel.",
            required=True
        )
    ) -> None:

        guild = self.bot[ctx.guild_id]
        await guild.training_manager.post_signup_message(ctx.interaction, channel)

################################################################################
    @admin.command(
        name="log_channel",
        description="Set the channel for bot logs.",
    )
    async def set_log_channel(
        self,
        ctx: ApplicationContext,
        channel: Option(
            SlashCommandOptionType.channel,
            name="channel",
            description="The channel to set as the log channel.",
            required=True
        )
    ) -> None:

        await self.bot[ctx.guild_id].log.set_log_channel(ctx.interaction, channel)

################################################################################
    @admin.command(
        name="venue_channel",
        description="Set the channel for venue postings.",
    )
    async def set_venue_channel(
        self,
        ctx: ApplicationContext,
        channel: Option(
            SlashCommandOptionType.channel,
            name="channel",
            description="The channel to set as the venue channel.",
            required=True
        )
    ) -> None:

        guild = self.bot[ctx.guild_id]
        await guild.venue_manager.set_venue_channel(ctx.interaction, channel)

################################################################################
    @admin.command( 
        name="jobs_channel",
        description="Set the channel for job postings."
    )
    async def set_jobs_channel(
        self,
        ctx: ApplicationContext,
        channel: Option(
            SlashCommandOptionType.channel,
            name="channel",
            description="The channel to set as the jobs channel.",
            required=True
        ),
        post_type: Option(
            SlashCommandOptionType.string,
            name="post_type",
            description="The type of job posting to set the channel for.",
            required=True,
            choices=[
                OptionChoice(name="Temporary", value="1"),
                OptionChoice(name="Permanent", value="2")
            ]
        )
    ) -> None:

        guild = self.bot[ctx.guild_id]
        await guild.job_posting_manager.set_jobs_channel(ctx.interaction, channel, int(post_type))
        
################################################################################
    @admin.command(
        name="add_venue",
        description="Add a new venue to the system."
    )
    async def add_venue(
        self,
        ctx: ApplicationContext,
        name: Option(
            SlashCommandOptionType.string,
            name="name",
            description="The name of the venue.",
            required=True
        ),
        user: Option(
            SlashCommandOptionType.user,
            name="user",
            description="The initial user to add to the venue's authorized user list.",
            required=True
        )
    ) -> None:

        guild = self.bot[ctx.guild_id]
        await guild.venue_manager.add_venue(ctx.interaction, name, user)
        
################################################################################
    @admin.command(
        name="add_venue_user",
        description="Add a user as a venue's owner or authorized user."
    )
    async def add_venue_user(
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
        await guild.venue_manager.add_user(ctx.interaction, venue, user, _type, True)
        
################################################################################
    @admin.command(
        name="remove_venue_user",
        description="Remove a user as a venue's owner or authorized user."
    )
    async def remove_venue_user(
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
            description="The user to remove from the venue's authorized user list.",
            required=True
        )
    ) -> None:

        guild = self.bot[ctx.guild_id]
        await guild.venue_manager.remove_user(ctx.interaction, venue, user)
        
################################################################################
    @admin.command(
        name="venue_profile",
        description="View and edit a venue's internship profile & status."
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
        await guild.venue_manager.venue_menu(ctx.interaction, name, admin=True)
        
################################################################################
    @admin.command(
        name="yeet_venue",
        description="Remove a venue from the system."
    )
    async def yeet_venue(
        self,
        ctx: ApplicationContext,
        name: Option(
            SlashCommandOptionType.string,
            name="name",
            description="The name of the venue to remove.",
            required=True
        )
    ) -> None:

        guild = self.bot[ctx.guild_id]
        await guild.venue_manager.remove_venue(ctx.interaction, name)
        
################################################################################
    @admin.command(
        name="reports",
        description="Generate reports for various system data."
    )
    async def report_menu(self, ctx: ApplicationContext) -> None:

        await self.bot[ctx.guild_id].report_menu(ctx.interaction)
        
################################################################################
    @admin.command(
        name="test",
    )
    async def test(self, ctx: ApplicationContext) -> None:

        await self.bot.veni_client.get_venues_by_manager(120065261037420544)
        
################################################################################        
def setup(bot: "TrainingBot") -> None:

    bot.add_cog(Admin(bot))

################################################################################
