from typing import List

from discord import SelectOption

from ._Enum import FroggeEnum
################################################################################
class TrainingLevel(FroggeEnum):

    Null = 0
    Active = 1
    OnHold = 2
    Inactive = 3
    Pending = 4

################################################################################
    @property
    def proper_name(self) -> str:

        if self.value == 2:
            return "On Hold" 
            
        return self.name

################################################################################
    @staticmethod
    def select_options() -> List[SelectOption]:

        return [p.select_option for p in TrainingLevel if p.value != 0]

################################################################################
