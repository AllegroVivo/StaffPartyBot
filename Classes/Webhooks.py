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
        "__app__",
    )
    
################################################################################
    def __init__(self, bot: TrainingBot):

        self._state: TrainingBot = bot
        
        self.__app__: Flask = Flask(__name__)
        self.add_routes()

################################################################################
    def get_app(self) -> Flask:
        
        return self.__app__
    
################################################################################
    def add_routes(self):
        # Define routes using a decorator method
        @self.__app__.route("/", methods=["POST"])
        def home():
            print(request.data)
            return "success"
    
################################################################################
    def run(self):
        # Use a separate method to run the app
        with self.__app__.test_request_context():
            print(url_for('home', _external=True))  # Correctly reference 'home'
        self.__app__.run(debug=True, port=5000)
        
################################################################################
        