from typing import List

from discord import SelectOption

from ._Enum import FroggeEnum
################################################################################
class JobPostingType(FroggeEnum):

    Event = 1
    ShortTermTemp = 2
    LongTermTemp = 3
    Permanent = 4
    
################################################################################
    @staticmethod
    def select_options() -> List[SelectOption]:
        
        return [t.select_option for t in JobPostingType]
    
################################################################################
    @property
    def proper_name(self) -> str:
        
        if self.value == 1:
            return "Single Event"
        if self.value == 2:
            return "Short-Term Temporary"
        if self.value == 3:
            return "Long-Term Temporary"
        
        return self.name
        
################################################################################
        