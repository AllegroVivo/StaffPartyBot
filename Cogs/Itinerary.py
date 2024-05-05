from typing import TYPE_CHECKING

from discord import (
    ApplicationContext,
    Cog,
    SlashCommandGroup,
    SlashCommandOptionType,
    OptionChoice,
    Option,
)

if TYPE_CHECKING:
    from Classes import StaffPartyBot
################################################################################
class Itinerary(Cog):

    def __init__(self, bot: "StaffPartyBot"):

        self.bot: "StaffPartyBot" = bot

################################################################################

    itinerary = SlashCommandGroup(
        name="itinerary",
        description="Commands for itinerary-related tasks and data.",
        guild_only=True
    )

################################################################################
    @itinerary.command(
        name="compile",
        description="Create a new current itinerary and export to excel.",
    )
    async def compile_itinerary(
        self, 
        ctx: ApplicationContext,
        region: Option(
            SlashCommandOptionType.string,
            name="region",
            description="The datacenter to compile the itinerary for.",
            required=False,
            options=[
                OptionChoice(name="North America", value="NA"),
                OptionChoice(name="Europe", value="EU"),
                OptionChoice(name="Oceanan", value="OC"),
                OptionChoice(name="Japan", value="JP"),
            ]
        )
    ) -> None:

        guild = self.bot[ctx.guild_id]
        await guild.itinerary_manager.compile_itinerary(ctx.interaction, region or None)
        
################################################################################
def setup(bot: "StaffPartyBot") -> None:

    bot.add_cog(Itinerary(bot))

################################################################################
