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
class Classifieds(Cog):

    def __init__(self, bot: "TrainingBot"):

        self.bot: "TrainingBot" = bot

################################################################################

    jobs = SlashCommandGroup(
        name="jobs",
        description="Commands for job classified-related tasks and queries."
    )

################################################################################
    @jobs.command(
        name="post",
        description="Post a new job classified."
    )
    async def jobs_post(
        self,
        ctx: ApplicationContext,
        venue: Option(
            SlashCommandOptionType.string,
            name="venue",
            description="The venue for which the job is being posted.",
            required=True
        )
    ) -> None:

        guild = self.bot[ctx.guild_id]
        await guild.classified_manager.post_new(ctx.interaction, venue)

################################################################################
def setup(bot: "TrainingBot") -> None:

    bot.add_cog(Classifieds(bot))

################################################################################
