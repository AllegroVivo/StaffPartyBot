from typing import List

from discord import SelectOption

from ._Enum import FroggeEnum
################################################################################
class RateType(FroggeEnum):

    PerHour = 1
    PerShift = 2
    PerRound = 3

################################################################################
    @property
    def proper_name(self) -> str:

        if self.value == 3:
            return "Non-Binary"

        return self.name
    
################################################################################
    @staticmethod
    def select_options() -> List[SelectOption]:
        
        return [r.select_option for r in RateType]
    
################################################################################
    