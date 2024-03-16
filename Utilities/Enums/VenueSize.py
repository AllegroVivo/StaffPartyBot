from typing import List

from discord import SelectOption

from ._Enum import FroggeEnum
################################################################################
class VenueSize(FroggeEnum):

    Apartment = 1
    Small = 2
    Medium = 3
    Large = 4
    
################################################################################
    @staticmethod
    def select_options() -> List[SelectOption]:
        
        return [vs.select_option for vs in VenueSize]
    
################################################################################
    