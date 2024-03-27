from __future__ import annotations

from typing import Optional, Any

from discord import Interaction, InputTextStyle
from discord.ui import InputText

from UI.Common import FroggeModal
################################################################################

__all__ = ("LocationElementModal",)

################################################################################
class LocationElementModal(FroggeModal):
    
    def __init__(self, component_name: str, cur_value: Optional[Any]):
        
        super().__init__(title=f"Edit {component_name} Number")
        
        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Instructions",
                placeholder=f"Enter the venue's {component_name} number.",
                value=(
                    f"Enter the {component_name} number for the venue.\n"
                    "This should just be a raw number. (eg. 5, 12) or "
                    f"leave blank to clear the {component_name} number."
                ),
                required=False
            )
        )
        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label=component_name,
                placeholder="eg. '12'",
                value=str(cur_value) if cur_value else None,
                max_length=2,
                required=False
            )
        )
        
    async def callback(self, interaction: Interaction):
        try:
            self.value = int(self.children[1].value) if self.children[1].value else None
        except ValueError:
            self.value = -1
        self.complete = True
        
        await interaction.edit()
        self.stop()

################################################################################
