from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Optional

from .Branch import DBWorkerBranch

if TYPE_CHECKING:
    from Classes import Position, Trainer, Trainee, Qualification, Training, TUser, SignUpMessage, Job
    from Utils import RequirementLevel
################################################################################

__all__ = ("DatabaseUpdater",)

################################################################################
class DatabaseUpdater(DBWorkerBranch):
    """A utility class for updating records in the database."""

    def update_log_channel(self, guild_id: int, channel_id: Optional[int]) -> None:
        
        self.execute(
            "UPDATE bot_config SET log_channel = %s WHERE guild_id = %s;",
            channel_id, guild_id
        )
        
################################################################################
    
    log_channel     = update_log_channel
    
################################################################################
    