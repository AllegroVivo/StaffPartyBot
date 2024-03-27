from typing import List

from discord import SelectOption

from ._Enum import FroggeEnum
################################################################################
class RateType(FroggeEnum):

    Null = 0
    PerHour = 1
    PerShift = 2

################################################################################
    @property
    def proper_name(self) -> str:

        if self.value == 1:
            return "Per Hour"
        elif self.value == 2:
            return "Per Shift"

        return self.name
    
################################################################################
    @staticmethod
    def select_options() -> List[SelectOption]:
        
        return [r.select_option for r in RateType if r != RateType.Null]
    
################################################################################
    