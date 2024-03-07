from __future__ import annotations

from typing import TYPE_CHECKING, List, Union, Optional, Dict, Any

from discord import Message, WebhookMessage, User, Interaction, ButtonStyle
from discord.ui import View, Button

if TYPE_CHECKING:
    from .PaginatorButton import PaginatorButton
    from .Page import Page
    from .PageGroup import PageGroup
    from .PaginatorMenu import PaginatorMenu
################################################################################

__all__ = ("Paginator",)

################################################################################
class Paginator(View):
    
    __slots__ = (
        "timeout",
        "pages",
        "current_page",
        "menu",
        "show_menu",
        "menu_placeholder",
        "page_groups",
        "default_page_group",
        "page_count",
        "buttons",
        "custom_buttons",
        "show_disabled",
        "show_indicator",
        "disable_on_timeout",
        "use_default_buttons",
        "default_button_row",
        "loop_pages",
        "custom_view",
        "message",
        "usercheck",
        "user",
    )
    
################################################################################
    def __init__(
        self,
        pages: Union[List[Page], List[PageGroup]],
        show_disabled: bool = True,
        show_indicator: bool = True,
        show_menu: bool = False,
        menu_placeholder: str = "Select Page Group",
        author_check: bool = True,
        disable_on_timeout: bool = True,
        use_default_buttons: bool = True,
        default_button_row: int = 0,
        loop_pages: bool = False,
        custom_view: Optional[View] = None,
        timeout: Optional[float] = 180.0,
        custom_buttons: Optional[List[PaginatorButton]] = None,
    ):
        
        super().__init__(timeout=timeout)
        
        self.timeout: float = timeout
        
        self.pages: Union[List[Page], List[PageGroup]] = pages
        self.current_page: int = 0
        
        self.menu: Optional[PaginatorMenu] = None
        self.show_menu: bool = show_menu
        self.menu_placeholder: str = menu_placeholder
        
        self.page_groups: Optional[List[PageGroup]] = None
        self.default_page_group: int = 0
        
        if all(isinstance(pg, PageGroup) for pg in pages):
            self.page_groups = self.pages if show_menu else None
            if sum(pg.default is True for pg in self.page_groups) > 1:
                raise ValueError("only one PageGroup can be set as the default.")
            
            for pg in self.page_groups:
                if pg.default:
                    self.default_page_group = self.page_groups.index(pg)
                    break
                    
            self.pages: List[Page] = self.get_page_group_content(
                self.page_groups[self.default_page_group]
            )
            
        self.page_count: int = max(len(self.pages) - 1, 0)
        
        self.buttons: Dict[str, Dict[str, Any]] = {}
        self.custom_buttons: Optional[List[PaginatorButton]] = custom_buttons
        self.default_button_row: int = default_button_row
        
        self.show_disabled: bool = show_disabled
        self.show_indicator: bool = show_indicator
        self.disable_on_timeout: bool = disable_on_timeout
        self.use_default_buttons: bool = use_default_buttons
        self.loop_pages: bool = loop_pages
        
        self.custom_view: Optional[View] = custom_view
        self.message: Optional[Union[Message, WebhookMessage]] = None
        
        if self.custom_buttons and not self.use_default_buttons:
            for btn in custom_buttons:
                self.add_item(btn)
        elif not self.custom_buttons and self.use_default_buttons:
            self.add_default_buttons()
            
        if self.show_menu:
            self.add_menu()
            
        self.usercheck: bool = author_check
        self.user: Optional[User] = None
        
################################################################################
    async def update(
        self,
        pages: Union[List[Page], List[PageGroup]],
        show_disabled: Optional[bool] = None,
        show_indicator: Optional[bool] = None,
        show_menu: Optional[bool] = None,
        menu_placeholder: Optional[str] = None,
        author_check: Optional[bool] = None,
        disable_on_timeout: Optional[bool] = None,
        use_default_buttons: Optional[bool] = None,
        default_button_row: Optional[int] = None,
        loop_pages: Optional[bool] = None,
        custom_view: Optional[View] = None,
        timeout: Optional[float] = 180.0,
        custom_buttons: Optional[List[PaginatorButton]] = None,
        interaction: Optional[Interaction] = None,
        current_page: int = 0
    ) -> None:
        
        self.pages = pages if pages is not None else self.pages
        self.show_menu = show_menu if show_menu is not None else self.show_menu
        
        if pages is not None and all(isinstance(pg, PageGroup) for pg in pages):
            self.page_groups = self.pages if self.show_menu else None
            if sum(pg.default is True for pg in self.page_groups) > 1:
                raise ValueError("only one PageGroup can be set as the default.")
            
            for pg in self.page_groups:
                if pg.default:
                    self.default_page_group = self.page_groups.index(pg)
                    break
                    
            self.pages = self.get_page_group_content(self.page_groups[self.default_page_group])
            
        self.page_count = max(len(self.pages) - 1, 0)
        self.current_page = current_page if current_page <= self.page_count else 0
        
        self.menu_placeholder = (
            menu_placeholder if menu_placeholder is not None else self.menu_placeholder
        )
        
        self.show_disabled = (
            show_disabled if show_disabled is not None else self.show_disabled
        )
        self.show_indicator = (
            show_indicator if show_indicator is not None else self.show_indicator
        )
        self.usercheck = author_check if author_check is not None else self.usercheck
        self.disable_on_timeout = (
            disable_on_timeout if disable_on_timeout is not None else self.disable_on_timeout
        )
        self.use_default_buttons = (
            use_default_buttons if use_default_buttons is not None else self.use_default_buttons
        )
        self.loop_pages = (
            loop_pages if loop_pages is not None else self.loop_pages
        )
        
        self.default_button_row = (
            default_button_row if default_button_row is not None else self.default_button_row
        )
        self.timeout = timeout if timeout is not None else self.timeout
        
        self.custom_view = custom_view
        self.custom_buttons = (
            custom_buttons if custom_buttons is not None else self.custom_buttons
        )
        
        self.buttons = {}
        if self.use_default_buttons:
            self.add_default_buttons()
        elif self.custom_buttons:
            for btn in self.custom_buttons:
                self.add_item(btn)
                
        await self.goto_page(self.current_page, interaction=interaction)
        
################################################################################
    async def on_timeout(self) -> None:
    
        if not self.disable_on_timeout:
            return
        
        for item in self.children:
            item.disabled = True  # type: ignore

        await self.message.edit(view=self, attachments=[])
        
################################################################################
    async def disable(self, include_custom: bool = False, page: Optional[Page] = None) -> None:
    
        for item in self.children:
            if (
                include_custom
                or not self.custom_view
                or item not in self.custom_view.children
            ):
                item.disabled = True  # type: ignore
                
        page = self.get_page_content(page)
        if page:
            await self.message.edit(embeds=page.embeds, view=self)
        else:
            await self.message.edit(view=self)

################################################################################
    async def cancel(self, include_custom: bool = False, page: Optional[Page] = None) -> None:
        
        items = self.children.copy()
        for item in items:
            if (
                include_custom
                or not self.custom_view
                or item not in self.custom_view.children
            ):
                self.remove_item(item)
                
        page = self.get_page_content(page)
        if page:
            await self.message.edit(embeds=page.embeds, view=self)
        else:
            await self.message.edit(view=self)
            
#################################################################################
    async def goto_page(self, pg_number: int = 0, *, interaction: Optional[Interaction] = None) -> None:
            
        self.update_buttons()
        self.current_page = pg_number
        
        if self.show_indicator:
            try:
                self.buttons["page_indicator"][
                    "object"
                ].label = f"{self.current_page + 1}/{self.page_count + 1}"
            except KeyError:
                pass
            
        page = self.pages[pg_number]
        page = self.get_page_content(page)
        
        if page.custom_view:
            self.update_custom_view(page.custom_view)
            
        if interaction:
            await interaction.response.defer()
            await interaction.followup.edit_message(
                message_id=self.message.id, embeds=page.embeds, view=self
            )
        else:
            await self.message.edit(embeds=page.embeds, view=self)
    
################################################################################
    async def interaction_check(self, interaction: Interaction) -> bool:
        
        if self.usercheck:
            return self.user == interaction.user
        return True
    
################################################################################
    def add_menu(self) -> None:
        
        self.menu = PaginatorMenu(self.page_groups, placeholder=self.menu_placeholder)
        self.menu.paginator = self
        
        self.add_item(self.menu)
        
################################################################################
    def add_default_buttons(self) -> None:
        
        default_buttons = [
            PaginatorButton(
                "first",
                label="<<",
                style=ButtonStyle.primary,
                row=self.default_button_row
            ),
            PaginatorButton(
                "prev",
                label="<",
                style=ButtonStyle.danger,
                loop_label="↪",
                row=self.default_button_row
            ),
            PaginatorButton(
                "page_indicator",
                style=ButtonStyle.secondary,
                disabled=True,
                row=self.default_button_row
            ),
            PaginatorButton(
                "next",
                label=">",
                style=ButtonStyle.success,
                loop_label="↩",
                row=self.default_button_row
            ),
            PaginatorButton(
                "last",
                label=">>",
                style=ButtonStyle.primary,
                row=self.default_button_row
            )
        ]
        
        for btn in default_buttons:
            self.add_item(btn)
            
################################################################################
    def add_button(self, button: PaginatorButton) -> None:
        
        self.buttons[button.button_type] = {
            "object": Button(
                style=button.style,
                label=(
                    button.label
                    if button.label or button.emoji
                    else (
                        button.button_type.capitalize()
                        if button.button_type != "page_indicator"
                        else f"{self.current_page + 1}/{self.page_count + 1}"
                    )
                ),
                disabled=button.disabled,
                custom_id=button.custom_id,
                emoji=button.emoji,
                row=button.row
            ),
            "label": button.label,
            "loop_label": button.loop_label,
            "hidden": (
                button.disabled
                if button.button_type != "page_indicator"
                else not self.show_indicator
            )
        }
        
        self.buttons[button.button_type]["object"].callback = button.callback
        button.paginator = self
        
################################################################################
    def remove_button(self, button_type: str) -> None:
    
        if button_type not in self.buttons.keys():
            raise ValueError(
                f"No button_type {button_type} was found in this paginator."
            )
        
        self.buttons.pop(button_type)
        
################################################################################
    def update_buttons(self) -> Dict[str, Dict[str, Union[PaginatorButton, bool]]]:

        for key, button in self.buttons.items():
            if key == "first":
                if self.current_page <= 1:
                    button["hidden"] = True
                elif self.current_page >= 1:
                    button["hidden"] = False
            elif key == "last":
                if self.current_page >= self.page_count - 1:
                    button["hidden"] = True
                if self.current_page < self.page_count - 1:
                    button["hidden"] = False
            elif key == "next":
                if self.current_page == self.page_count:
                    if not self.loop_pages:
                        button["hidden"] = True
                        button["object"].label = button["label"]
                    else:
                        button["object"].label = button["loop_label"]
                elif self.current_page < self.page_count:
                    button["hidden"] = False
                    button["object"].label = button["label"]
            elif key == "prev":
                if self.current_page <= 0:
                    if not self.loop_pages:
                        button["hidden"] = True
                        button["object"].label = button["label"]
                    else:
                        button["object"].label = button["loop_label"]
                elif self.current_page >= 0:
                    button["hidden"] = False
                    button["object"].label = button["label"]

        self.clear_items()
        if self.show_indicator:
            try:
                self.buttons["page_indicator"][
                    "object"
                ].label = f"{self.current_page + 1}/{self.page_count + 1}"
            except KeyError:
                pass
        for key, button in self.buttons.items():
            if key != "page_indicator":
                if button["hidden"]:
                    button["object"].disabled = True
                    if self.show_disabled:
                        self.add_item(button["object"])
                else:
                    button["object"].disabled = False
                    self.add_item(button["object"])
            elif self.show_indicator:
                self.add_item(button["object"])
                
        if self.show_menu:
            self.add_menu()
            
        if self.custom_view:
            self.update_custom_view(self.custom_view)
            
        return self.buttons
    
################################################################################
    def update_custom_view(self, custom_view: View) -> None:
    
        if isinstance(self.custom_view, View):
            for item in self.custom_view.children:
                self.remove_item(item)
            
        for item in custom_view.children:
            self.add_item(item)
            
################################################################################
        