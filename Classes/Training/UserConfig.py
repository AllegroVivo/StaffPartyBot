from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Type, TypeVar, Tuple, Any

from discord import Embed
from discord import EmbedField

from Assets import BotEmojis
from Utilities import Utilities as U

if TYPE_CHECKING:
    from Classes import TUser
################################################################################

__all__ = ("UserConfiguration",)

UC = TypeVar("UC", bound="UserConfiguration")

################################################################################
class UserConfiguration:
    """Class to represent a user's configuration settings.
    
    Attributes
    ----------
    _parent: TUser
        The user to which this configuration belongs.
    _image: Optional[str]
        The image URL for the user's profile picture.
    _trainee_pings: bool
        Whether the user should be pinged when a job is available.
    """

    __slots__ = (
        "_parent",
        "_image",
        "_trainee_pings",
    )

################################################################################
    def __init__(
        self,
        parent: TUser,
        image: Optional[str] = None,
        job_pings: bool = True
    ):

        self._parent: TUser = parent

        self._image: Optional[str] = image
        self._trainee_pings: bool = job_pings

################################################################################
    @classmethod
    def load(cls: Type[UC], parent: TUser, data: Tuple[Any, ...]) -> UC:

        return cls(parent,  data[0],  data[1])

################################################################################
    @property
    def user_id(self) -> int:
        
        return self._parent.user_id
    
################################################################################
    @property
    def trainee_pings(self) -> bool:

        return self._trainee_pings

################################################################################
    @property
    def image(self) -> Optional[str]:

        return self._image

################################################################################
    def status(self) -> Embed:

        fields = [
            EmbedField(
                name="__Trainee Pings__",
                value=f"{BotEmojis.Check if self._trainee_pings else BotEmojis.Cross}",
                inline=True
            )
        ]

        return U.make_embed(
            title=f"User Configuration for __{self._parent.name}__",
            description=U.draw_line(extra=35),
            fields=fields
        )

################################################################################
    def toggle_trainee_pings(self) -> None:

        self._trainee_pings = not self._trainee_pings
        self.update()

################################################################################
    def update(self) -> None:

        self._parent.bot.database.update.tuser_config(self)

################################################################################
