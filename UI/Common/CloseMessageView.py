from __future__ import annotations

from discord import User

from .FroggeView import FroggeView
from .CloseMessageButton import CloseMessageButton
################################################################################

__all__ = ("CloseMessageView",)

################################################################################        
class CloseMessageView(FroggeView):

    def __init__(self, owner: User):
        super().__init__(owner, close_on_complete=True)

        self.add_item(CloseMessageButton())

################################################################################
