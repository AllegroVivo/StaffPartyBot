from typing import List

from discord import SelectOption

from ._Enum import FroggeEnum
################################################################################
class TrainingLevel(FroggeEnum):

    Null = 0
    Active = 1
    Inactive = 2

################################################################################
    @staticmethod
    def select_options() -> List[SelectOption]:

        return [p.select_option for p in TrainingLevel if p.value != 0]

################################################################################
