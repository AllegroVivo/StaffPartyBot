from __future__ import annotations

from typing import Union, TYPE_CHECKING
from discord import Emoji, PartialEmoji, ButtonStyle, Interaction
from discord.ui import Button

if TYPE_CHECKING:
    from .Paginator import Paginator
################################################################################

__all__ = ("PaginatorButton", )

################################################################################
class PaginatorButton(Button):
    
    __slots__ = (
        "button_type",
        "loop_label",
        "paginator",
    )
    
################################################################################    
    def __init__(
        self,
        button_type: str,
        label: str = None,
        emoji: Union[Emoji, PartialEmoji] = None,
        style: ButtonStyle = ButtonStyle.success,
        disabled: bool = False,
        custom_id: str = None,
        row: int = 0,
        loop_label: str = None
    ):
        
        super().__init__(
            label=label if label or emoji else button_type.capitalize(),
            emoji=emoji,
            style=style,
            disabled=disabled,
            custom_id=custom_id,
            row=row
        )
        
        self.button_type: str = button_type
        self.loop_label: str = self.label if not loop_label else loop_label
        self.paginator: Paginator = None
        
################################################################################
    async def callback(self, interaction: Interaction):
        
        match self.button_type:
            case "first":
                self.paginator.current_page = 0
            case "prev":
                if self.paginator.loop_pages and self.paginator.current_page == 0:
                    self.paginator.current_page = self.paginator.page_count
                else:
                    self.paginator.current_page -= 1
            case "next":
                if (
                    self.paginator.loop_pages and
                    self.paginator.current_page == self.paginator.page_count
                ):
                    self.paginator.current_page = 0
                else:
                    self.paginator.current_page += 1
            case "last":
                self.paginator.current_page = self.paginator.page_count
            
        await self.paginator.goto_page(
            page_number=self.paginator.current_page, interaction=interaction
        )
            
################################################################################
        