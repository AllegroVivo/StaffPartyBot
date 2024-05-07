from typing import TYPE_CHECKING

from discord import (
    ApplicationContext,
    Cog,
    SlashCommandGroup,
    guild_only
)

if TYPE_CHECKING:
    from Classes import StaffPartyBot
################################################################################
class Training(Cog):

    def __init__(self, bot: "StaffPartyBot"):

        self.bot: "StaffPartyBot" = bot

################################################################################

    trainees = SlashCommandGroup(
        name="trainee",
        description="Commands for trainee-related tasks and queries.",
        guild_only=True
    )

################################################################################
    @trainees.command(
        name="profile",
        description="View and edit your training registration profile & status."
    )
    @guild_only()
    async def training_profile(self, ctx: ApplicationContext) -> None:

        guild = self.bot[ctx.guild_id]
        await guild.training_manager.trainee_status(ctx.interaction)

################################################################################
    @trainees.command(
        name="match",
        description="Match yourself post-training to a venue for internship."
    )
    @guild_only()
    async def training_match(self, ctx: ApplicationContext) -> None:

        guild = self.bot[ctx.guild_id]
        await guild.training_manager.match(ctx.interaction)
        
################################################################################  
    @trainees.command(
        name="position_info",
        description="View information about a specific venue position."
    )
    async def trainee_position_info(self, ctx: ApplicationContext) -> None:

        guild = self.bot[ctx.guild_id]
        await guild.position_manager.trainee_pos_report(ctx.interaction)

################################################################################
def setup(bot: "StaffPartyBot") -> None:

    bot.add_cog(Training(bot))

################################################################################
