from typing import TYPE_CHECKING

from discord import (
    ApplicationContext,
    Cog,
    SlashCommandGroup,
    SlashCommandOptionType,
    Option,
    guild_only,
)

if TYPE_CHECKING:
    from Classes import TrainingBot
################################################################################
class Trainers(Cog):

    def __init__(self, bot: "TrainingBot"):

        self.bot: "TrainingBot" = bot

################################################################################

    trainer = SlashCommandGroup(
        name="trainer",
        description="Commands for trainer-related tasks and data."
    )

################################################################################
    @trainer.command(
        name="dashboard",
        description="Update training requirements for your trainees."
    )
    @guild_only()
    async def trainer_dashboard(self, ctx: ApplicationContext) -> None:

        guild = self.bot[ctx.guild_id]
        await guild.training_manager.trainer_dashboard(ctx.interaction)

################################################################################
    @trainer.command(
        name="profile",
        description="View and edit your training registration profile & status."
    )
    @guild_only()
    async def training_profile(self, ctx: ApplicationContext) -> None:

        guild = self.bot[ctx.guild_id]
        await guild.training_manager.tuser_status(ctx.interaction)

################################################################################
    @trainer.command(
        name="position_info",
        description="View information about a specific training position."
    )
    @guild_only()
    async def register_trainer(self, ctx: ApplicationContext) -> None:

        guild = self.bot[ctx.guild_id]
        await guild.position_manager.trainer_pos_report(ctx.interaction)
        
################################################################################
    @trainer.command(
        name="trainee_profile",
        description="View a trainee's profile and training status."
    )
    @guild_only()
    async def register_trainer(
        self, 
        ctx: ApplicationContext,
        user: Option(
            SlashCommandOptionType.user,
            name="user",
            description="The user whose profile to view.",
            required=True
        )
    ) -> None:

        guild = self.bot[ctx.guild_id]
        await guild.training_manager.trainee_profile(ctx.interaction, user)
        
################################################################################
def setup(bot: "TrainingBot") -> None:

    bot.add_cog(Trainers(bot))

################################################################################
