from __future__ import annotations

from typing import TYPE_CHECKING, Optional, List

from discord import Embed, Interaction, User

from UI.Training import TUserNameModal, TUserNotesModal, DataCenterSelectView
from Utilities import Utilities as U, GlobalDataCenter

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
    )
    
################################################################################
    def __init__(
        self,
        parent: TUser,
        name: Optional[str] = None,
        notes: Optional[str] = None,
        hiatus: Optional[bool] = None,
        data_centers: Optional[List[GlobalDataCenter]] = None
    ):
        
        self._parent: TUser = parent
        
        self._name: Optional[str] = name
        self._notes: Optional[str] = notes
        self._hiatus: Optional[bool] = hiatus
        
        self._data_centers: List[GlobalDataCenter] = data_centers or []
        
################################################################################
    @classmethod
    def load(cls, user: TUser, data: dict) -> UserDetails:
        
        return cls(
            parent=user,
            name=data[0],
            notes=data[1],
            hiatus=data[2],
            data_centers=[GlobalDataCenter(int(dc)) for dc in data[3]] if data[3] else None
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
    def update(self) -> None:
        
        self.bot.database.update.tuser_details(self)
        
################################################################################
    async def set_name(self, interaction: Interaction) -> None:

        modal = TUserNameModal(self._name)

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.name = modal.value

################################################################################
    async def set_notes(self, interaction: Interaction) -> None:

        modal = TUserNotesModal(self._notes)

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.notes = modal.value

################################################################################
    def toggle_hiatus(self) -> None:
        
        self.hiatus = not self.hiatus

################################################################################
    async def set_data_centers(self, interaction: Interaction) -> None:
        
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
            return
        
        self.data_centers = view.value
    
################################################################################
