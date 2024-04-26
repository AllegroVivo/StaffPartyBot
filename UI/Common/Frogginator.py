from __future__ import annotations

from discord.ext.pages import Paginator
################################################################################

__all__ = ("Frogginator", )

################################################################################
class Frogginator(Paginator):
    
    def __init__(self, pages, clear_on_timeout: bool = True, **kwargs):
        
        super().__init__(
            pages=pages,
            author_check=kwargs.pop("author_check", True),
            disable_on_timeout=kwargs.pop("disable_on_timeout", True),
            use_default_buttons=kwargs.pop("use_default_buttons", True),
            default_button_row=kwargs.pop("default_button_row", 4),
            loop_pages=kwargs.pop("loop_pages", True),
            show_indicator=kwargs.pop("show_indicator", True),
            timeout=kwargs.pop("timeout", 300),
            **kwargs
        )
        
        self.clear_on_timeout: bool = clear_on_timeout
        
################################################################################
    async def on_timeout(self) -> None:
        
        if self.clear_on_timeout:
            await self.cancel(True, self.pages[self.current_page])
        else:
            await super().on_timeout()
            
################################################################################
            