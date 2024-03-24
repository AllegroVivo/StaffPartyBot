from typing import List

from discord import SelectOption

from ._Enum import FroggeEnum
################################################################################
class RateType(FroggeEnum):

    PerHour = 1
    PerShift = 2
    PerRep = 3
    PerNight = 4
    Once = 5

################################################################################
    @property
    def proper_name(self) -> str:

        if self.value == 1:
            return "Per Hour"
        elif self.value == 2:
            return "Per Shift"
        elif self.value == 3:
            return "Per Repetition"
        elif self.value == 4:
            return "Per Night"

        return self.name
    
################################################################################
    @staticmethod
    def select_options() -> List[SelectOption]:
        
        return [r.select_option for r in RateType]
    
################################################################################
    