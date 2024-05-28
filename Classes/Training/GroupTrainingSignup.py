from __future__ import annotations

from typing import TYPE_CHECKING, Type, TypeVar

from Utilities import SignupLevel

if TYPE_CHECKING:
    from Classes import TUser, GroupTraining
################################################################################

__all__ = ("GroupTrainingSignup",)

GTS = TypeVar("GTS", bound="GroupTrainingSignup")

################################################################################
class GroupTrainingSignup:
    
    __slots__ = (
        "_parent",
        "_id",
        "_user",
        "_level"
    )
    
################################################################################
    def __init__(self, parent: GroupTraining, _id: str, user: TUser, level: SignupLevel) -> None:
        
        self._parent: GroupTraining = parent
        
        self._id: str = _id
        self._user: TUser = user
        self._level: SignupLevel = level
    
################################################################################
    @classmethod
    def new(cls: Type[GTS], parent: GroupTraining, user: TUser, level: SignupLevel) -> GTS:
        
        new_id = parent.bot.database.insert.group_training_signup(parent.id, user.user_id, level.value)
        return cls(parent, new_id, user, level)
    
################################################################################
    @property
    def id(self) -> str:
        
        return self._id
    
################################################################################
    @property
    def user(self) -> TUser:
        
        return self._user
    
################################################################################
    @property
    def level(self) -> SignupLevel:
        
        return self._level
    
    @level.setter
    def level(self, value: SignupLevel) -> None:
        
        self._level = value
        self.update()
        
################################################################################
    def delete(self) -> None:
        
        self._parent.bot.database.delete.group_training_signup(self)
        self._parent.signups.remove(self)
        
################################################################################
    def update(self) -> None:
        
        self._parent.bot.database.update.group_training_signup(self)
        
################################################################################
