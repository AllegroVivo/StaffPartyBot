from typing import List

from discord import SelectOption

from ._Enum import FroggeEnum
################################################################################
class RequirementLevel(FroggeEnum):

    Null = 0
    Complete = 1
    InProgress = 2
    Incomplete = 3
    Waived = 4

################################################################################
    @property
    def proper_name(self) -> str:

        if self.value == 2:
            return "In Progress"

        return self.name

################################################################################
    @staticmethod
    def select_options() -> List[SelectOption]:

        return [p.select_option for p in RequirementLevel if p.value != 0]

################################################################################
