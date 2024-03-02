from discord import (
    ApplicationContext,
    Cog,
    SlashCommandGroup,
    Option,
    SlashCommandOptionType
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
        name="set_log_channel",
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
def setup(bot: "TrainingBot") -> None:

    bot.add_cog(Admin(bot))

################################################################################
