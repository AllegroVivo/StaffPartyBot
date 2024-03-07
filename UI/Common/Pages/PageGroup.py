from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Union

from discord import Emoji, PartialEmoji
from discord.ui import View

if TYPE_CHECKING:
    from .Page import Page
    from .PaginatorButton import PaginatorButton
################################################################################

__all__ = ("PageGroup",)

################################################################################
class PageGroup:
    
    __slots__ = (
        "label",
        "description",
        "emoji",
        "pages",
        "default",
        "show_disabled",
        "show_indicator",
        "author_check",
        "disable_on_timeout",
        "use_default_buttons",
        "default_button_row",
        "loop_pages",
        "custom_view",
        "timeout",
        "custom_buttons",
        "trigger_on_display"
    )
    
################################################################################
    def __init__(
        self,
        pages: List[Page],
        label: str,
        description: Optional[str] = None,
        emoji: Union[str, Emoji, PartialEmoji] = None, 
        default: Optional[bool] = None,
        show_disabled: Optional[bool] = None,
        show_indicator: Optional[bool] = None,
        author_check: Optional[bool] = None,
        disable_on_timeout: Optional[bool] = None,
        use_default_buttons: Optional[bool] = None,
        default_button_row: int = 0,
        loop_pages: Optional[bool] = None,
        custom_view: Optional[View] = None,
        timeout: Optional[float] = None,
        custom_buttons: Optional[List[PaginatorButton]] = None,
        trigger_on_display: Optional[bool] = None,
    ):

        self.label: str = label
        self.description: Optional[str] = description
        self.emoji: Union[str, Emoji, PartialEmoji] = emoji
        self.pages: List[Page] = pages
        self.default: Optional[bool] = default
        self.show_disabled: Optional[bool] = show_disabled
        self.show_indicator: Optional[bool] = show_indicator
        self.author_check: Optional[bool] = author_check
        self.disable_on_timeout: Optional[bool] = disable_on_timeout
        self.use_default_buttons: Optional[bool] = use_default_buttons
        self.default_button_row: int = default_button_row
        self.loop_pages: Optional[bool] = loop_pages
        self.custom_view: Optional[View] = custom_view
        self.timeout: Optional[float] = timeout
        self.custom_buttons: List[PaginatorButton] = custom_buttons or []
        self.trigger_on_display: Optional[bool] = trigger_on_display
        
################################################################################
        