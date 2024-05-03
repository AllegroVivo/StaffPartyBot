from typing import List

from discord import SelectOption

from ._Enum import FroggeEnum
################################################################################
class RoleType(FroggeEnum):

    TrainerMain = 1
    TrainerPending = 2
    TrainingHiatus = 3
    StaffMain = 4
    StaffNotValidated = 5
    NewStaff = 6
    VenuePending = 7
    VenueManagement = 8

################################################################################
    @property
    def proper_name(self) -> str:

        if self.value == 2:
            return "Trainer Pending"
        elif self.value == 3:
            return "Training Hiatus"
        elif self.value == 5:
            return "Staff Not Validated"
        elif self.value == 6:
            return "New Staff"
        elif self.value == 7:
            return "Venue Pending"
        elif self.value == 8:
            return "Venue Management"

        return self.name.rstrip("Main")
    
################################################################################
    @staticmethod
    def select_options() -> List[SelectOption]:
        
        return [r.select_option for r in RoleType]
    
################################################################################
    