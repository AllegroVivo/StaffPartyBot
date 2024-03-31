from typing import List

from discord import SelectOption

from .DataCenter import DataCenter
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
    def contains(self, dc: DataCenter) -> bool:
        
        if dc is None:
            return False
        
        if self.value == 1:
            return dc.value in [1, 2, 3, 4]
        elif self.value == 2:
            return dc.value in [5, 6]
        elif self.value == 3:
            return dc.value in [7]
        
################################################################################
