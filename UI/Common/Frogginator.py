from __future__ import annotations

from discord.ext.pages import Paginator
################################################################################

__all__ = ("Frogginator", )

################################################################################
class Frogginator(Paginator):
    
    def __init__(self, pages, **kwargs):
        
        super().__init__(
            pages=pages,
            author_check=True,
            disable_on_timeout=True,
            use_default_buttons=True,
            default_button_row=4,
            loop_pages=True,
            show_indicator=True,
            timeout=300,
            **kwargs
        )
        
################################################################################
    