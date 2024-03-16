from typing import List

from discord import SelectOption

from ._Enum import FroggeEnum
################################################################################
class DataCenter(FroggeEnum):
    
    Aether = 1
    Crystal = 2
    Dynamis = 3
    Primal = 4
    Light = 5
    Chaos = 6
    Materia = 7

################################################################################
    @staticmethod
    def select_options() -> List[SelectOption]:
        
        return [dc.select_option for dc in DataCenter]
    
################################################################################
