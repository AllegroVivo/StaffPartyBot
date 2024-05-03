from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Dict, Optional, Tuple

from discord import (
    Interaction,
    ForumChannel,
    Member,
    EmbedField
)
from discord.ext.pages import Page

from UI.Common import Frogginator, ConfirmCancelView
from UI.Jobs import JobReportRangeModal
from Utilities import (
    Utilities as U,
    VenueDoesntExistError,
    JobPostingNotFoundError,
    DateTimeFormatError,
    DateTimeMismatchError,
)
from Utilities import log
from .JobPosting import JobPosting

if TYPE_CHECKING:
    from Classes import GuildData, StaffPartyBot, VenueManager, Venue
################################################################################

__all__ = ("JobsManager",)

################################################################################
class JobsManager:
    
    __slots__ = (
        "_guild",
        "_postings",
    )
    
################################################################################
    def __init__(self, guild: GuildData):
        
        self._guild: GuildData = guild
        
        self._postings: List[JobPosting] = []
        
################################################################################
    async def _load_all(self, data: Dict[str, Any]) -> None:

        for _, posting in data["job_postings"].items():
            self._postings.append(await JobPosting.load(self, posting))
            
################################################################################
    def get_posting(self, post_id: str) -> Optional[JobPosting]:
        
        log.debug("Jobs", f"Searching for job posting with ID {post_id}")
        
        for posting in self._postings:
            if posting.id == post_id:
                return posting
    
################################################################################
    @property
    def bot(self) -> StaffPartyBot:
        
        return self._guild.bot
    
################################################################################
    @property
    def guild(self) -> GuildData:
        
        return self._guild
    
################################################################################
    @property
    def venue_manager(self) -> VenueManager:
        
        return self._guild.venue_manager
    
################################################################################
    @property
    def guild_id(self) -> int:
        
        return self._guild.guild_id
    
################################################################################
    @property
    def all_postings(self) -> List[JobPosting]:
        
        return self._postings
    
################################################################################
    @property
    def temporary_jobs_channel(self) -> Optional[ForumChannel]:
        
        return self.guild.channel_manager.temp_job_channel
        
################################################################################
    @property
    def permanent_jobs_channel(self) -> Optional[ForumChannel]:
        
        return self.guild.channel_manager.perm_job_channel
        
################################################################################
    async def create_new(self, interaction: Interaction, venue_name: str) -> None:
        
        log.info(
            "Jobs",
            f"Creating new job posting for {venue_name} by {interaction.user.display_name}"
        )

        venue = self.venue_manager.get_venue(venue_name)
        if venue is None:
            log.warning("Jobs", f"Venue {venue_name} does not exist")
            error = VenueDoesntExistError(venue_name)
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        if not await self.venue_manager.authenticate(venue, interaction.user, interaction):
            log.warning(
                "Jobs",
                f"{interaction.user.display_name} does not have permission to post for {venue_name}"
            )
            return
        
        posting = JobPosting.new(self, venue, interaction.user)
        self._postings.append(posting)
        
        log.info("Jobs", f"Job posting created with ID {posting.id}")
        
        await posting.menu(interaction)
    
################################################################################
    async def check_status(self, interaction: Interaction, post_id: str) -> None:
        
        log.info("Jobs", f"Checking status of job posting with ID {post_id}")
        
        posting = self.get_posting(post_id)
        if posting is None:
            log.warning("Jobs", f"Job posting with ID {post_id} not found")
            error = JobPostingNotFoundError(post_id)
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        await posting.menu(interaction)
        
################################################################################
    async def cull_job_postings(self) -> None:
        
        if self.temporary_jobs_channel is None:
            return
        
        log.info("Jobs", "Culling job postings")
        
        for posting in self._postings:
            await posting.expiration_check()
            
        for thread in self.temporary_jobs_channel.threads:
            count = 0
            async for _ in thread.history():
                count += 1
            if count == 0:
                log.debug("Jobs", f"Deleting empty thread {thread.name}")
                await thread.delete()
        
################################################################################
    async def temp_job_report(self, interaction: Interaction) -> None:
        
        log.info("Jobs", "Creating temporary job report")
        
        modal = JobReportRangeModal()
        
        await interaction.response.send_modal(modal)
        await modal.wait()
        
        if not modal.complete:
            log.warning("Jobs", "Job report modal not completed")
            return
        
        try:
            start_dt = datetime.strptime(modal.value[0], "%m/%d/%Y")
        except ValueError:
            log.warning("Jobs", f"Invalid start date format: {modal.value[0]}")
            error = DateTimeFormatError(modal.value[0])
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        try:
            end_dt = datetime.strptime(modal.value[1], "%m/%d/%Y")
        except ValueError:
            log.warning("Jobs", f"Invalid end date format: {modal.value[1]}")
            error = DateTimeFormatError(modal.value[1])
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        if start_dt > end_dt:
            log.warning("Jobs", f"Start date '{start_dt}' is after end date '{end_dt}'")
            error = DateTimeMismatchError(start_dt, end_dt)
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        job_postings = [
            posting for posting in self._postings
            if posting.end_time is not None and start_dt <= posting.end_time <= end_dt
        ]
        job_postings.sort(key=lambda x: x.start_time)
        
        job_dict: Dict[Venue, List[JobPosting]] = {}
        for jp in job_postings:
            if jp.venue not in job_dict:
                job_dict[jp.venue] = []
            job_dict[jp.venue].append(jp)

        # Initial setup
        pages = []
        col1 = col2 = col3 = ""
        current_length = 0
        venue_continued = False

        def add_page():
            nonlocal pages, col1, col2, col3, current_length
            report = U.make_embed(
                title="Temporary Job Postings",
                fields=[
                    EmbedField("** **", col1, True),
                    EmbedField("** **", col2, True),
                    EmbedField("** **", col3, True)
                ]
            )
            pages.append(Page(embeds=[report]))
            col1 = col2 = col3 = ""
            current_length = 0

        for venue, postings in job_dict.items():
            # Calculate the potential new lengths
            venue_name = f"{venue.name} (cont.)" if venue_continued else venue.name
            potential_addition = sum(
                len(
                    posting.candidate.name 
                    if posting.candidate else "Not Accepted"
                ) + len(
                    U.format_dt(posting.start_time, 'd')
                ) + len(
                    U.format_dt(posting.start_time, 't') + " - " + U.format_dt(posting.end_time, 't')
                ) + 3  # +3 for newlines and formatting
                for posting in postings
            ) + len(venue_name)
    
            # Check if adding the current venue's postings would exceed the limit
            if current_length + potential_addition > 5800:
                add_page()  # Finalize current page and start a new one
                venue_continued = False  # Reset continuation status for the new page
    
            if not venue_continued:
                col1 += f"__**{venue_name}**__\n"
                col2 += "** **\n"
                col3 += "** **\n"
                current_length += len(venue_name) + 6  # +6 for newlines and formatting
    
            for posting in postings:
                entry = (
                    f"{U.format_dt(posting.start_time, 'd')}\n",
                    f"{U.format_dt(posting.start_time, 't')} - "
                    f"{U.format_dt(posting.end_time, 't')}\n",
                    f"{posting.candidate.name if posting.candidate else 'Not Accepted'}\n"
                )
                if current_length + sum(len(e) for e in entry) > 5800:
                    add_page()  # Start a new page
                    col1 += f"__**{venue.name} (cont.)**__\n** **\n"  # Add continuation header
                    col2 += "** **\n"
                    col3 += "** **\n"
                    current_length += len(venue.name) + 14  # Adjust length for continuation header
    
                col1 += entry[0]
                col2 += entry[1]
                col3 += entry[2]
                current_length += sum(len(e) for e in entry)  # Update current length
                venue_continued = True  # Mark as continued for potential next page
    
            venue_continued = False  # Reset for next venue
    
        # Check if there's content left for a final page
        if current_length > 0:
            add_page()
            
        log.info("Jobs", f"Sending temporary job report with {len(pages)} pages")
    
        # Send report paginator
        frogginator = Frogginator(pages=pages)
        await frogginator.respond(interaction)

################################################################################
    async def delete_all_by_venue(self, venue: Venue) -> int:
        
        log.info("Jobs", f"Deleting all job postings for {venue.name}")
        
        count = 0
        
        for p in self._postings:
            if p.venue == venue:
                await p.delete()
                count += 1
                
        return count

################################################################################
    async def on_member_leave(self, member: Member) -> Tuple[int, int]:
        
        log.info("Jobs", f"Member Left. Deleting all job postings for {member.display_name}")
        
        delete_count = 0
        cancel_count = 0
        
        for posting in self._postings:
            if posting.user.id == member.id:
                await posting.delete()
                delete_count += 1
            if posting.candidate is not None and posting.candidate.user_id == member.id:
                await posting.cancel()
                
        log.info("Jobs", f"Deleted {delete_count} job postings and cancelled {cancel_count}.")
        return delete_count, cancel_count

################################################################################
    async def bulk_update(self, interaction: Interaction) -> None:
        
        log.info("Jobs", "Bulk updating all job postings")
        
        prompt = U.make_embed(
            title="Bulk Update",
            description=(
                "This tool will perform an update on all job postings.\n\n"

                "This will take **SOME TIME.** Please confirm that you wish "
                "to proceed with this action."
            )
        )
        view = ConfirmCancelView(interaction.user)
        
        await interaction.respond(embed=prompt, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            log.debug("Jobs", "Bulk update cancelled")
            return
        
        msg = await interaction.followup.send("Please wait...")
        
        count = 0
        for posting in self._postings:
            await posting._update_post_components()
            count += 1
        
        await msg.delete()
        
        confirm = U.make_embed(
            title="Bulk Update Complete",
            description=f"Successfully updated {count} job postings."
        )
        await interaction.respond(embed=confirm)
        
        log.info("Jobs", f"Bulk update complete. Updated {count} job postings.")
        
################################################################################
        