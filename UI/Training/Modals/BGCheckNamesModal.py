from __future__ import annotations

from typing import List

from discord import Interaction, InputTextStyle
from discord.ui import InputText

from UI.Common import FroggeModal
################################################################################

__all__ = ("BGCheckNamesModal",)

################################################################################
class BGCheckNamesModal(FroggeModal):
    
    def __init__(self, cur_val: List[str]):
        
        super().__init__(title="Edit Names")
        
        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Instructions",
                placeholder="Enter your character name(s).",
                value=(
                    "Please enter the name(s) of your game character(s).\n"
                    "Separate names with a comma - eg. 'Allegro Vivo, Vivace Vivo'."
                ),
                required=False
            )
        )
        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Name(s)",
                placeholder="eg. 'Allegro Vivo'",
                value=", ".join(cur_val) if cur_val else None,
                max_length=200,
                required=True
            )
        )
        
    async def callback(self, interaction: Interaction):
        self.value = [
            n.strip() for n in self.children[1].value.split(",")
        ] if self.children[1].value else []
        self.complete = True
        
        await interaction.edit()
        self.stop()

################################################################################
