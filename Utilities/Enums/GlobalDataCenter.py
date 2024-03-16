from typing import List

from discord import SelectOption

from ._Enum import FroggeEnum
################################################################################
class GlobalDataCenter(FroggeEnum):
    
    Americas = 1
    Europe = 2
    Oceania = 3

################################################################################
    @staticmethod
    def select_options() -> List[SelectOption]:
        
        return [dc.select_option for dc in GlobalDataCenter]
    
################################################################################
    @property
    def abbreviation(self) -> str:
        
        if self.value == 1:
            return "AM"
        elif self.value == 2:
            return "EU"
        elif self.value == 3:
            return "OC"
    
################################################################################
