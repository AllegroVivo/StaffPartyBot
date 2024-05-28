from __future__ import annotations

from discord import Cog
from typing import TYPE_CHECKING
from discord.ext import tasks

if TYPE_CHECKING:
    from Classes import StaffPartyBot
################################################################################
class Internal(Cog):

    def __init__(self, bot: StaffPartyBot):

        self.bot: StaffPartyBot = bot

################################################################################
    @Cog.listener("on_ready")
    async def load_internals(self) -> None:

        print("Loading internals...")
        await self.bot.load_all()

        print("Starting tasks...")
        self.cull_job_postings.start()
        # self.training_reminder.start()
        
        print("TrainingBot Online!")

################################################################################
    @Cog.listener("on_guild_join")
    async def on_guild_join(self, guild) -> None:

        self.bot.guild_manager.add_guild(guild)

################################################################################
    @Cog.listener("on_member_join")
    async def on_member_join(self, member) -> None:
        
        await self.bot[member.guild.id].on_member_join(member)
        
################################################################################
    @Cog.listener("on_member_remove")
    async def on_member_remove(self, member) -> None:

        await self.bot[member.guild.id].on_member_leave(member)
        
################################################################################
    @tasks.loop(minutes=30)
    async def cull_job_postings(self) -> None:

        for f in self.bot.guild_manager.fguilds:
            await f.jobs_manager.cull_job_postings()
        
################################################################################
    @tasks.loop(minutes=5)
    async def training_reminder(self) -> None:

        for frogge in self.bot.guild_manager.fguilds:
            for group in frogge.training_manager.groups:
                await group.reminder()    
            
################################################################################
def setup(bot: StaffPartyBot) -> None:

    bot.add_cog(Internal(bot))

################################################################################
