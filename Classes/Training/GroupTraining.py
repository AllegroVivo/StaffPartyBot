from __future__ import annotations

from datetime import datetime

from typing import TYPE_CHECKING, Optional, List, Any, Tuple, Type, TypeVar, Dict

from Classes.Training.GroupTrainingSignup import GroupTrainingSignup

if TYPE_CHECKING:
    from Classes import TrainingManager, Position
################################################################################

__all__ = ("GroupTraining",)

SE = TypeVar("SE", bound="ScheduledEvent")

################################################################################
class GroupTraining:
    
    __slots__ = (
        "_mgr",
        "_id",
        "_name",
        "_description",
        "_start",
        "_end",
        "_position",
        "_signups",
    )
    
################################################################################
    def __init__(self, mgr: TrainingManager, _id: str, **kwargs):
        
        self._id: str = _id
        self._mgr: TrainingManager = mgr
        
        self._name: Optional[str] = kwargs.get("name")
        self._description: Optional[str] = kwargs.get("description")
        self._position: Optional[Position] = kwargs.get("position")
        
        self._start: Optional[datetime] = kwargs.get("start_time")
        self._end: Optional[datetime] = kwargs.get("end_time")
        
        self._signups: List[GroupTrainingSignup] = []
    
################################################################################
    @classmethod
    async def load(cls: Type[SE], mgr: TrainingManager, data: Dict[str, Any]) -> SE:
        
        return cls(
            mgr=mgr,
            _id=data["training"][0],
            name=data["training"][2],
            description=data["training"][3],
            start_time=data["training"][4],
            end_time=data["training"][5],
            position=(
                mgr.guild.position_manager.get_position(data["training"][6])
                if data["training"][6] else None
            )
        )
    
################################################################################
    