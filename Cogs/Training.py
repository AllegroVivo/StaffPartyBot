from typing import TYPE_CHECKING

from discord import (
    ApplicationContext,
    Cog,
    SlashCommandGroup
)

if TYPE_CHECKING:
    from Classes import TrainingBot
################################################################################
class Training(Cog):

    def __init__(self, bot: "TrainingBot"):

        self.bot: "TrainingBot" = bot

################################################################################

    training = SlashCommandGroup(
        name="training",
        description="Commands for training-related tasks and queries."
    )

################################################################################
    @training.command(
        name="profile",
        description="View and edit your training registration profile & status."
    )
    async def training_profile(self, ctx: ApplicationContext) -> None:

        guild = self.bot[ctx.guild_id]
        await guild.training_manager.tuser_status(ctx.interaction)

################################################################################  
def setup(bot: "TrainingBot") -> None:

    bot.add_cog(Training(bot))

################################################################################
