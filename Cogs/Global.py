from typing import TYPE_CHECKING

from discord import (
    ApplicationContext,
    Cog,
    slash_command,
    guild_only
)

from Classes.HelpMessage import HelpMessage

if TYPE_CHECKING:
    from Classes import StaffPartyBot
################################################################################
class GlobalCommands(Cog):

    def __init__(self, bot: "StaffPartyBot"):

        self.bot: "StaffPartyBot" = bot

################################################################################
    @slash_command(
        name="bg_check",
        description="Fill out the mandatory background check form."
    )
    @guild_only()
    async def start_bg_check(self, ctx: ApplicationContext) -> None:

        guild = self.bot[ctx.guild_id]
        await guild.training_manager.start_bg_check(ctx.interaction)

################################################################################
    @slash_command(
        name="help",
        description="Get help with using the bot."
    )
    @guild_only()
    async def help_menu(self, ctx: ApplicationContext) -> None:
        
        await HelpMessage(self.bot).menu(ctx.interaction)
        
################################################################################
    @slash_command(
        name="etiquette",
        description="Get the Venue Etiquette Guide."
    )
    @guild_only()
    async def venue_etiquette(self, ctx: ApplicationContext) -> None:

        guild = self.bot[ctx.guild_id]
        await guild.venue_manager.venue_etiquette(ctx.interaction)
        
################################################################################
def setup(bot: "StaffPartyBot") -> None:

    bot.add_cog(GlobalCommands(bot))

################################################################################
