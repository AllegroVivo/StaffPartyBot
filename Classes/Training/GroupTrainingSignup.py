from __future__ import annotations

from datetime import datetime
from discord import Interaction, Embed, EmbedField

from typing import TYPE_CHECKING, Optional, List

if TYPE_CHECKING:
    from Classes import ScheduleManager
################################################################################

__all__ = ("GroupTrainingSignup",)

################################################################################
class GroupTrainingSignup:
    
    __slots__ = (
        "_parent",
        "_id",
        "_user",
        "_level"
    )
    
################################################################################
    def __init__(self, mgr: ScheduleManager, _id: str, **kwargs):
        
        pass
    
################################################################################
    