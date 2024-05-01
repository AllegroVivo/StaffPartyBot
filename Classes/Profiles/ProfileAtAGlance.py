from __future__ import annotations

import math
import re
from typing import TYPE_CHECKING, List, Optional, Union, Type, TypeVar, Any, Tuple, Dict

from discord import Interaction, Embed, EmbedField

from Assets import BotEmojis
from UI.Profiles import (
    GenderPronounView,
    RaceClanSelectView,
    OrientationSelectView,
    ProfileHeightModal,
    ProfileAgeModal,
    ProfileMareModal,
    AtAGlanceStatusView
)
from UI.Venues import DataCenterSelectView, HomeWorldSelectView
from Utilities import (
    Utilities as U,
    Gender,
    Pronoun,
    Race,
    Clan,
    Orientation,
    HeightInputError,
    NS,
    FroggeEnum,
    DataCenter,
    GameWorld,
    GlobalDataCenter
)
from .ProfileSection import ProfileSection

if TYPE_CHECKING:
    from Classes import Profile
################################################################################

__all__ = ("ProfileAtAGlance",)

AAG = TypeVar("AAG", bound="ProfileAtAGlance")

################################################################################
class ProfileAtAGlance(ProfileSection):
    
    __slots__ = (
        "_gender",
        "_pronouns",
        "_race",
        "_clan",
        "_orientation",
        "_height",
        "_age",
        "_mare",
        "_dc",
        "_world",
    )

################################################################################
    def __init__(self, parent: Profile, **kwargs) -> None:
        
        super().__init__(parent)

        self._gender: Optional[Union[Gender, str]] = kwargs.pop("gender", None)
        self._pronouns: List[Pronoun] = kwargs.pop("pronouns", None) or []
        self._race: Optional[Union[Race, str]] = kwargs.pop("race", None)
        self._clan: Optional[Union[Clan, str]] = kwargs.pop("clan", None)
        self._orientation: Optional[Union[Orientation, str]] = kwargs.pop("orientation", None)
        self._height: Optional[int] = kwargs.pop("height", None)
        self._age: Optional[Union[str, int]] = kwargs.pop("age", None)
        self._mare: Optional[str] = kwargs.pop("mare", None)
        self._dc: List[GlobalDataCenter] = kwargs.pop("data_centers", None) or []
     
################################################################################
    @classmethod
    def load(cls: Type[AAG], parent: Profile, data: Tuple[Any, ...]) -> AAG:

        gender = race = clan = orientation = None
        if data[0] is not None:
            gender = Gender(int(data[0])) if data[0].isdigit() else data[0]
        if data[2] is not None:
            race = Race(int(data[2])) if data[2].isdigit() else data[2]
        if data[3] is not None:
            clan = Clan(int(data[3])) if data[3].isdigit() else data[3]
        if data[4] is not None:
            orientation = Orientation(int(data[4])) if data[4].isdigit() else data[4]

        return cls(
            parent=parent,
            gender=gender,
            pronouns=[Pronoun(int(x)) for x in data[1]] if data[1] else [],
            race=race,
            clan=clan,
            orientation=orientation,
            height=data[5],
            age=data[6],
            mare=data[7],
            data_centers=[GlobalDataCenter(dc) for dc in data[8]] if data[8] else [],
        )
    
################################################################################
    @property
    def gender(self) -> Optional[Union[Gender, str]]:
        
        return self._gender
    
    @gender.setter
    def gender(self, value: Optional[Union[Gender, str]]) -> None:
        
        self._gender = value
        self.update()
        
################################################################################
    @property
    def pronouns(self) -> List[Pronoun]:
        
        return self._pronouns
    
    @pronouns.setter
    def pronouns(self, value: List[Pronoun]) -> None:
        
        self._pronouns = value
        self.update()
        
################################################################################
    @property
    def race(self) -> Optional[Union[Race, str]]:
        
        return self._race
    
    @race.setter
    def race(self, value: Optional[Union[Race, str]]) -> None:
        
        self._race = value
        self.update()
        
################################################################################
    @property
    def clan(self) -> Optional[Union[Clan, str]]:
        
        return self._clan
    
    @clan.setter
    def clan(self, value: Optional[Union[Clan, str]]) -> None:
        
        self._clan = value
        self.update()
        
################################################################################
    @property
    def orientation(self) -> Optional[Union[Orientation, str]]:
        
        return self._orientation
    
    @orientation.setter
    def orientation(self, value: Optional[Union[Orientation, str]]) -> None:
        
        self._orientation = value
        self.update()
        
################################################################################
    @property
    def height(self) -> Optional[int]:
        
        return self._height
    
    @height.setter
    def height(self, value: Optional[int]) -> None:
        
        self._height = value
        self.update()
        
################################################################################
    @property
    def age(self) -> Optional[Union[str, int]]:
        
        return self._age
    
    @age.setter
    def age(self, value: Optional[Union[str, int]]) -> None:
        
        self._age = value
        self.update()
        
################################################################################
    @property
    def mare(self) -> Optional[str]:
        
        return self._mare
    
    @mare.setter
    def mare(self, value: Optional[str]) -> None:
        
        self._mare = value
        self.update()
        
################################################################################
    @property
    def data_centers(self) -> List[GlobalDataCenter]:
        
        return self._dc
    
    @data_centers.setter
    def data_centers(self, value: List[GlobalDataCenter]) -> None:
        
        self._dc = value
        self.update()
        
################################################################################
    def update(self) -> None:

        self.parent.bot.database.update.profile_ataglance(self)
    
################################################################################
    async def menu(self, interaction: Interaction) -> None:
        
        embed = self.status()
        view = AtAGlanceStatusView(interaction.user, self)
        
        await interaction.response.send_message(embed=embed, view=view)
        await view.wait()
    
################################################################################
    @staticmethod
    def get_attribute_str(attr: Any) -> str:

        if not attr:
            return str(NS)
        elif isinstance(attr, FroggeEnum):
            return attr.proper_name
        elif isinstance(attr, int):
            return str(attr)
        elif isinstance(attr, str):
            return attr
        elif isinstance(attr, list):
            return "/".join([p.proper_name for p in attr])
        else:
            raise ValueError(f"Invalid attribute type: {type(attr)}")
        
################################################################################
    def format_height(self) -> str:
            
        if self.height is None:
            return str(NS)

        inches = int(self._height / 2.54)
        feet = int(inches / 12)
        leftover = int(inches % 12)

        return f"{feet}' {leftover}\" (~{self.height} cm.)"
    
################################################################################    
    def status(self) -> Embed:

        race_val = self.get_attribute_str(self.race)
        clan_val = self.get_attribute_str(self.clan)

        raceclan = f"{race_val}/{clan_val}"
        if isinstance(self.race, str) or isinstance(self.clan, str):
            raceclan += "\n*(Custom Value(s))*"

        gender_val = self.get_attribute_str(self.gender)
        pronoun_val = self.get_attribute_str(self.pronouns)

        gp_combined = f"{gender_val} -- *({pronoun_val})*"
        if isinstance(self.gender, str):
            gp_combined += "\n*(Custom Value)*"

        orientation_val = self.get_attribute_str(self.orientation)
        if isinstance(self.orientation, str):
            orientation_val += "\n*(Custom Value)*"

        height_val = self.format_height()
        age_val = self.get_attribute_str(self.age)
        mare_val = self.get_attribute_str(self.mare)
        dc_val = self.get_attribute_str(self.data_centers)

        fields = [
            EmbedField("__Home Regions__", dc_val, True),
            EmbedField("", U.draw_line(extra=30), False),
            EmbedField("__Race/Clan__", raceclan, True),
            EmbedField("__Gender/Pronouns__", gp_combined, True),
            EmbedField("", U.draw_line(extra=30), False),
            EmbedField("__Orientation__", orientation_val, True),
            EmbedField("__Mare ID__", mare_val, True),
            EmbedField("", U.draw_line(extra=30), False),
            EmbedField("__Height__", height_val, True),
            EmbedField("__Age__", age_val, True),
        ]

        return U.make_embed(
            color=self.parent.color,
            title=f"At A Glance Section Details for {self.parent.char_name}",
            description=(
                "*All sections, aside from **Home Region(s)** are optional.*\n"
                "*(Click the corresponding button below to edit each data point.)*\n"
                f"{U.draw_line(extra=38)}"
            ),
            fields=fields,
            timestamp=False
        )
    
################################################################################
    async def set_gender(self, interaction: Interaction) -> None:

        prompt = U.make_embed(
            title="Gender/Pronoun Selection",
            description=(
                "Pick your preferred gender from the selector below.\n"
                "Don't worry,  you'll be able to choose your pronouns next!\n\n"

                "**If you select `Custom`, a pop-up will appear for you\n"
                "to provide your custom gender text.**"
            )
        )
        view = GenderPronounView(interaction.user, self)

        await interaction.response.send_message(embed=prompt, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            return
        
        self.gender = view.value[0]
        self.pronouns = view.value[1]
    
################################################################################
    async def set_raceclan(self, interaction: Interaction) -> None:

        prompt = U.make_embed(
            title="Select Your Race & Clan",
            description=(
                "Pick your character's race from the drop-down below.\n"
                "An additional selector will then appear for you to choose your clan.\n\n"

                "**If none of those apply, you may select `Custom`, and a pop-up will\n"
                "appear for you to enter your own custom information into.**"
            )
        )
        view = RaceClanSelectView(interaction.user, self)

        await interaction.response.send_message(embed=prompt, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            return
        
        self.race = view.value[0]
        self.clan = view.value[1]
        
################################################################################
    async def set_orientation(self, interaction: Interaction) -> None:

        prompt = U.make_embed(
            title="Select Your Orientation",
            description=(
                "Pick your preferred orientation from the selector below.\n\n"

                "**If you select `Custom`, a pop-up will appear for\n"
                "you to provide your custom orientation value.**"
            )
        )
        view = OrientationSelectView(interaction.user, self)

        await interaction.response.send_message(embed=prompt, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            return
        
        self.orientation = view.value

################################################################################
    async def set_height(self, interaction: Interaction) -> None:
        
        modal = ProfileHeightModal(self.height)
        
        await interaction.response.send_modal(modal)
        await modal.wait()
        
        if not modal.complete:
            return
        
        raw = modal.value
        if raw is None:
            self.height = None
            return

        result = re.match(
            r"^(\d+)\s*cm\.?|(\d+)\s*(?:ft\.?|feet|')$|(\d+)\s*(?:in\.?|inches|\"|'')|"
            r"(\d+)\s*(?:ft\.?|feet|')\s*(\d+)\s*(?:in\.?|inches|\"|'')",
            raw
        )

        if not result:
            error = HeightInputError(raw)
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        if result.group(1):
            self.height = int(result.group(1))
        elif result.group(2):
            cm = int(result.group(2)) * 12 * 2.54
            self.height = math.ceil(cm)
        elif result.group(3):
            cm = int(result.group(3)) * 2.54
            self.height = math.ceil(cm)
        elif result.group(4) and result.group(5):
            inches = int(result.group(4)) * 12 + int(result.group(5))
            self.height = math.ceil(inches * 2.54)

################################################################################
    async def set_age(self, interaction: Interaction) -> None:
        
        modal = ProfileAgeModal(self.age)
        
        await interaction.response.send_modal(modal)
        await modal.wait()
        
        if not modal.complete:
            return
        
        self.age = modal.value
    
################################################################################
    async def set_mare(self, interaction: Interaction) -> None:
        
        modal = ProfileMareModal(self.mare)
        
        await interaction.response.send_modal(modal)
        await modal.wait()
        
        if not modal.complete:
            return
        
        self.mare = modal.value

################################################################################
    async def set_data_centers(self, interaction: Interaction) -> None:
        
        prompt = U.make_embed(
            title="Select Your Home Region(s)",
            description=(
                "Pick your character's home region(s) from the drop-down below."
            )
        )
        view = DataCenterSelectView(interaction.user)
        
        await interaction.respond(embed=prompt, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            return
        
        self.data_centers = view.value
        
################################################################################
    def progress(self) -> str:

        em_data_centers = self.progress_emoji(self._dc)
        em_gender = self.progress_emoji(self._gender)
        em_race = self.progress_emoji(self._race)
        em_orientation = self.progress_emoji(self._orientation)
        em_height = self.progress_emoji(self._height)
        em_age = self.progress_emoji(self._age)
        em_mare = self.progress_emoji(self._mare)

        return (
            f"{U.draw_line(extra=15)}\n"
            "__**At A Glance**__\n"
            f"{em_data_centers} -- Home Region(s)\n"
            f"{em_gender} -- Gender / Pronouns\n"
            f"{em_race} -- Race / Clan\n"
            f"{em_orientation} -- Orientation\n"
            f"{em_height} -- Height\n"
            f"{em_age} -- Age\n"
            f"{em_mare} -- Friend ID\n"
        )

################################################################################
    def _raw_string(self) -> str:

        ret = (
            self.compile_data_center() +
            self.compile_gender() +
            self.compile_raceclan() +
            self.compile_orientation() +
            self.compile_height() +
            self.compile_age() +
            self.compile_mare()
        )

        if ret:
            ret += U.draw_line(extra=15)

        return ret

################################################################################
    def compile(self) -> Optional[EmbedField]:

        if not self._raw_string():
            return

        return EmbedField(
            name=f"{BotEmojis.Eyes}  __At A Glance__ {BotEmojis.Eyes}",
            value=self._raw_string(),
            inline=False
        )

################################################################################
    def compile_gender(self) -> str:

        if self.gender is None:
            return ""

        gender = self._gender.proper_name if isinstance(self._gender, Gender) else self._gender
        ret = f"__Gender:__ {gender}"

        if self.pronouns:
            pronouns = "/".join([p.proper_name for p in self._pronouns])
            ret += f" -- *({pronouns})*"

        ret += "\n"

        return ret

################################################################################
    def compile_raceclan(self) -> str:

        if self.race is None:
            return ""

        race = self._race.proper_name if isinstance(self._race, Race) else self._race
        ret = f"__Race:__ {race}"

        if self.clan is not None:
            clan = self._clan.proper_name if isinstance(self._clan, Clan) else self._clan
            ret += f" / {clan}"

        ret += "\n"

        return ret

################################################################################
    def compile_orientation(self) -> str:

        if self.orientation is None:
            return ""

        orientation = (
            self._orientation.proper_name
            if isinstance(self._orientation, Orientation)
            else self._orientation
        )
        return f"__Orientation:__ {orientation}\n"

################################################################################
    def compile_height(self) -> str:

        if self.height is None:
            return ""

        return f"__Height:__ {self.format_height()}\n"

################################################################################
    def compile_age(self) -> str:

        if self.age is None:
            return ""

        return f"__Age:__ {self.age}\n"

################################################################################
    def compile_mare(self) -> str:

        if self.mare is None:
            return ""

        return f"__Mare ID:__ `{self.mare}`\n"

################################################################################
    def compile_data_center(self) -> str:

        if not self.data_centers:
            return ""

        dc_string = ", ".join([f"`{dc.abbreviation}`" for dc in self.data_centers])
        return f"__Home Regions:__ {dc_string}\n"
    
################################################################################
    def _to_dict(self) -> Dict[str, Any]:
        
        return {
            "gender": (
                self.gender.value if isinstance(self.gender, FroggeEnum)
                else self.gender
            ),
            "pronouns": [p.value for p in self.pronouns],
            "race": (
                self.race.value if isinstance(self.race, FroggeEnum)
                else self.race
            ),
            "clan": (
                self.clan.value if isinstance(self.clan, FroggeEnum)
                else self.clan
            ),
            "orientation": (
                self.orientation.value if isinstance(self.orientation, FroggeEnum)
                else self.orientation
            ),
            "height": self.height,
            "age": self.age,
            "mare": self.mare,
            "data_centers": [dc.value for dc in self.data_centers]
        }
    
################################################################################
