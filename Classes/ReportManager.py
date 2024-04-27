from __future__ import annotations

import os
from datetime import datetime
from typing import TYPE_CHECKING, List

import pandas as pd
from discord import Interaction, Member, Role, File

if TYPE_CHECKING:
    from Classes import StaffPartyBot
################################################################################

__all__ = ("ReportManager",)

################################################################################
class ReportManager:
    
    __slots__ = (
        "_state",
    )
    
################################################################################
    def __init__(self, bot: StaffPartyBot):
        
        self._state: StaffPartyBot = bot
        
################################################################################
    @staticmethod
    async def roles_report(interaction: Interaction, members: List[Member], roles: List[Role]) -> None:
        
        # Prepare the data structure
        data = {
            "Discord ID": [],
            "Discord Username": [],
            "Server Display Name": [],
            "Server Join Date": []
        }
    
        # Prepare a column for each role
        for role in roles:
            data[role.name] = []  # Role name as column header
    
        # Populate the data structure
        for member in members:
            data["Discord ID"].append(str(member.id))
            data["Discord Username"].append(member.name)
            data["Server Display Name"].append(member.display_name)
            join_dt = member.joined_at
            data["Server Join Date"].append(
                datetime(
                    join_dt.year,
                    join_dt.month,
                    join_dt.day
                ).strftime("%Y-%m-%d")
            )
    
            # Check each role
            member_roles = set(member.roles)
            for role in roles:
                data[role.name].append('Yes' if role in member_roles else 'No')
    
        # Create a DataFrame
        df = pd.DataFrame(data)
    
        # Write the DataFrame to an Excel file
        df.to_excel("roles_report.xlsx", index=False, engine='openpyxl')
    
        # Send the Excel file
        with open("roles_report.xlsx", "rb") as f:
            await interaction.respond(
                f"Excel file roles_report.xlsx has been created with member data.", 
                file=File(f)  # type: ignore
            )
            
        # Delete the Excel file
        os.remove("roles_report.xlsx")
        
################################################################################
