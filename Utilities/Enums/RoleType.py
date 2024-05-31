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
    # VenuePending = 7  # Don't need this, but keeping here, so I know why it's skipped
    VenueManagement = 8
    Trainee = 9
    TraineeHiatus = 10

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
        # elif self.value == 7:
        #     return "Venue Pending"
        elif self.value == 8:
            return "Venue Management"
        elif self.value == 10:
            return "Trainee Hiatus"

        return self.name.rstrip("Main")
    
################################################################################
    @staticmethod
    def select_options() -> List[SelectOption]:
        
        return [r.select_option for r in RoleType]
    
################################################################################
    