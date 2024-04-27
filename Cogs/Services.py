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
class Services(Cog):

    def __init__(self, bot: "StaffPartyBot"):

        self.bot: "StaffPartyBot" = bot

################################################################################

    services = SlashCommandGroup(
        name="services",
        description="Commands for service-related tasks and data.",
        guild_only=True,
        guild_ids=[303742308874977280]
    )

################################################################################
    @services.command(
        name="add",
        description="Add a new type of hireable service to the server."
    )
    async def add_service(
        self, 
        ctx: ApplicationContext,
        name: Option(
            SlashCommandOptionType.string,
            name="name",
            description="The name of the service to add.",
            required=True
        )
    ) -> None:

        guild = self.bot[ctx.guild_id]
        await guild.service_manager.add_service(ctx.interaction, name)
    
################################################################################
    @services.command(
        name="status",
        description="Check or edit the status of a hireable service."
    )
    async def service_status(
        self, 
        ctx: ApplicationContext,
        name: Option(
            SlashCommandOptionType.string,
            name="name",
            description="The name of the service to check.",
            required=True
        )
    ) -> None:

        guild = self.bot[ctx.guild_id]
        await guild.service_manager.service_status(ctx.interaction, name)
        
################################################################################
def setup(bot: "StaffPartyBot") -> None:

    bot.add_cog(Services(bot))

################################################################################
