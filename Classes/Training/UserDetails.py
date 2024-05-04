from __future__ import annotations

from typing import TYPE_CHECKING, Optional, List

from discord import Embed, Interaction, User

from UI.Common import YesNoView
from UI.Training import TUserNameModal, TUserNotesModal, DataCenterSelectView
from Utilities import Utilities as U, GlobalDataCenter, log

if TYPE_CHECKING:
    from Classes import TUser, StaffPartyBot
################################################################################

__all__ = ("UserDetails", )

################################################################################
class UserDetails:
    
    __slots__ = (
        "_parent",
        "_name",
        "_notes",
        "_hiatus",
        "_data_centers",
        "_guidelines",
    )
    
################################################################################
    def __init__(self, parent: TUser, **kwargs):
        
        self._parent: TUser = parent
        
        self._name: Optional[str] = kwargs.get("name", None)
        self._notes: Optional[str] = kwargs.get("notes", None)
        self._hiatus: Optional[bool] = kwargs.get("hiatus", None)
        self._guidelines: bool = kwargs.get("guidelines", False)
        
        self._data_centers: List[GlobalDataCenter] = kwargs.get("data_centers", None) or []
        
################################################################################
    @classmethod
    def load(cls, user: TUser, data: dict) -> UserDetails:
        
        return cls(
            parent=user,
            name=data[0],
            notes=data[1],
            hiatus=data[2],
            data_centers=[GlobalDataCenter(int(dc)) for dc in data[3]] if data[3] else None,
            guidelines=data[4],
        )
    
################################################################################
    @property
    def bot(self) -> StaffPartyBot:
        
        return self._parent.bot
    
################################################################################
    @property
    def user_id(self) -> int:
        
        return self._parent.user_id
    
################################################################################
    @property
    def name(self) -> Optional[str]:
        
        return self._name or self._parent.user.display_name
    
    @name.setter
    def name(self, value: Optional[str]) -> None:
        
        self._name = value
        self.update()
        
################################################################################
    @property
    def notes(self) -> Optional[str]:
        
        return self._notes
    
    @notes.setter
    def notes(self, value: Optional[str]) -> None:
        
        self._notes = value
        self.update()
        
################################################################################
    @property
    def hiatus(self) -> Optional[bool]:
        
        return self._hiatus
    
    @hiatus.setter
    def hiatus(self, value: Optional[bool]) -> None:
        
        self._hiatus = value
        self.update()
        
################################################################################
    @property
    def data_centers(self) -> List[GlobalDataCenter]:
        
        return self._data_centers 
    
    @data_centers.setter
    def data_centers(self, value: Optional[List[GlobalDataCenter]]) -> None:
        
        self._data_centers = value or []
        self.update()
        
################################################################################
    @property
    def guidelines_accepted(self) -> bool:
        
        return self._guidelines
    
    @guidelines_accepted.setter
    def guidelines_accepted(self, value: bool) -> None:
        
        self._guidelines = value
        self.update()
        
################################################################################
    def update(self) -> None:
        
        self.bot.database.update.tuser_details(self)
        
################################################################################
    async def set_name(self, interaction: Interaction) -> None:

        log.info(
            "Training",
            f"User {self.user_id} ({self.name}) is changing their name."
        )

        modal = TUserNameModal(self._name)

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            log.debug("Training", "User cancelled name change.")
            return

        self.name = modal.value
        
        log.info(
            "Training",
            (
                f"User {self.user_id} ({self.name}) has changed their name to "
                f"{modal.value}."
            )
        )

################################################################################
    async def set_notes(self, interaction: Interaction) -> None:
        
        log.info(
            "Training",
            f"User {self.user_id} ({self.name}) is changing their notes."
        )

        modal = TUserNotesModal(self._notes)

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            log.debug("Training", "User cancelled notes change.")
            return

        self.notes = modal.value
        
        log.info(
            "Training",
            (
                f"User {self.user_id} ({self.name}) has changed their notes to "
                f"{modal.value}."
            )
        )

################################################################################
    def toggle_hiatus(self) -> None:
        
        self.hiatus = not self.hiatus
        
        log.info(
            "Training",
            (
                f"User {self.user_id} ({self.name}) is toggling their hiatus "
                f"status. New status: {self.hiatus}"    
            )
        )

################################################################################
    async def set_data_centers(self, interaction: Interaction) -> None:
        
        log.info(
            "Training",
            f"User {self.user_id} ({self.name}) is changing their data centers."
        )
        
        embed = U.make_embed(
            title="Data Center",
            description=(
                "Please select the data center(s) you want to use for all "
                "training activities."
            )
        )
        view = DataCenterSelectView(interaction.user)
        
        await interaction.respond(embed=embed, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            log.debug("Training", "User cancelled data center selection.")
            return
        
        self.data_centers = view.value
        
        log.info(
            "Training",
            (
                f"User {self.user_id} ({self.name}) has changed their data "
                f"centers to {view.value}."
            )
        )
    
################################################################################
    async def accept_guidelines(self, interaction: Interaction) -> bool:
        
        log.info(
            "Training",
            f"User {self.user_id} ({self.name}) is accepting the trainer guidelines."
        )
        
        prompt = U.make_embed(
            title="Please Accept the Trainer Guidelines",
            description=(
                "I confirm I have read and understood the guidelines and will "
                "do trainings within these parameters.\n\n"
                
                "https://discord.com/channels/1104515062187708525/1220565996314820670"
            )
        )
        view = YesNoView(interaction.user)
        
        await interaction.respond(embed=prompt, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            log.debug("Training", "User declined the guidelines.")
            return False
        
        self.guidelines_accepted = True
        
        log.info(
            "Training",
            f"User {self.user_id} ({self.name}) has accepted the guidelines."
        )
        
        return True
        
################################################################################
