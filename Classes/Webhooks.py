from __future__ import annotations

from flask import Flask, request, abort, url_for

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Classes import StaffPartyBot
################################################################################

__all__ = ("FroggeHookManager", )

################################################################################
class FroggeHookManager:
    
    __slots__ = (
        "_state",
        "__app__",
    )
    
################################################################################
    def __init__(self, bot: StaffPartyBot):

        self._state: StaffPartyBot = bot
        
        self.__app__: Flask = Flask(__name__)
        self.add_routes()

################################################################################
    def get_app(self) -> Flask:
        
        return self.__app__
    
################################################################################
    def add_routes(self):
        @self.__app__.route("/", methods=["POST"])
        def home():
            print(request.data)
            return "success"
    
################################################################################
    def run(self):
        
        with self.__app__.test_request_context():
            print(url_for('home', _external=True))
        self.__app__.run(debug=True, port=5000)
        
################################################################################
        