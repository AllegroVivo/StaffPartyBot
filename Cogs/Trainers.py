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
    from Classes import StaffPartyBot
################################################################################
class Trainers(Cog):

    def __init__(self, bot: "StaffPartyBot"):

        self.bot: "StaffPartyBot" = bot

################################################################################

    trainer = SlashCommandGroup(
        name="trainer",
        description="Commands for trainer-related tasks and data.",
        guild_only=True
    )

################################################################################
    @trainer.command(
        name="dashboard",
        description="Update training requirements for your trainees."
    )
    async def trainer_dashboard(self, ctx: ApplicationContext) -> None:

        guild = self.bot[ctx.guild_id]
        await guild.training_manager.trainer_dashboard(ctx.interaction)

################################################################################
    @trainer.command(
        name="profile",
        description="View and edit your training registration profile & status."
    )
    async def training_profile(self, ctx: ApplicationContext) -> None:

        guild = self.bot[ctx.guild_id]
        await guild.training_manager.tuser_status(ctx.interaction)

################################################################################
    @trainer.command(
        name="position_info",
        description="View information about a specific training position."
    )
    async def register_trainer(self, ctx: ApplicationContext) -> None:

        guild = self.bot[ctx.guild_id]
        await guild.position_manager.trainer_pos_report(ctx.interaction)
        
################################################################################
    @trainer.command(
        name="trainee_profile",
        description="View a trainee's profile and training status."
    )
    async def register_trainer(
        self, 
        ctx: ApplicationContext,
        user: Option(
            SlashCommandOptionType.user,
            name="user",
            description="The user whose profile to view.",
            required=False
        )
    ) -> None:

        guild = self.bot[ctx.guild_id]
        await guild.training_manager.trainee_profile(ctx.interaction, user or None)
        
################################################################################
    @trainer.command(
        name="group_training",
        description="Create and manage Group Training events."
    )
    async def group_training(self, ctx: ApplicationContext) -> None:

        guild = self.bot[ctx.guild_id]
        await guild.training_manager.group_training_menu(ctx.interaction)
        
################################################################################
    @trainer.command(
        name="acquire_trainee",
        description="Pick up all trainings for a specific trainee."
    )
    async def acquire_trainee(
        self, 
        ctx: ApplicationContext,
        user: Option(
            SlashCommandOptionType.user,
            name="user",
            description="The trainee to acquire.",
            required=True
        )
    ) -> None:

        guild = self.bot[ctx.guild_id]
        await guild.training_manager.acquire_trainee(ctx.interaction, user)
        
################################################################################
def setup(bot: "StaffPartyBot") -> None:

    bot.add_cog(Trainers(bot))

################################################################################
