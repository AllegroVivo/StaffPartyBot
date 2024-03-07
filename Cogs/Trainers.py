from typing import TYPE_CHECKING

from discord import (
    ApplicationContext,
    Cog,
    SlashCommandGroup
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
    async def trainer_dashboard(self, ctx: ApplicationContext) -> None:

        guild = self.bot[ctx.guild_id]
        await guild.training_manager.trainer_dashboard(ctx.interaction)

################################################################################  
def setup(bot: "TrainingBot") -> None:

    bot.add_cog(Trainers(bot))

################################################################################
