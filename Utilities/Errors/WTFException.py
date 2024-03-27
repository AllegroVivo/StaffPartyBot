from __future__ import annotations
################################################################################

__all__ = ("WTFException",)

################################################################################
class WTFException(Exception):

    def __init__(self, message: str):
        
        super().__init__(
            "I'm not entirely sure what happened just now... but it "
            "wasn't good... : " + message
        )        
        
################################################################################
        