from __future__ import annotations

from discord import Cog
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Classes import TrainingBot
################################################################################
class Internal(Cog):

    def __init__(self, bot: TrainingBot):

        self.bot: TrainingBot = bot

################################################################################
    @Cog.listener("on_ready")
    async def load_internals(self) -> None:

        print("Loading internals...")
        await self.bot.load_all()
        
        print("TrainingBot Online!")

################################################################################
    @Cog.listener("on_guild_join")
    async def on_guild_join(self, guild) -> None:

        self.bot.fguilds.add_guild(guild)

################################################################################
    @Cog.listener("on_member_join")
    async def on_member_join(self, member) -> None:
        
        await self.bot[member.guild.id].log.member_join(member)
        
################################################################################
    @Cog.listener("on_member_remove")
    async def on_member_remove(self, member) -> None:

        await self.bot[member.guild.id].log.member_left(member)
        
################################################################################
def setup(bot: TrainingBot) -> None:

    bot.add_cog(Internal(bot))

################################################################################
