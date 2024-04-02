from typing import List

from discord import SelectOption

from ._Enum import FroggeEnum
################################################################################
class RoleType(FroggeEnum):

    TrainerMain = 1
    TrainerPending = 2
    TrainerHiatus = 3
    StaffMain = 4
    StaffNotValidated = 5
    NewStaff = 6

################################################################################
    @property
    def proper_name(self) -> str:

        if self.value == 2:
            return "Trainer Pending"
        elif self.value == 5:
            return "Staff Not Validated"
        elif self.value == 6:
            return "New Staff"

        return self.name.rstrip("Main")
    
################################################################################
    @staticmethod
    def select_options() -> List[SelectOption]:
        
        return [r.select_option for r in RoleType]
    
################################################################################
    