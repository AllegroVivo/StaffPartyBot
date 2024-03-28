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
class JobPostings(Cog):

    def __init__(self, bot: "TrainingBot"):

        self.bot: "TrainingBot" = bot

################################################################################

    jobs = SlashCommandGroup(
        name="jobs",
        description="Commands for job classified-related tasks and queries."
    )

################################################################################
    @jobs.command(
        name="create_post",
        description="Create a new job classified posting."
    )
    async def jobs_create_post(
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
        await guild.jobs_manager.create_new(ctx.interaction, venue)

################################################################################
    @jobs.command(
        name="post_status",
        description="Check or modify the status of a job classified posting."
    )
    async def jobs_post_status(
        self,
        ctx: ApplicationContext,
        post_id: Option(
            SlashCommandOptionType.string,
            name="post_id",
            description="The ID of the job posting to check or modify.",
            required=True
        )
    ) -> None:

        guild = self.bot[ctx.guild_id]
        await guild.jobs_manager.check_status(ctx.interaction, post_id)
        
################################################################################
def setup(bot: "TrainingBot") -> None:

    bot.add_cog(JobPostings(bot))

################################################################################
