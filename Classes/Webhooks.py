from __future__ import annotations

from flask import Flask, request, abort, url_for

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
    
    with __app__.test_request_context():
        print(url_for('self.home', _external=True))
    
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
    @__app__.route("/", methods=["POST"])
    def home(self):
        
        print(request.data)
        return "success"
    
################################################################################
    