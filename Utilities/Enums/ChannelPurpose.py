from typing import List

from discord import SelectOption

from ._Enum import FroggeEnum
################################################################################
class ChannelPurpose(FroggeEnum):
    
    TempJobs = 1
    PermJobs = 2
    Venues = 3
    Profiles = 4
    LogStream = 5

################################################################################
    @staticmethod
    def select_options() -> List[SelectOption]:
        
        return [dc.select_option for dc in ChannelPurpose]
    
################################################################################
    @property
    def proper_name(self) -> str:
        
        if self.value == 1:
            return "Temporary Jobs"
        elif self.value == 2:
            return "Permanent Jobs"
        elif self.value == 5:
            return "Log Stream"
        
        return self.name
    
################################################################################   
