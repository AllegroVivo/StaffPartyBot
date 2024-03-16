from typing import List

from discord import SelectOption

from ._Enum import FroggeEnum
################################################################################
class RPLevel(FroggeEnum):

    NoRP = 1
    MinimalRP = 2
    SomeRP = 3
    CasualRP = 4
    ModerateRP = 5
    HalfRP = 6
    ConsiderableRP = 7
    MostlyRP = 8
    HighRP = 9
    FullyRP = 10

################################################################################
    @property
    def proper_name(self) -> str:

        return self.name.replace("RP", " RP")
    
################################################################################
    @staticmethod
    def select_options() -> List[SelectOption]:
        
        return [l.select_option for l in RPLevel]
    
################################################################################
    