from ._Enum import FroggeEnum
from discord import SelectOption
from typing import List
################################################################################
class DataCenter(FroggeEnum):
    
    Aether = 1
    Chaos = 2
    Crystal = 3
    Dynamis = 4
    Elemental = 5
    Gaia = 6
    Light = 7
    Mana = 8
    Materia = 9
    Meteor = 10
    Primal = 11

################################################################################
    @staticmethod
    def select_options() -> List[SelectOption]:
        
        return [dc.select_option for dc in DataCenter]
    
################################################################################
    