from __future__ import annotations

import asyncio
import os
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, List, Optional

import pandas as pd
from discord import Interaction, Member, Role, File

from Utilities import log, GlobalDataCenter

if TYPE_CHECKING:
    from Classes import StaffPartyBot, XIVVenue
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
        
        log.info(
            "Core",
            f"Creating roles report for {len(members)} members and {len(roles)} roles."
        )
        
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
        
        log.info("Core", "Roles report created and sent!")
        
################################################################################
    @staticmethod
    async def itinerary_report(
        interaction: Interaction,
        hours_out: int,
        venues: List[XIVVenue], 
        region: Optional[str]
    ) -> None:
        
        log.info("Core", f"Creating itinerary report for region: {region}.")

        if region is None:
            filtered_venues = venues
        else:
            dc_names = [
                dc.proper_name.lower()
                for dc in GlobalDataCenter.data_centers_by_region(region)
            ]
            filtered_venues = [
                venue for venue in venues
                if venue.location.data_center and
                venue.location.data_center.lower() in dc_names
            ]
            
        log.info("Core", f"Filtered venues count: {len(filtered_venues)}")

        # Prepare the data structure
        data = {
            "Itinerary String": [],
            "Venue Name": [],
            "Data Center": [],
            "Home World": [],
            "Housing Div.": [],
            "Ward": [],
            "Plot": [],
            "Open Time": [],
            "Close Time": [],
            "Tags": []
        }
        
        # Nightclubs sorted by DC
        # Everything else sorted by 
        
        start_limit = datetime.now()
        end_limit = start_limit + timedelta(hours=hours_out)
        
        for venue in filtered_venues:
            if venue.resolution:
                # Need to create tz-naive datetime object for comparison
                res_start = datetime(
                    year=venue.resolution.start.year,
                    month=venue.resolution.start.month,
                    day=venue.resolution.start.day,
                    hour=venue.resolution.start.hour,
                    minute=venue.resolution.start.minute
                )
                if res_start < end_limit:
                    data["Venue Name"].append(venue.name)
                    data["Data Center"].append(venue.location.data_center)
                    data["Home World"].append(venue.location.world)
                    data["Housing Div."].append(venue.location.district)
                    data["Ward"].append(venue.location.ward)
                    data["Plot"].append(venue.location.plot)
                    data["Open Time"].append(
                        datetime(
                            year=venue.resolution.start.year,
                            month=venue.resolution.start.month,
                            day=venue.resolution.start.day,
                            hour=venue.resolution.start.hour,
                            minute=venue.resolution.start.minute
                        ).strftime("%H:%M %p")
                    )
                    data["Close Time"].append(
                        datetime(
                            year=venue.resolution.end.year,
                            month=venue.resolution.end.month,
                            day=venue.resolution.end.day,
                            hour=venue.resolution.end.hour,
                            minute=venue.resolution.end.minute
                        ).strftime("%H:%M %p")
                    )
                    data["Tags"].append(", ".join(venue.tags[:3]) if venue.tags else "None")
                    data["Itinerary String"].append(venue.to_itinerary_string())

        # Create a DataFrame
        df = pd.DataFrame(data)

        date_str = start_limit.strftime("%Y-%m-%d")
        prefix = region.upper() if region else "FULL"
        xl_path = f"{prefix}_itinerary_{date_str}.xlsx"
        
        # Write the DataFrame to an Excel file
        df.to_excel(xl_path, index=False, engine='openpyxl')

        # Send the Excel file
        with open(xl_path, "rb") as f:
            await interaction.respond(
                f"Excel file {xl_path} has been created with itinerary data.",
                file=File(f)  # type: ignore
            )

        log.info("Core", "Itinerary report created and sent!")
        
        # Attempt to delete the Excel file after waiting a few seconds
        await asyncio.sleep(10)
        try:
            os.remove(xl_path)
        except PermissionError:
            log.error("Core", f"Could not delete {xl_path} due to a permission error.")
            # The container will eventually delete the file when it restarts
            # anyway, so we aren't too worried about this.
            pass
        except Exception as ex:
            log.error("Core", f"Could not delete {xl_path} due to an unexpected error: {ex}")
        else:
            log.info(
                "Core",
                f"Deleted {xl_path} after sending the itinerary report."
            )
            
################################################################################
            