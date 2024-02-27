from __future__ import annotations

from enum import Enum
from typing import List

from discord import SelectOption
################################################################################
class FroggeEnum(Enum):

    @property
    def proper_name(self) -> str:

        return self.name

################################################################################    
    @staticmethod
    def select_options() -> List[SelectOption]:

        raise NotImplementedError

################################################################################
    @property
    def select_option(self) -> SelectOption:

        return SelectOption(label=self.proper_name, value=str(self.value))

################################################################################
