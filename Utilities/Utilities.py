import math
import os
import re
import textwrap
from datetime import datetime, time, timezone
from typing import Any, List, Optional, Tuple, Union, Literal

import pytz
import requests
from discord import Colour, Embed, EmbedField, NotFound, Interaction
from discord.abc import Mentionable
from dotenv import load_dotenv

from .Colors import CustomColor
from .Enums import Timezone, MentionableType
from .Errors import DateTimeFormatError, DateTimeMismatchError, DateTimeBeforeNowError, TimeRangeError
################################################################################

__all__ = ("Utilities", )

TimestampStyle = Literal["f", "F", "d", "D", "t", "T", "R"]

################################################################################
class Utilities:
    """A collection of utility functions for use in various parts of the bot."""

    TIMEZONE_OFFSETS = {
        Timezone.MIT: pytz.timezone('Pacific/Midway'),
        Timezone.HST: pytz.timezone('Pacific/Honolulu'),
        Timezone.AST: pytz.timezone('US/Alaska'),
        Timezone.PST: pytz.timezone('US/Pacific'),
        Timezone.MST: pytz.timezone('US/Mountain'),
        Timezone.CST: pytz.timezone('US/Central'),
        Timezone.EST: pytz.timezone('US/Eastern'),
        Timezone.PRT: pytz.timezone('America/Puerto_Rico'),
        Timezone.AGT: pytz.timezone('America/Argentina/Buenos_Aires'),
        Timezone.CAT: pytz.timezone('Africa/Harare'),
        Timezone.GMT: pytz.timezone('GMT'),
        Timezone.ECT: pytz.timezone('Europe/Paris'),
        Timezone.EET: pytz.timezone('Europe/Bucharest'),
        Timezone.EAT: pytz.timezone('Africa/Nairobi'),
        Timezone.NET: pytz.timezone('Asia/Yerevan'),
        Timezone.PLT: pytz.timezone('Asia/Karachi'),
        Timezone.BST: pytz.timezone('Asia/Dhaka'),
        Timezone.VST: pytz.timezone('Asia/Ho_Chi_Minh'),
        Timezone.CTT: pytz.timezone('Asia/Shanghai'),
        Timezone.JST: pytz.timezone('Asia/Tokyo'),
        Timezone.AET: pytz.timezone('Australia/Sydney'),
        Timezone.SST: pytz.timezone('Pacific/Guadalcanal'),
        Timezone.NST: pytz.timezone('Pacific/Auckland'),
    }
    
################################################################################
    
    JOB_WEIGHTS = {
        'gamba': 1,
        'shout runner': 2,
        'bartender': 3,
        'greeter': 4,
        'photographer': 5,
        'dj': 6,
        'courtesan': 7,
        'exotic dancer': 8,
        'host-dancer': 9,
        'pillow': 10,
        'security': 11,
        'tarot reader': 12,
        'manager': 13,
        'rp flex': 14,
        'pf attendant': 15,
        'bard': 16
    }
    
################################################################################
    @staticmethod
    def make_embed(
        *,
        title: Optional[str] = None,
        description: Optional[str] = None,
        url: Optional[str] = None,
        color: Optional[Union[Colour, int]] = None,
        thumbnail_url: Optional[str] = None,
        image_url: Optional[str] = None,
        author_text: Optional[str] = None,
        author_url: Optional[str] = None,
        author_icon: Optional[str] = None,
        footer_text: Optional[str] = None,
        footer_icon: Optional[str] = None,
        timestamp: Union[datetime, bool] = False,
        fields: Optional[List[Union[Tuple[str, Any, bool], EmbedField]]] = None
    ) -> Embed:
        """Creates and returns a Discord embed with the provided parameters.
    
        All parameters are optional.
    
        Parameters:
        -----------
        title: :class:`str`
            The embed's title.
    
        description: :class:`str`
            The main text body of the embed.
    
        url: :class:`str`
            The URL for the embed title to link to.
    
        color: Optional[Union[:class:`Colour`, :class:`int`]]
            The desired accent color. Defaults to :func:`colors.random_all()`
    
        thumbnail_url: :class:`str`
            The URL for the embed's desired thumbnail image.
    
        image_url: :class:`str`
            The URL for the embed's desired main image.
    
        footer_text: :class:`str`
            The text to display at the bottom of the embed.
    
        footer_icon: :class:`str`
            The icon to display to the left of the footer text.
    
        author_name: :class:`str`
            The text to display at the top of the embed.
    
        author_url: :class:`str`
            The URL for the author text to link to.
    
        author_icon: :class:`str`
            The icon that appears to the left of the author text.
    
        timestamp: Union[:class:`datetime`, `bool`]
            Whether to add the current time to the bottom of the embed.
            Defaults to ``False``.
    
        fields: Optional[List[Union[Tuple[:class:`str`, Any, :class:`bool`], :class:`EmbedField`]]]
            List of tuples or EmbedFields, each denoting a field to be added
            to the embed. If entry is a tuple, values are as follows:
                0 -> Name | 1 -> Value | 2 -> Inline (bool)
            Note that in the event of a tuple, the value at index one is automatically cast to a string for you.
    
        Returns:
        --------
        :class:`Embed`
            The finished embed object.
        """

        embed = Embed(
            colour=color if color is not None else CustomColor.random_all(),
            title=title,
            description=description,
            url=url
        )

        embed.set_thumbnail(url=thumbnail_url)
        embed.set_image(url=image_url)

        if author_text is not None:
            embed.set_author(
                name=author_text,
                url=author_url,
                icon_url=author_icon
            )

        if footer_text is not None:
            embed.set_footer(
                text=footer_text,
                icon_url=footer_icon
            )

        if isinstance(timestamp, datetime):
            embed.timestamp = timestamp
        elif timestamp is True:
            embed.timestamp = datetime.now()

        if fields is not None:
            if all(isinstance(f, EmbedField) for f in fields):
                embed.fields = fields
            else:
                for f in fields:
                    if isinstance(f, EmbedField):
                        embed.fields.append(f)
                    elif isinstance(f, tuple):
                        embed.add_field(name=f[0], value=f[1], inline=f[2])
                    else:
                        continue

        return embed

################################################################################
    @staticmethod
    def _text_length(text: str) -> float:

        value = 0.0

        for c in text:
            if c == "'":
                value += 0.25
            elif c in ("i", "j", ".", " "):
                value += 0.30
            elif c in ("I", "!", ";", "|", ","):
                value += 0.35
            elif c in ("f", "l", "`", "[", "]"):
                value += 0.40
            elif c in ("(", ")", "t"):
                value += 0.45
            elif c in ("r", "t", "1" "{", "}", '"', "\\", "/"):
                value += 0.50
            elif c in ("s", "z", "*", "-"):
                value += 0.60
            elif c in ("x", "^"):
                value += 0.65
            elif c in ("a", "c", "e", "g", "k", "v", "y", "J", "7", "_", "=", "+", "~", "<", ">", "?"):
                value += 0.70
            elif c in ("n", "o", "u", "2", "5", "6", "8", "9"):
                value += 0.75
            elif c in ("b", "d", "h", "p", "q", "E", "F", "L", "S", "T", "Z", "3", "4", "$"):
                value += 0.80
            elif c in ("P", "V", "X", "Y", "0"):
                value += 0.85
            elif c in ("A", "B", "C", "D", "K", "R", "#", "&"):
                value += 0.90
            elif c in ("G", "H", "U"):
                value += 0.95
            elif c in ("w", "N", "O", "Q", "%"):
                value += 1.0
            elif c in ("m", "W"):
                value += 1.15
            elif c == "M":
                value += 1.2
            elif c == "@":
                value += 1.3

        return value

################################################################################
    @staticmethod
    def draw_line(*, text: str = "", num_emoji: int = 0, extra: float = 0.0) -> str:

        text_value = extra + (1.95 * num_emoji) + Utilities._text_length(text)
        return "═" * math.ceil(text_value)

################################################################################
    @staticmethod
    def format_dt(dt: datetime, /, style: TimestampStyle | None = None) -> str:
        """A helper function to format a :class:`datetime.datetime` for presentation within Discord.

        This allows for a locale-independent way of presenting data using Discord specific Markdown.

        +-------------+----------------------------+-----------------+
        |    Style    |       Example Output       |   Description   |
        +=============+============================+=================+
        | t           | 22:57                      | Short Time      |
        +-------------+----------------------------+-----------------+
        | T           | 22:57:58                   | Long Time       |
        +-------------+----------------------------+-----------------+
        | d           | 17/05/2016                 | Short Date      |
        +-------------+----------------------------+-----------------+
        | D           | 17 May 2016                | Long Date       |
        +-------------+----------------------------+-----------------+
        | f (default) | 17 May 2016 22:57          | Short Date Time |
        +-------------+----------------------------+-----------------+
        | F           | Tuesday, 17 May 2016 22:57 | Long Date Time  |
        +-------------+----------------------------+-----------------+
        | R           | 5 years ago                | Relative Time   |
        +-------------+----------------------------+-----------------+

        Note that the exact output depends on the user's locale setting in the client. 
        The example output presented is using the ``en-GB`` locale.

        Parameters
        ----------
        dt: :class:`datetime.datetime`
            The datetime to format.
        style: :class:`str`
            The style to format the datetime with.

        Returns
        -------
        :class:`str`
            The formatted string.
        """
        if style is None:
            return f"<t:{int(dt.timestamp())}>"
        return f"<t:{int(dt.timestamp())}:{style}>"

################################################################################
    @staticmethod
    def time_to_datetime(_time: time) -> datetime:

        return datetime(
            year=2069,
            month=4,
            day=20,
            hour=_time.hour,
            minute=_time.minute,
            second=_time.second,
        )

################################################################################
    @staticmethod
    def titleize(text: str) -> str:
    
        return re.sub(
            r"[A-Za-z]+('[A-Za-z]+)?",
            lambda word: word.group(0).capitalize(),
            text
        )   

################################################################################
    @staticmethod
    def parse_salary(salary: str) -> Optional[int]:

        # Remove commas and whitespace, and make lowercase
        salary = salary.lower().strip().replace(",", "")

        try:
            if salary.endswith("k"):
                return int(salary[:-1]) * 1000
            elif salary.endswith("m"):
                return int(salary[:-1]) * 1000000
            else:
                return int(salary)
        except ValueError:
            return

################################################################################
    @staticmethod
    def wrap_text(text: str, line_length: int) -> str:
        
        return "\n".join(textwrap.wrap(text, width=line_length))
    
################################################################################
    @staticmethod
    def crop_image_square(fp: str) -> str:
        """Crops an image to a square aspect ratio.

        Parameters
        ----------
        fp: :class:`str`
            The file path to the image.

        Returns
        -------
        :class:`str`
            The file path to the cropped image.
        """
        from PIL import Image

        with Image.open(fp) as img:
            width, height = img.size
            size = min(width, height)

            left = (width - size) // 2
            top = (height - size) // 2
            right = (width + size) // 2
            bottom = (height + size) // 2

            img = img.crop((left, top, right, bottom))
            img.save(fp)

        return fp
    
################################################################################
    @staticmethod
    async def listen_for_mentionable(
        interaction: Interaction,
        prompt: Embed,
        _type: MentionableType
    ) -> Optional[Mentionable]:

        match _type:
            case MentionableType.User:
                pattern = r"<@!?(\d+)>"
            case MentionableType.Role:
                pattern = r"<@&(\d+)>"
            case MentionableType.Channel:
                pattern = r"<#(\d+)>"
            case MentionableType.Emoji:
                pattern = r"<a?:\w+:(\d+)>"
            case _:
                raise ValueError(f"Invalid MentionableType: {_type}")

        response = await interaction.respond(embed=prompt)

        def check(m):
            return (
                m.author == interaction.user
                and (x := re.match(pattern, m.content))
            ) or m.content.lower() == "cancel"

        try:
            message = await interaction.client.wait_for("message", check=check, timeout=180)
        except TimeoutError:
            embed = Utilities.make_embed(
                title="Timeout",
                description=(
                    "You took too long to respond. Please try again."
                ),
                color=CustomColor.brand_red()
            )
            await response.respond(embed=embed)
            return

        error = Utilities.make_embed(
            title="Invalid Mention",
            description="You did not provide a valid mention. Please try again.",
            color=CustomColor.brand_red()
        )

        if message.content.lower() == "cancel":
            return

        results = re.match(pattern, message.content)
        if not results:
            await interaction.respond(embed=error)
            return

        mentionable_id = int(results.group(1))
        guild: GuildData = interaction.client[interaction.guild_id]  # type: ignore

        match _type:
            case MentionableType.User:
                mentionable = await guild.get_or_fetch_member_or_user(mentionable_id)
            case MentionableType.Channel:
                mentionable = await guild.get_or_fetch_channel(mentionable_id)
            case MentionableType.Role:
                mentionable = await guild.get_or_fetch_role(mentionable_id)
            case MentionableType.Emoji:
                mentionable = await guild.get_or_fetch_emoji(mentionable_id)
            case _:
                raise ValueError(f"Invalid MentionableType: {_type}")

        if not mentionable:
            await interaction.respond(embed=error)
            return

        try:
            await message.delete()
        except NotFound:
            pass

        try:
            await response.delete_original_response()
        except NotFound:
            pass

        return mentionable

################################################################################
    @staticmethod
    def shorten_url(long_url: str) -> Optional[str]:
        
        load_dotenv()
        
        key = os.getenv("CUTTLY_API_KEY")
        r = requests.get("https://cutt.ly/api/api.php?key={}&short={}".format(key, long_url))
        
        return r.json()["url"]["shortLink"] if r.json()["url"]["status"] == 7 else None
        
################################################################################
    @staticmethod
    def string_clamp(text: str, length: int) -> str:
        
        return text[:length] + "..." if len(text) > length else text
    
################################################################################
    @staticmethod
    def compare_datetimes(dt1: Optional[datetime], dt2: Optional[datetime]) -> int:
        """
        Compare two Optional[datetime] objects, handling tz-aware and naive datetimes.
        
        Args:
            dt1: First datetime object, may be None.
            dt2: Second datetime object, may be None.
        
        Returns:
            -1 if dt1 < dt2
             0 if dt1 == dt2
             1 if dt1 > dt2
        """
        
        print("Comparing datetimes...")
        
        def make_tz_aware(dt: Optional[datetime]) -> Optional[datetime]:
            if dt is None:
                return None
            if dt.tzinfo is None:
                # Assuming naive datetime is in local timezone, convert it to UTC
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.astimezone(timezone.utc)

        dt1_aware = make_tz_aware(dt1)
        dt2_aware = make_tz_aware(dt2)
        
        print(f"dt1_aware: {dt1_aware}")
        print(f"dt2_aware: {dt2_aware}")

        if dt1_aware is None and dt2_aware is None:
            print("Both datetimes are None.")
            return 0
        if dt1_aware is None:
            print("First datetime is None.")
            return -1
        if dt2_aware is None:
            print("Second datetime is None.")
            return 1

        if dt1_aware < dt2_aware:
            print("First datetime is earlier.")
            return -1
        elif dt1_aware > dt2_aware:
            print("First datetime is later.")
            return 1
        else:
            print("Datetimes are equal.")
            return 0
        
################################################################################
        