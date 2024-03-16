from typing import List

from discord import SelectOption

from ._Enum import FroggeEnum
################################################################################
class NSFWPreference(FroggeEnum):

    SFW = 1
    NSFW = 2

################################################################################
    @staticmethod
    def select_options() -> List[SelectOption]:
        
        return [o.select_option for o in NSFWPreference]
    
################################################################################    
        