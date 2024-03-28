from typing import List

from discord import SelectOption

from ._Enum import FroggeEnum
################################################################################
class Weekday(FroggeEnum):

    Monday = 0
    Tuesday = 1
    Wednesday = 2
    Thursday = 3
    Friday = 4
    Saturday = 5
    Sunday = 6

################################################################################
    @staticmethod
    def select_options() -> List[SelectOption]:

        return [p.select_option for p in Weekday]

################################################################################
