from typing import List

from discord import SelectOption

from ._Enum import FroggeEnum
################################################################################
class HousingZone(FroggeEnum):

    Mist = 1
    LavenderBeds = 2
    TheGoblet = 3
    Shirogane = 4
    Empyreum = 5

################################################################################
    @staticmethod
    def select_options() -> List[SelectOption]:
        
        return [o.select_option for o in HousingZone]
    
################################################################################    
    @property
    def proper_name(self) -> str:
        
        if self.value == 2:
            return "Lavender Beds"
        elif self.value == 3:
            return "The Goblet"
        else:
            return self.name
        
################################################################################
        