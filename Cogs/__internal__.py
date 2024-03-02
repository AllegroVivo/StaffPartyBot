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
def setup(bot: TrainingBot) -> None:

    bot.add_cog(Internal(bot))

################################################################################
