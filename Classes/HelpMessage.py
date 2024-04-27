from __future__ import annotations

from typing import TYPE_CHECKING, List
from discord import Interaction, Embed, EmbedField
from discord.ext.pages import Page, PageGroup

from UI.Common import Frogginator

if TYPE_CHECKING:
    from Classes import StaffPartyBot
################################################################################

__all__ = ("HelpMessage",)

################################################################################
class HelpMessage:
    
    __slots__ = (
        "_state",
    )
    
################################################################################
    def __init__(self, bot: StaffPartyBot):
        
        self._state: StaffPartyBot = bot
    
################################################################################
    async def menu(self, interaction: Interaction) -> None:
        
        page_groups = self._prepare_page_groups()
        frogginator = Frogginator(
            pages=page_groups,
            show_menu=True,
            menu_placeholder="Select your situation to get more info..."
        )
        await frogginator.respond(interaction)
        
################################################################################
    def _prepare_page_groups(self) -> List[PageGroup]:
        
        return [
            PageGroup(
                label="Start Here",
                pages=[
                    self._welcome_page()
                ]
            ),
            PageGroup(
                label="I Am a Venue Manager",
                description="I am a venue manager looking for staff.",
                pages=[
                    self.venue_manager_start(),
                    self.venue_manager_page1(),
                    self.venue_manager_page2(),
                    self.venue_manager_page3(),
                    self.venue_manager_page4(),
                    self.venue_manager_page5(),
                    self.venue_manager_page7(),
                    self.venue_manager_page6(),
                ]
            ),
            PageGroup(
                label="I am Staff",
                description="I am a staff member looking for work.",
                pages=[
                    self.staff_member_start(),
                    self.staff_member_page1(),
                    self.staff_member_page2(),
                    self.staff_member_page3(),
                    self.staff_member_page4(),
                    self.staff_member_page5(),
                    self.staff_member_page6(),
                ]
            ),
            PageGroup(
                label="I am a Trainer",
                description="I am a trainer looking to train staff.",
                pages=[
                    self.trainer_start(),
                    self.trainer_page1(),
                    self.trainer_page2(),
                    self.trainer_page3(),
                    self.trainer_page4(),
                    self.trainer_page5(),
                    self.trainer_page6(),
                    self.trainer_page7(),
                    self.trainer_page8(),
                    self.trainer_page9(),
                ]
            ),
            PageGroup(
                label="I am a Trainee",
                description="I am new and looking for training.",
                pages=[
                    self.trainee_start(),
                    self.trainee_page1(),
                    self.trainee_page2(),
                    self.trainee_page3(),
                    self.trainee_page4(),
                ]
            )
        ]
    
################################################################################
    @staticmethod
    def _welcome_page() -> Page:
        
        embed = Embed(
            title="__Welcome to the Staff Party Bus!__",
            description=(
                "The purpose of this server is to provide **fill-in staff** "
                "to venues who might experience a last minute shortage.\n\n"
                
                "It also offers staff a wide range of venue experience "
                "and resources:\n\n"
                
                "* **Training** - __Learn new skills and improve existing ones.__\n"
                "*We offer a complete training to new staff including a "
                "venue etiquette guide.*\n\n"
                
                "* **BG Check** - __All staff members are cleared.__\n"
                "*We require all staff and trainers to complete a (short) "
                "background check before they can work with us.*\n\n"
                
                "Select your situation from the menu below to get more information."
            )
        )
        
        return Page(embeds=[embed])
    
################################################################################
    @staticmethod
    def venue_manager_start() -> Page:

        embed = Embed(
            title="__Help! I'm a Venue Manager and I Need Staff!__",
            description=(
                "The following pages contain information on the these topics:\n\n"
                
                "* **How to Create Your Venue Profile**\n"
                "* **What if Import Isn't Working?**\n"
                "* **Updating Profile Information**\n"
                "* **Adding a Manager to Your Venue**\n"
                "* **How to Post a Job Offer**\n"
                "* **Muting Job Offers for Selected Staff**\n\n"
                
                "Click the arrow buttons below to navigate through the pages."
            )
        )

        return Page(embeds=[embed])
    
################################################################################
    @staticmethod
    def venue_manager_page1() -> Page:

        embed = Embed(
            title="__How do I create my venue profile?__",
            description=(
                "Venue profile creation in Staff Party Bus is a simple process.\n"
                "Just follow these steps:\n\n"
                
                "1. **List your venue with FFXIV Venues**\n"
                "> Our venue profiles process partners with and relies heavily "
                "on FFXIV Venues. You'll need to create a venue there before "
                "you can make one with us. Check it out at "
                "https://discord.com/channels/1104515062187708525/1158618747356065902\n\n"
                
                "2. **Import your venue with </venue import:1218699777156317185>**\n"
                "> Once you've created your venue on FFXIV Venues, you can "
                "import it into Staff Party Bus. This will automatically "
                "populate your venue profile with the information you've "
                "already provided.\n\n"
                
                "3. **Review and update with </venue profile:1218699777156317185> command**\n"
                "> After importing your venue, you'll need to review the "
                "information as well as update a few items unique to your venue "
                "with us. (There are buttons indicating what you can edit.)\n\n"
                
                "4. **Post your venue profile**\n"
                "> Once you're satisfied with your venue profile, you can post "
                "it to the venue listings channel **using the button on your venue "
                "profile dashboard** (from the previous step). This will allow "
                "staff to see your venue and apply for internships post-training."
                
            )
        )

        return Page(embeds=[embed])

################################################################################
    @staticmethod
    def venue_manager_page2() -> Page:

        embed = Embed(
            title="__Import isn't working for my venue! What do I do?__",
            description=(
                "If you're having trouble importing your venue, there are a "
                "few things you can try to fix the issue:\n\n"
                
                "1. **Check your venue on FFXIV Venues**\n"
                "> Make sure your venue is registered with FFXIV Venues and that "
                "you've been approved.\n\n"
                
                "2. **Check your venue name**\n"
                "> Make sure you're using the correct venue name when importing "
                "your venue. This must be **the exact name used on your FFXIV "
                "Venues listing.** (Copy/Paste recommended!)\n\n"
                
                "3. **Check your permissions**\n"
                "> Make sure your discord user is associated with the venue "
                "on FFXIV Venues as a manager. If you cannot make administrative "
                "updates to your venue on their platform, you'll be unable to "
                "import/make updates in Staff Party Bus\n\n"
                
                "If none of these steps work, you can contact a server "
                "administrator for further assistance."
            )
        )

        return Page(embeds=[embed])

################################################################################
    @staticmethod
    def venue_manager_page3() -> Page:

        embed = Embed(
            title="__How do I update my venue's profile/information__",
            description=(
                "Updating your venue's profile is a simple process.\n"
                "Just follow these steps:\n\n"
                
                "1. **Update your profile on FFXIV Venues**\n"
                "> If you need to make changes to venue information governed by "
                "FFXIV Venues, you'll need to make those changes on their platform"
                "first.\n\n"
                
                "2. **Use the </venue profile:1218699777156317185> command**\n"
                "> This command will display your venue profile dashboard. "
                "From here, you can make changes to your venue's other information "
                "such as the RP Level, hiring status, and staff application URL.\n\n"
                
                "3. **Use the button on your dashboard to update**\n"
                "> Once you're satisfied with your changes, you can post your "
                "updated venue profile using the \"Post/Update Profile\" button. "
                "on your dashboard (from the previous step). This will update your "
                "existing venue profile in the venue listings channel."
            )
        )

        return Page(embeds=[embed])

################################################################################
    @staticmethod
    def venue_manager_page4() -> Page:

        embed = Embed(
            title="__How do I add a manager to my venue?__",
            description=(
                "Adding a manager to your venue is pretty straightforward.\n\n"

                "**Update your profile on FFXIV Venues**\n"
                "> Managers for Staff Party bus profiles are part of the "
                "information governed by FFXIV Venues, you'll need to make "
                "those changes on their platform first by asking our close friend "
                "Veni Ki to add a manager! Then simply return here and run "
                "an update. (See previous page!)\n\n"
            )
        )

        return Page(embeds=[embed])

################################################################################
    @staticmethod
    def venue_manager_page5() -> Page:

        embed = Embed(
            title="__How do I post a job offer?__",
            description=(
                "Posting a job offer is a simple process.\n\n"
                
                "1. **Import your venue by using </venue import:1218699777156317185>**\n"
                "> Follow the steps on the appropriate page of this help message "
                "to import your venue. Dont forget to post it when complete!\n\n"
                
                "2. **Use the </jobs create_post:1221244262499221606> command**\n"
                "> This command will display message allowing you to customize the "
                "job offer you're posting. You can include information such as the "
                "job type, description, and pay amount. **Remember: shifts must be "
                "a minimum of two (2) hours.**\n\n"
                
                "3. **Post the job offer**\n"
                "> Once you're satisfied with your job offer, you can post it to the "
                "job listings channel **using the button on your job offer dashboard** "
                "(from the previous step). This will allow staff to see your job offer "
                "and apply for it."
            )
        )

        return Page(embeds=[embed])

################################################################################
    @staticmethod
    def venue_manager_page6() -> Page:

        embed = Embed(
            title="__I don't want my job offers appearing for certain staff!__",
            description=(
                "Muting job offers for selected staff is as easy as a button "
                "click.\n\n"
                
                "1. **Navigate to the <#1224161402734772275> channel**\n"
                "> This channel contains all of our staff members' profiles. "
                "You can easily locate a given staff member by using the search "
                "function in the forum channel.\n\n"
                
                "2. **Click the '`Mute`' button on that staff member's profile**\n"
                "> This will prevent job offers from being sent to that staff "
                "member. They will still be able to see job offers in the job "
                "listings channel, but they will not receive a notification when "
                "a new job is posted."
            )
        )

        return Page(embeds=[embed])

################################################################################
    @staticmethod
    def venue_manager_page7() -> Page:

        embed = Embed(
            title="__How do I edit/cancel my job posting?__",
            description=(
                "Editing or canceling a job posting is a simple process.\n\n"
                
                "1. **Locate your job posting and copy the ID**\n"
                "> You can find the ID of your job posting at the bottom of the "
                "job posting message. Copy this ID to use in the next step.\n\n"
                
                "2. **Use the </jobs post_status:1221244262499221606> with the job ID**\n"
                "> This command will display a message with buttons allowing you to "
                "edit or cancel your job posting. You can change the job type, "
                "description, and pay amount, or cancel the job posting entirely."
            )
        )

        return Page(embeds=[embed])

################################################################################
    @staticmethod
    def staff_member_start() -> Page:

        embed = Embed(
            title="__I'm a Staff Member Looking for Work!__",
            description=(
                "The following pages contain information on these topics:\n\n"

                "* **How to obtain the <@&1104515062187708529> role?**\n"
                "* **How do I create my staff profile?**\n"
                "* **I'm having trouble posting my profile.**\n"
                "* **How do I get jobs?**\n"
                "* **Muting Job Offers from selected venues.**\n"
                "* **I have no RP work experience!**\n\n"

                "Click the arrow buttons below to navigate through the pages."
            )
        )

        return Page(embeds=[embed])

################################################################################
    @staticmethod
    def staff_member_page1() -> Page:

        embed = Embed(
            title="__How do I become a proper 'Staff Member' in SPB?__",
            description=(
                "Becoming staff in Staff Party Bus required you first complete a "
                "*VERY* short background check outlining your work experience.\n\n"

                "1. **Use the </bg_check:1224431692790628545> command**\n"
                "> This command will display a message with some buttons allowing "
                "you to complete the background check process. This is a simple "
                "process that requires only a few clicks and answers.\n\n"
                
                "2. **Wait...**\n"
                "> Once you've completed the background check, you'll need to wait "
                "for a server administrator to review your information. This "
                "usually takes only a few minutes.\n\n"
                
                "3 **You'll get a DM when you're approved!**\n"
                "> Once you're approved, you'll receive a DM from the Staff Party Bus "
                "bot indicating that you're now able to create your staff profile.\n\n"
                
                "**Remember, the goal of Staff Party Bus is to provide reliable and "
                "professional staff to venues in need, and the BG check is a part of "
                "that process.**"
            )
        )

        return Page(embeds=[embed])

################################################################################
    @staticmethod
    def staff_member_page2() -> Page:

        embed = Embed(
            title="__How do I create my staff profile?__",
            description=(
                "Creating your staff profile is a simple process.\n\n"

                "1. **Use the </staffing profile:1226227239155138600> command**\n"
                "> This command will display a message with some buttons allowing "
                "you to complete the staff profile creation process. This is a simple "
                "process that requires only a few clicks and answers.\n\n"
                
                "2. **Ensure you complete all the required information!**\n"
                "> The staff profile creation process requires you to provide some "
                "basic information about yourself, including your **home region(s)**, "
                "**work availability**, **employable positions**, and **character name.**\n\n"
                
                "3. **Post your profile (This is important!)**\n"
                "> Once you're satisfied with your staff profile, you can post it to the "
                "staff listings channel **using the button on your staff profile dashboard** "
                "(from the previous steps). This will allow venues to see your profile and "
                "offer you work.\n\n"
                
                "__**Hey, my image isn't uploading!**__\n"
                "> If you're having trouble uploading your image, make sure it's of "
                "the correct format. We only accept **WEBP**, **GIF**, **PNG** "
                "and **JPEG** files. "
                
                "__**Hey my profile isn't posting!**__\n"
                "> If you're having trouble posting your profile, make sure you've "
                "completed all the following required sections:\n"
                "> * **Home Region(s)**\n"
                "> * **Work Availability**\n"
                "> * **Employable Positions**\n"
                "> * **Character Name**\n"
                "> If you're still having trouble, contact a server administrator."
            )
        )

        return Page(embeds=[embed])

################################################################################
    @staticmethod
    def staff_member_page3() -> Page:

        embed = Embed(
            title="__It won't let me post my profile!__",
            description=(
                "Not a problem, just ensure you've completed all the required sections.\n\n"

                "**Ensure you complete all the required information!**\n"
                "> The staff profile creation process requires you to provide some "
                "basic information about yourself:\n"
                "> * **Home Region(s)**\n"
                "> * **Work Availability**\n"
                "> * **Employable Positions**\n"
                "> * **Character Name**\n"
                "> If you're still having trouble, contact a server administrator."
            )
        )

        return Page(embeds=[embed])

################################################################################
    @staticmethod
    def staff_member_page4() -> Page:

        embed = Embed(
            title="__How do I get jobs?__",
            description=(
                "Getting jobs in Staff Party Bus is a simple process.\n\n"

                "The Staff Party Bus bot will automatically send you a DM when a "
                "job offer is posted that matches your profile. You can also view "
                "job offers in the job listings channel.\n\n"
                
                "(If you're not receiving DMs, you can check your profile to ensure "
                "you've set your availability and employable positions correctly.)\n\n"
                
                "You can also view job offers in the job listings channel. "
                "https://discord.com/channels/1104515062187708525/1224185349924978808 If you "
                "see a job offer you like, you can apply for it by clicking the "
                "button on the job offer message.\n\n"
                
                "**I don't want to receive DMs anymore.**\n"
                "> If you no longer want to receive DMs when job offers are posted, "
                "you can use the '`Hiatus`' button on your </staffing profile:1226227239155138600> "
                "dashboard. This will prevent the bot from sending you DMs until you "
                "reactivate your profile."
            )
        )

        return Page(embeds=[embed])

################################################################################
    @staticmethod
    def staff_member_page5() -> Page:

        embed = Embed(
            title="__I don't want to receive DMs from certain venue(s)__",
            description=(
                "Muting job offers from selected venues is as easy as a button click.\n\n"

                "1. **Navigate to the <#1222976936360415303> channel**\n"
                "> This channel contains all of our venue profiles. You can easily "
                "locate a given venue by using the search function in the forum channel.\n\n"
                
                "2. **Click the '`Mute`' button on that venue's profile**\n"
                "> This will prevent job offers from that venue from being sent to you. "
                "You will still be able to see job offers in the job listings channel, "
                "but you will not receive a notification when a new job is posted."
            )
        )

        return Page(embeds=[embed])

################################################################################
    @staticmethod
    def staff_member_page6() -> Page:

        embed = Embed(
            title="__I have no work experience, but still want jobs!__",
            description=(
                "No problem! We have a training program that will help you get the "
                "experience you need to work in the venues we support.\n\n"

                "Just head over to <#1104515062636478638> and get the "
                "<@&1104515062187708530> role. This will give you access to the "
                "training program and allow you to apply for internships post-training."
                
                "For more information, see the relevant section in this help message!"
            )
        )

        return Page(embeds=[embed])

################################################################################
    @staticmethod
    def trainer_start() -> Page:

        embed = Embed(
            title="__I want to become a Trainer!__",
            description=(
                "The following pages contain information on these topics:\n\n"

                "* **How to obtain the <@&1104515062187708527> role?**\n"
                "* **How do I create my trainer profile?**\n"
                "* **I'm having trouble completing my profile.**\n"
                "* **How do I know when there are new trainees available?**\n"
                "* **Can I check a trainee's availability before accepting?**\n"
                "* **Where do I check on existing trainings I've picked up?**\n"
                "* **Where do I see my pay?**\n"
                "* **Is there a quick way to check a position's requirements?**\n"
                "* **I want to go on hiatus from training.**\n\n"

                "Click the arrow buttons below to navigate through the pages."
            )
        )

        return Page(embeds=[embed])

################################################################################
    @staticmethod
    def trainer_page1() -> Page:

        embed = Embed(
            title="__How to obtain the `Trainer` role?__",
            description=(
                "Becoming a trainer in Staff Party Bus requires you first complete a "
                "*VERY* short background check outlining your work experience.\n\n"

                "1. **Use the </bg_check:1224431692790628545> command**\n"
                "> This command will display a message with some buttons allowing "
                "you to complete the background check process. This is a simple "
                "process that requires only a few clicks and answers.\n\n"
                
                "1a. **Click the `I Want to Train Staff` button**\n"
                "> This will flag your profile as a trainer and allow you to pick up "
                "trainings.\n\n"

                "2. **Wait...**\n"
                "> Once you've completed the background check, you'll need to wait "
                "for a server administrator to review your information. This "
                "usually takes only a few minutes.\n\n"
                
                "3 **You'll get a DM when you're approved!**\n"
                "> Once you're approved, you'll receive a DM from the Staff Party Bus "
                "bot indicating that you're now able to create your trainer profile.\n\n"

                "**Remember, the goal of Staff Party Bus is to provide reliable and "
                "professional staff to venues in need, and the BG check is a part of "
                "that process.**"
            )
        )

        return Page(embeds=[embed])

################################################################################
    @staticmethod
    def trainer_page2() -> Page:

        embed = Embed(
            title="__How do I create my trainer profile?__",
            description=(
                "Creating your trainer profile is a simple process.\n\n"

                "1. **Use the </trainer profile:1215157989372338191> command**\n"
                "> This command will display a message with some buttons allowing "
                "you to complete the trainer profile setup process. This is a simple "
                "process that requires only a few clicks and answers.\n\n"

                "2. **Ensure you complete all the required information!**\n"
                "> The trainer profile creation process requires you to provide some "
                "basic information about yourself:\n"
                "> * **Home Region(s)**\n"
                "> * **Work Availability**\n"
                "> * **Employable Positions**\n"
                "> * **Character Name**\n"
            )
        )

        return Page(embeds=[embed])

################################################################################
    @staticmethod
    def trainer_page3() -> Page:

        embed = Embed(
            title="__It won't let me post my profile!__",
            description=(
                "Not a problem, just ensure you've completed all the required sections.\n\n"

                "**Ensure you complete all the required information!**\n"
                "> The trainer profile creation process requires you to provide some "
                "basic information about yourself:\n"
                "> * **Home Region(s)**\n"
                "> * **Work Availability**\n"
                "> * **Employable Positions**\n"
                "> * **Character Name**\n"
                "> If you're still having trouble, contact a server administrator."
            )
        )

        return Page(embeds=[embed])

################################################################################
    @staticmethod
    def trainer_page4() -> Page:

        embed = Embed(
            title="__How do I know when there are new trainees available?__",
            description=(
                "The Staff Party Bus bot will automatically send you a DM when a "
                "trainee that matches your availability and home region(s) is "
                "available for training. You can also view trainees available "
                "for picking up in the <#1215371208661667951> channel.\n\n"

                "(If you're not receiving DMs, you can check your profile to ensure "
                "you've set your availability and employable positions correctly.)\n\n"
            )
        )

        return Page(embeds=[embed])

################################################################################
    @staticmethod
    def trainer_page5() -> Page:

        embed = Embed(
            title="__Can I check a trainee's availability before accepting?__",
            description=(
                "Yes! You can check a trainee's availability before accepting a "
                "training. Just use the </trainer trainee_profile:1215157989372338191> "
                "command to view their profile, availability, and employable positions."
            )
        )

        return Page(embeds=[embed])

################################################################################
    @staticmethod
    def trainer_page6() -> Page:

        embed = Embed(
            title="__Where do I check on/complete trainings I've picked up?__",
            description=(
                "You can view all the trainings you've picked up by running the "
                "</trainer dashboard:1215157989372338191> command. This will display "
                "a message with buttons allowing you to view and complete your "
                "current trainings. "
                
                "Each requirement will need to be marked as `complete` before the "
                "training is considered finished. Once all requirements are marked "
                "as complete, the trainee will receive a DM indicating that their "
                "training is finished and it will be moved off your roster."
            )
        )

        return Page(embeds=[embed])

################################################################################
    @staticmethod
    def trainer_page7() -> Page:

        embed = Embed(
            title="__Where do I see my pay?__",
            description=(
                "You can view your pay by running the </trainer profile:1215157989372338191> "
                "command. This message will display your current unpaid balance "
                "in the lower-right corner."
            )
        )

        return Page(embeds=[embed])

################################################################################
    @staticmethod
    def trainer_page8() -> Page:

        embed = Embed(
            title="__Is there a quick way to check a position's requirements?__",
            description=(
                "Yes! You can check a position's requirements by running the "
                "</trainer position_info:1215157989372338191> command. This will "
                "display a message with the requirements all positions."
            )
        )

        return Page(embeds=[embed])

################################################################################
    @staticmethod
    def trainer_page9() -> Page:

        embed = Embed(
            title="__I want to go on hiatus from training.__",
            description=(
                "If you no longer want to receive DMs when trainees are available, "
                "you can use the '`Hiatus`' button on your </trainer profile:1215157989372338191> "
                "dashboard. This will prevent the bot from sending you DMs until you "
                "reactivate your profile."
            )
        )

        return Page(embeds=[embed])

################################################################################
    @staticmethod
    def trainee_start() -> Page:

        embed = Embed(
            title="__I'm new to one or more venue positions and want training!__",
            description=(
                "The following pages contain information on these topics:\n\n"

                "* **How do I get training?**\n"
                "* **How do I know if a trainer has picked me?**\n"
                "* **What exactly does 'training' entail?**\n"
                "* **What happens after my training?**\n\n"

                "Click the arrow buttons below to navigate through the pages."
            )
        )

        return Page(embeds=[embed])

################################################################################
    @staticmethod
    def trainee_page1() -> Page:

        embed = Embed(
            title="__How do I get training?__",
            description=(
                "Getting started with training in Staff Party Bus is a simple process.\n\n"

                "1. **Use the </trainee profile:1215157989372338191> command**\n"
                "> This command will display a message with some buttons allowing "
                "you to complete the staff profile creation process. This is a simple "
                "process that requires only a few clicks and answers.\n\n"

                "2. **Ensure you complete all the required information!**\n"
                "> The staff profile creation process requires you to provide some "
                "basic information about yourself:\n"
                "> * **Home Region(s)**\n"
                "> * **Work Availability**\n"
                "> * **Employable Positions**\n"
                "> * **Character Name**\n"
                
                "3. **Prepare for training!**\n"
                "> Once you've completed your profile, you can prepare for training. "
                "This includes reading the venue </etiquette:1231774050150514759> guide "
                "and reading on the general position description by using the "
                "</trainee position_info:1220098774312026124> command.\n\n"
                
                "4. **Wait for a trainer to pick you up!**\n"
                "> Once you've completed your profile and are ready for training, you "
                "can wait for a trainer to pick you up. You'll receive a DM when a "
                "trainer has selected you for training."
            )
        )

        return Page(embeds=[embed])

################################################################################
    @staticmethod
    def trainee_page2() -> Page:

        embed = Embed(
            title="__How do I know if a trainer has picked me?__",
            description=(
                "You'll receive a DM from the Staff Party Bus bot when a trainer "
                "has selected you for training. The trainer will contact you "
                "via DMs shortly thereafter! You can also view trainings you've "
                "been picked up for by using the </trainee profile:1215157989372338191> "
                "command."
            )
        )

        return Page(embeds=[embed])

################################################################################
    @staticmethod
    def trainee_page3() -> Page:

        embed = Embed(
            title="__What exactly does 'training' entail?__",
            description=(
                "Training in Staff Party Bus is a simple process that involves "
                "working with a trainer to learn the ropes of a given position.\n\n"

                "1. **Read the venue etiquette guide**\n"
                "> Before your training, you should read the venue "
                "</etiquette:1231774050150514759> guide. This will give you an idea of "
                "what to expect from the venue community.\n\n"

                "2. **Talk to your trainer**\n"
                "> After selecting you, your trainer will send a DM to you to discuss "
                "your training. This primarily involves setting a time and place to complete "
                "the training.\n\n"

                "3. **Work with your trainer**\n"
                "> During your training, you'll work with your trainer to learn the "
                "ropes of the position. This may involve shadowing them during a "
                "shift or working alongside them to complete tasks.\n\n"

                "4. **Complete your training**\n"
                "> Once your training is complete, your trainer will mark it as such "
                "and you'll receive a DM indicating that you're now able to apply "
                "for internships post-training."
            )
        )

        return Page(embeds=[embed])

################################################################################
    @staticmethod
    def trainee_page4() -> Page:

        embed = Embed(
            title="__What happens after my training?__",
            description=(
                "After your training is complete, you'll be able to apply for "
                "internships post-training. These are real shifts at real venues "
                "where you'll be able to put your new skills to the test.\n\n"

                "1. **Use the </staffing profile:1226227239155138600> command**\n"
                "> This command will display a message with some buttons allowing "
                "you to complete the staff profile creation process. This is a simple "
                "process that requires only a few clicks and answers.\n\n"
                
                "2. **Check what venues match your tastes**\n"
                "> Selecting a venue to intern at is a stressful process, the options "
                "are seemingly limitless! Don't worry, the </trainee match:1220096104008388689> "
                "command will help you narrow down your choices.\n"
                "*The purpose of the Trainee matching is to show you what venues "
                "offers on-site experience for a few shifts. __(This is not mandatory)__*"
            )
        )

        return Page(embeds=[embed])

################################################################################
