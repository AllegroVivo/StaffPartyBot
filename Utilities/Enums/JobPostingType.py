from typing import List

from discord import SelectOption

from ._Enum import FroggeEnum
################################################################################
class JobPostingType(FroggeEnum):

    Temporary = 1
    Permanent = 2
    
################################################################################
    @staticmethod
    def select_options() -> List[SelectOption]:
        
        return [t.select_option for t in JobPostingType]
    
################################################################################
