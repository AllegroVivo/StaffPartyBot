from typing import List

from discord import SelectOption

from ._Enum import FroggeEnum
################################################################################
class RPLevel(FroggeEnum):

    NoRP = 1
    CasualRP = 2
    ConsiderableRP = 3
    HighRP = 4
    FullyRP = 5

################################################################################
    @property
    def proper_name(self) -> str:

        return self.name.replace("RP", " RP")
    
################################################################################
    @staticmethod
    def select_options() -> List[SelectOption]:
        
        return [l.select_option for l in RPLevel]
    
################################################################################
    