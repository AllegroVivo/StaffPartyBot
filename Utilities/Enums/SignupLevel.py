from typing import List

from discord import SelectOption

from ._Enum import FroggeEnum
################################################################################
class SignupLevel(FroggeEnum):

    Declined = 0
    Accepted = 1
    Tentative = 2
    
################################################################################
    @staticmethod
    def select_options() -> List[SelectOption]:
        
        return [sl.select_option for sl in SignupLevel]
    
################################################################################
    