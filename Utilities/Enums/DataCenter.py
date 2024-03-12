from ._Enum import FroggeEnum
from discord import SelectOption
from typing import List
################################################################################
class DataCenter(FroggeEnum):
    
    Americas = 1
    Europe = 2
    Oceania = 3

################################################################################
    @staticmethod
    def select_options() -> List[SelectOption]:
        
        return [dc.select_option for dc in DataCenter]
    
################################################################################
    