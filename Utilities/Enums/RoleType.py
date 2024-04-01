from typing import List

from discord import SelectOption

from ._Enum import FroggeEnum
################################################################################
class RoleType(FroggeEnum):

    Hiatus = 1
    Trainer = 2
    TrainerPending = 3
    Staff = 4
    StaffNotValidated = 5
    NewStaff = 6

################################################################################
    @property
    def proper_name(self) -> str:

        if self.value == 3:
            return "Trainer Pending"
        elif self.value == 5:
            return "Staff Not Validated"
        elif self.value == 6:
            return "New Staff"

        return self.name
    
################################################################################
    @staticmethod
    def select_options() -> List[SelectOption]:
        
        return [r.select_option for r in RoleType]
    
################################################################################
    