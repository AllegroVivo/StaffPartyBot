# Can't use annotations if we're using slash command Options.
from typing import TYPE_CHECKING

from discord import (
    ApplicationContext,
    Cog,
    SlashCommandGroup,
    Option,
    SlashCommandOptionType
)

if TYPE_CHECKING:
    from Classes.Bot import TrainingBot
################################################################################
class Positions(Cog):

    def __init__(self, bot: "TrainingBot"):

        self.bot: "TrainingBot" = bot

################################################################################

    positions = SlashCommandGroup(
        name="positions",
        description="Commands for trainer management."
    )

################################################################################
    @positions.command(
        name="add",
        description="Add a new position to the database."
    )
    async def add_position(
        self,
        ctx: ApplicationContext,
        name: Option(
            type=SlashCommandOptionType.string,
            name="name",
            description="The name of the position to add.",
            required=True
        )
    ) -> None:
        
        guild = self.bot[ctx.guild_id]
        await guild.position_manager.add_position(ctx.interaction, name)

################################################################################
    @positions.command(
        name="status",
        description="View and edit the status of a given job position."
    )
    async def position_status(
        self,
        ctx: ApplicationContext,
        name: Option(
            type=SlashCommandOptionType.string,
            name="position",
            description="The position to view.",
            required=True
        )
    ) -> None:

        guild = self.bot[ctx.guild_id]
        await guild.position_manager.position_status(ctx.interaction, name)
        
################################################################################
    @positions.command(
        name="global_reqs",
        description="View and edit the global requirements for all positions."
    )
    async def global_requirements(self, ctx: ApplicationContext) -> None:

        guild = self.bot[ctx.guild_id]
        await guild.position_manager.global_requirements_menu(ctx.interaction)

################################################################################
def setup(bot: "TrainingBot") -> None:

    bot.add_cog(Positions(bot))

################################################################################
