from typing import TYPE_CHECKING

from discord import (
    ApplicationContext,
    Cog,
    SlashCommandGroup,
    Option,
    SlashCommandOptionType,
)

if TYPE_CHECKING:
    from Classes.Bot import StaffPartyBot
################################################################################
class Admin(Cog):

    def __init__(self, bot: "StaffPartyBot"):

        self.bot: "StaffPartyBot" = bot

################################################################################

    admin = SlashCommandGroup(
        name="admin",
        description="Administrator commands for user/system configuration & management.",
        guild_only=True
    )

################################################################################
    @admin.command(
        name="user_status",
        description="View and edit the trainer/trainee profile & status of a user."
    )
    async def user_status(
        self,
        ctx: ApplicationContext,
        user: Option(
            SlashCommandOptionType.user,
            name="user",
            description="The user whose trainer record to view.",
            required=True
        )
    ) -> None:

        guild = self.bot[ctx.guild_id]
        await guild.training_manager.tuser_admin_status(ctx.interaction, user)
        
################################################################################
    @admin.command(
        name="post_signup",
        description="Post the trainer signup message."
    )
    async def post_signup_message(
        self,
        ctx: ApplicationContext,
        channel: Option(
            SlashCommandOptionType.channel,
            name="channel",
            description="The channel to set as the trainer signup message channel.",
            required=True
        )
    ) -> None:

        guild = self.bot[ctx.guild_id]
        await guild.training_manager.post_signup_message(ctx.interaction, channel)

################################################################################
    @admin.command(
        name="add_venue",
        description="Add a new venue to the system."
    )
    async def add_venue(
        self,
        ctx: ApplicationContext,
        name: Option(
            SlashCommandOptionType.string,
            name="name",
            description="The name of the venue.",
            required=True
        ),
        user: Option(
            SlashCommandOptionType.user,
            name="user",
            description="The initial user to add to the venue's authorized user list.",
            required=True
        )
    ) -> None:

        guild = self.bot[ctx.guild_id]
        await guild.venue_manager.add_venue(ctx.interaction, name, user)
        
################################################################################
    @admin.command(
        name="add_venue_user",
        description="Add a user as a venue's owner or authorized user."
    )
    async def add_venue_user(
        self,
        ctx: ApplicationContext,
        venue: Option(
            SlashCommandOptionType.string,
            name="venue",
            description="The name of the venue.",
            required=True
        ),
        user: Option(
            SlashCommandOptionType.user,
            name="user",
            description="The user to add to the venue's authorized user list.",
            required=True
        )
    ) -> None:

        guild = self.bot[ctx.guild_id]
        await guild.venue_manager.add_user(ctx.interaction, venue, user, True)
        
################################################################################
    @admin.command(
        name="remove_venue_user",
        description="Remove a user as a venue's owner or authorized user."
    )
    async def remove_venue_user(
        self,
        ctx: ApplicationContext,
        venue: Option(
            SlashCommandOptionType.string,
            name="venue",
            description="The name of the venue.",
            required=True
        ),
        user: Option(
            SlashCommandOptionType.user,
            name="user",
            description="The user to remove from the venue's authorized user list.",
            required=True
        )
    ) -> None:

        guild = self.bot[ctx.guild_id]
        await guild.venue_manager.remove_user(ctx.interaction, venue, user)
        
################################################################################
    @admin.command(
        name="venue_profile",
        description="View and edit a venue's internship profile & status."
    )
    async def venue_profile(
        self,
        ctx: ApplicationContext,
        name: Option(
            SlashCommandOptionType.string,
            name="name",
            description="The name of the venue.",
            required=True
        )
    ) -> None:

        guild = self.bot[ctx.guild_id]
        await guild.venue_manager.venue_menu(ctx.interaction, name, admin=True)
        
################################################################################
    @admin.command(
        name="yeet_venue",
        description="Remove a venue from the system."
    )
    async def yeet_venue(
        self,
        ctx: ApplicationContext,
        name: Option(
            SlashCommandOptionType.string,
            name="name",
            description="The name of the venue to remove.",
            required=True
        )
    ) -> None:

        guild = self.bot[ctx.guild_id]
        await guild.venue_manager.remove_venue(ctx.interaction, name)
        
################################################################################
    @admin.command(
        name="reports",
        description="Generate reports for various system data."
    )
    async def report_menu(self, ctx: ApplicationContext) -> None:

        await self.bot[ctx.guild_id].report_menu(ctx.interaction)
        
################################################################################
    @admin.command(
        name="roles",
        description="View the status of important roles."
    )
    async def roles_status(self, ctx: ApplicationContext) -> None:

        await self.bot[ctx.guild_id].role_manager.menu(ctx.interaction)
        
################################################################################
    @admin.command(
        name="channels",
        description="View the status of important channels."
    )
    async def channels_status(self, ctx: ApplicationContext) -> None:

        await self.bot[ctx.guild_id].channel_manager.menu(ctx.interaction)
        
################################################################################
    @admin.command(
        name="staff_experience",
        description="View a previously submitted staff background check."
    )
    async def staff_experience(
        self,
        ctx: ApplicationContext,
        user: Option(
            SlashCommandOptionType.user,
            name="user",
            description="The user to view the background check for.",
            required=True
        )
    ) -> None:

        guild = self.bot[ctx.guild_id]
        await guild.training_manager.staff_experience(ctx.interaction, user)
    
################################################################################
    @admin.command(
        name="settle_trainer",
        description="Settle a trainer's training paycheck."
    )
    async def settle_trainer(
        self,
        ctx: ApplicationContext,
        user: Option(
            SlashCommandOptionType.user,
            name="user",
            description="The user to settle the paycheck for.",
            required=True
        )
    ) -> None:

        guild = self.bot[ctx.guild_id]
        await guild.training_manager.settle_trainer(ctx.interaction, user)
        
################################################################################
    @admin.command(
        name="trainer_workload",
        description="Manage a trainer's training assignments."
    )
    async def trainer_workload(
        self,
        ctx: ApplicationContext,
        user: Option(
            SlashCommandOptionType.user,
            name="user",
            description="The user to manage training assignments for.",
            required=True
        )
    ) -> None:

        guild = self.bot[ctx.guild_id]
        await guild.training_manager.trainer_management(ctx.interaction, user)

################################################################################
    @admin.command(
        name="roles_report",
        description="Generate a report of selected roles applied to all members in the server."
    )
    async def roles_report(
        self, 
        ctx: ApplicationContext,
        r1: Option(
            SlashCommandOptionType.role,
            name="role1",
            description="Report role #1",
            required=True
        ),
        r2: Option(
            SlashCommandOptionType.role,
            name="role2",
            description="Report role #2",
            required=False
        ),
        r3: Option(
            SlashCommandOptionType.role,
            name="role3",
            description="Report role #3",
            required=False
        ),
        r4: Option(
            SlashCommandOptionType.role,
            name="role4",
            description="Report role #4",
            required=False
        ),
        r5: Option(
            SlashCommandOptionType.role,
            name="role5",
            description="Report role #5",
            required=False
        ),
        r6: Option(
            SlashCommandOptionType.role,
            name="role6",
            description="Report role #6",
            required=False
        ),
        r7: Option(
            SlashCommandOptionType.role,
            name="role7",
            description="Report role #7",
            required=False
        ),
        r8: Option(
            SlashCommandOptionType.role,
            name="role8",
            description="Report role #8",
            required=False
        ),
        r9: Option(
            SlashCommandOptionType.role,
            name="role9",
            description="Report role #9",
            required=False
        ),
    ) -> None:

        await self.bot.report_manager.roles_report(
            ctx.interaction, ctx.guild.members,
            [r for r in [r1, r2, r3, r4, r5, r6, r7, r8, r9] if r]
        )
                          
################################################################################
    @admin.command(
        name="bulk_update",
        description="Bulk update various bot postings."
    )
    async def bulk_update(self, ctx: ApplicationContext) -> None:

        await self.bot[ctx.guild_id].bulk_update_menu(ctx.interaction)
        
################################################################################          
def setup(bot: "StaffPartyBot") -> None:

    bot.add_cog(Admin(bot))

################################################################################
