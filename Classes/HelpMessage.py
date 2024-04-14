from __future__ import annotations

from typing import TYPE_CHECKING, List
from discord import Interaction, Embed, EmbedField
from discord.ext.pages import Page, PageGroup

from UI.Common import Frogginator

if TYPE_CHECKING:
    from Classes import TrainingBot
################################################################################

__all__ = ("HelpMessage",)

################################################################################
class HelpMessage:
    
    __slots__ = (
        "_state",
    )
    
################################################################################
    def __init__(self, bot: TrainingBot):
        
        self._state: TrainingBot = bot
    
################################################################################
    async def menu(self, interaction: Interaction) -> None:
        
        page_groups = self._prepare_page_groups()
        frogginator = Frogginator(
            pages=page_groups,
            show_menu=True,
            menu_placeholder="Select a situation to get more info..."
        )
        await frogginator.respond(interaction)
        
################################################################################
    def _prepare_page_groups(self) -> List[PageGroup]:
        
        return [
            PageGroup(
                label="Start Here",
                pages=[
                    self._welcome_page()
                ]
            ),
            PageGroup(
                label="I Want to Train",
                description="I am new to one or more jobs and would like to learn new skills.",
                pages=self._training_pages
            )
        ]
    
################################################################################
    @staticmethod
    def _welcome_page() -> Page:
        
        embed = Embed(
            title="Welcome to the Staff Party Bus!",
            description=(
                "The purpose of this server is to provide **fill-in staff** "
                "to venues who might experience a last minute shortage.\n\n"
                
                "It also offers staff a wide range of venue experience "
                "and resources:\n\n"
                
                "* **Training** - __Learn new skills and improve existing ones.__\n"
                "*We offer a complete training to new staff including a "
                "venue etiquette guide.*\n\n"
                
                "* **BG Check** - __All staff members are cleared.__\n"
                "*We require all staff and trainers to complete a (short) "
                "background check before they can work with us.*\n\n"
                
                "Select your situation from the menu below to get more information."
            )
        )
        
        return Page(embeds=[embed])
    
################################################################################
    @staticmethod
    def _training_pages() -> Page:
        
        page1 = Embed(
            title="Training in New Skills",
            description=(
                "**One of the exciting things about SPB is the opportunity to "
                "learn new skills.**\n\n"
            )
        )
        
        return Page(
            embeds=[
                page1,
            ]
        )
    
################################################################################
