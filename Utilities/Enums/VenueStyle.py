from typing import List

from discord import SelectOption

from ._Enum import FroggeEnum
################################################################################
class VenueStyle(FroggeEnum):

    Nightclub = 1
    Bar = 2
    Cafe = 3
    Lounge = 4
    BathHouse = 5
    Restaurant = 6
    FightClub = 7
    Casino = 8
    Shop = 9
    MaidCafe = 10
    Brothel = 11
    Other = 12

################################################################################
    @property
    def proper_name(self) -> str:

        if self.value == 5:
            return "Bath House"
        elif self.value == 7:
            return "Fight Club"
        elif self.value == 10:
            return "Maid Cafe"

        return self.name
    
################################################################################
    @staticmethod
    def select_options() -> List[SelectOption]:
        
        return [vs.select_option for vs in VenueStyle]
    
################################################################################
    