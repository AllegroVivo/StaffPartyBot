from __future__ import annotations

from flask import Flask, request, abort

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Classes import TrainingBot
################################################################################

__all__ = ("FroggeHookManager", )

################################################################################
class FroggeHookManager:
    
    __slots__ = (
        "_state",
    )

    __app__: Flask = Flask(__name__)
    
################################################################################
    def __init__(self, bot: TrainingBot):
        
        self._state: TrainingBot = bot
        
################################################################################
    @property
    def app(self) -> Flask:
        
        return self.__app__
    
################################################################################
    @property
    def bot(self) -> TrainingBot:
        
        return self._state
    
################################################################################
    @__app__.route("/venue_update", methods=["POST"])
    def venue_update(self):
        
        print(request.data)
        return "success"
    
################################################################################
    