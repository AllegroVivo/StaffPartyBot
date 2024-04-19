from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from Classes.Common import AdditionalImage

if TYPE_CHECKING:
    from Classes import ServiceProfile
################################################################################

__all__ = ("SPAdditionalImage",)

################################################################################
class SPAdditionalImage(AdditionalImage):

    @classmethod
    def new(cls, parent: ServiceProfile, url: str, caption: Optional[str]) -> PAdditionalImage:

        new_id = parent.bot.database.insert.addl_image(parent.parent.id, url, caption)
        return cls(parent=parent, _id=new_id, url=url, caption=caption)

################################################################################
    def update(self) -> None:

        self._parent.parent.bot.database.update.profile_addl_image(self)

################################################################################
    def delete(self) -> None:

        self._parent.parent.bot.database.delete.profile_addl_image(self)

################################################################################
    