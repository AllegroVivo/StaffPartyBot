from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from .Branch import DBWorkerBranch

if TYPE_CHECKING:
    from Classes import *
################################################################################

__all__ = ("DatabaseUpdater",)

################################################################################
class DatabaseUpdater(DBWorkerBranch):
    """A utility class for updating records in the database."""

    def _update_log_channel(self, guild_id: int, channel_id: Optional[int]) -> None:
        
        self.execute(
            "UPDATE bot_config SET log_channel = %s WHERE guild_id = %s;",
            channel_id, guild_id
        )
    
################################################################################
    def _update_venue_post_channel(self, guild_id: int, channel_id: Optional[int]) -> None:
        
        self.execute(
            "UPDATE bot_config SET venue_post_channel = %s WHERE guild_id = %s;",
            channel_id, guild_id
        )
        
################################################################################
    def _update_position(self, position: Position) -> None:
        
        self.execute(
            "UPDATE positions SET name = %s, description = %s, linked_role = %s, "
            "trainer_pay = %s, follow_up = %s WHERE _id = %s;",
            position.name, position.description,
            position.linked_role.id if position.linked_role is not None else None, 
            position.trainer_pay, position.followup_included, position.id
        )
    
################################################################################
    def _update_requirement(self, requirement: Requirement) -> None:
        
        self.execute(
            "UPDATE requirements SET description = %s WHERE _id = %s;",
            requirement.description, requirement.id
        )
        
################################################################################        
    def _update_tuser_details(self, details: UserDetails) -> None:
        
        self.execute(
            "UPDATE tuser_details SET char_name = %s, notes = %s, hiatus = %s, "
            "data_centers = %s, guidelines = %s WHERE user_id = %s;",
            details.name, details.notes, details.hiatus, 
            [dc.value for dc in details.data_centers] if details.data_centers else None,
            details.guidelines_accepted, details.user_id
        )
        
################################################################################
    def _update_tuser_config(self, config: UserConfiguration) -> None:
        
        self.execute(
            "UPDATE tuser_config SET job_pings = %s WHERE user_id = %s;",
            config.trainee_pings, config.user_id
        )
        
################################################################################
    def _update_tuser(self, tuser: TUser) -> None:
        
        self.execute(
            "UPDATE tusers SET mute_list = %s WHERE user_id = %s AND guild_id = %s;",
            [v.id for v in tuser.muted_venues], tuser.user_id, tuser.guild_id
        )
        
################################################################################
    def _update_availability(self, availability: TAvailability) -> None:
        
        self.execute(
            "UPDATE availability SET start_time = %s, end_time = %s "
            "WHERE user_id = %s AND day = %s;",
            availability.start_time, availability.end_time,
            availability.user_id, availability.day.value
        )

################################################################################
    def _update_qualification(self, qualification: Qualification) -> None:      
    
        self.execute(
            "UPDATE qualifications SET level = %s WHERE _id = %s;",
            qualification.level.value, qualification.id
        )
        
################################################################################
    def _update_training(self, training: Training) -> None:
        
        self.execute(
            "UPDATE trainings SET trainer = %s, trainer_paid = %s, is_complete = %s "
            "WHERE _id = %s;",
            None if training.trainer is None else training.trainer.user_id,
            training.trainer_paid, training.is_complete, training.id
        )

        for requirement_id, level in training.requirement_overrides.items():
            self.execute(
                "SELECT * FROM requirement_overrides WHERE training_id = %s "
                "AND requirement_id = %s;",
                training.id, requirement_id
            )
            match = self.fetchone()

            if match:
                self.execute(
                    "UPDATE requirement_overrides SET level = %s "
                    "WHERE training_id = %s AND requirement_id = %s;",
                    level.value, training.id, requirement_id
                )
            else:
                self.execute(
                    "INSERT INTO requirement_overrides (user_id, guild_id, "
                    "training_id, requirement_id, level) "
                    "VALUES (%s, %s, %s, %s, %s);",
                    training.user_id, training.trainee.guild_id, 
                    training.id, requirement_id, level.value
                )
        
################################################################################
    def _update_signup_message(self, guild_id: int, message: SignUpMessage) -> None:
        
        self.execute(
            "UPDATE bot_config SET signup_msg_channel = %s, signup_msg_id = %s "
            "WHERE guild_id = %s;",
            message.channel.id if message.channel is not None else None,
            message.message.id if message.message is not None else None,
            guild_id
        )
        
################################################################################
    def _update_profile_details(self, details: ProfileDetails) -> None:
        
        self.execute(
            "UPDATE details SET char_name = %s, url = %s, color = %s, jobs = %s, "
            "rates = %s, post_url = %s, positions = %s, dm_preference = %s WHERE _id = %s;",
            details.name, details.url, 
            details.color.value if details.color is not None else None,
            details.jobs, details.rates, 
            details.post_message.jump_url if details.post_message else None,
            [p.id for p in details.positions], details.dm_preference,
            details.profile_id
        )
    
################################################################################    
    def _update_profile_ataglance(self, aag: ProfileAtAGlance) -> None:
        
        gender = race = clan = orientation = None
        if aag.gender is not None:
            gender = aag.gender if isinstance(aag.gender, str) else aag.gender.value
        if aag.race is not None:
            race = aag.race if isinstance(aag.race, str) else aag.race.value
        if aag.clan is not None:
            clan = aag.clan if isinstance(aag.clan, str) else aag.clan.value
        if aag.orientation is not None:
            orientation = (
                aag.orientation if isinstance(aag.orientation, str) 
                else aag.orientation.value
            )
        
        self.execute(
            "UPDATE ataglance SET gender = %s, pronouns = %s, race = %s, "
            "clan = %s, orientation = %s, height = %s, age = %s, mare = %s, "
            "data_centers = %s WHERE _id = %s;",
            gender, [p.value for p in aag.pronouns], race, clan, orientation,
            aag.height, aag.age, aag.mare, [dc.value for dc in aag.data_centers],
            aag.profile_id
        )
       
################################################################################ 
    def _update_profile_personality(self, personality: ProfilePersonality) -> None:
        
        self.execute(
            "UPDATE personality SET likes = %s, dislikes = %s, personality = %s, "
            "aboutme = %s WHERE _id = %s;",
            personality.likes, personality.dislikes, personality.personality,
            personality.aboutme, personality.profile_id
        )
        
################################################################################
    def _update_profile_images(self, images: ProfileImages) -> None:
        
        self.execute(
            "UPDATE images SET thumbnail = %s, main_image = %s WHERE _id = %s;",
            images.thumbnail, images.main_image, images.profile_id
        )
    
################################################################################        
    def _update_profile_additional_image(self, image: PAdditionalImage) -> None:
        
        self.execute(
            "UPDATE additional_images SET url = %s, caption = %s "
            "WHERE _id = %s;",
            image.url, image.caption, image.id
        )
    
################################################################################   
    def _update_venue_location(self, location: VenueLocation) -> None:
        
        self.execute(
            "UPDATE venue_locations SET data_center = %s, world = %s, "
            "zone = %s, ward = %s, plot = %s, apartment = %s, room = %s, "
            "subdivision = %s WHERE venue_id = %s;",
            location.data_center.value if location.data_center is not None else None,
            location.world.value if location.world is not None else None,
            location.zone.value if location.zone is not None else None,
            location.ward, location.plot, location.apartment, location.room,
            location.subdivision, location.venue_id
        )
      
################################################################################        
    def _update_venue_hours(self, hours: VenueHours) -> None:
        
        self.execute(
            "UPDATE venue_hours SET open_time = %s, close_time = %s, "
            "interval_type = %s, interval_arg = %s WHERE venue_id = %s AND weekday = %s;",
            hours.open_time, hours.close_time, hours.venue_id,
            hours.day.value, hours.interval_type.value, hours.interval_arg
        )
        
################################################################################
    def _update_venue(self, venue: Venue) -> None:
        
        self.execute(
            "UPDATE venues SET users = %s, positions = %s, pending = %s, "
            "post_url = %s, name = %s, description = %s, hiring = %s, "
            "mare_id = %s, mare_pass = %s, mute_list = %s, xivvenues_id = %s "
            "WHERE _id = %s;",
            [u.id for u in venue.authorized_users], [p.id for p in venue.positions],
            venue.pending, venue.post_url, venue.name, venue.description,
            venue.hiring, venue.mare_id, venue.mare_password,
            [u.id for u in venue.muted_users], venue._xiv_id, venue.id
        )
        
################################################################################
    def _update_venue_urls(self, urls: VenueURLs) -> None:
    
        self.execute(
            "UPDATE venue_urls SET discord_url = %s, website_url = %s, "
            "logo_url = %s, banner_url = %s, application_url = %s "
            "WHERE venue_id = %s;",
            urls["discord"], urls["website"], urls["logo"], urls["banner"],
            urls["app"], urls.venue_id
        )
        
################################################################################
    def _update_venue_aag(self, aag: VenueAtAGlance) -> None:
        
        self.execute(
            "UPDATE venue_aag SET level = %s, nsfw = %s, tags = %s "
            "WHERE venue_id = %s;",
            aag.level.value if aag.level is not None else None, aag.nsfw,
            [t.tag_text for t in aag.tags], aag.venue_id
        )
        
################################################################################
    def _update_job_hours(self, availability: JobHours) -> None:

        self.execute(
            "UPDATE job_hours SET start_time = %s, end_time = %s "
            "WHERE job_id = %s AND day = %s;",
            availability.start_time, availability.end_time,
            availability.job_id, availability.day.value
        )

################################################################################
    def _update_job_post(self, job: JobPosting) -> None:
        
        self.execute(
            "UPDATE job_postings SET post_type = %s, position = %s, "
            "description = %s, salary = %s, pay_frequency = %s, pay_details = %s, "
            "post_url = %s, start_time = %s, end_time = %s, candidate = %s, "
            "rejections = %s WHERE _id = %s;",
            job.post_type.value if job.post_type else None,
            job.position.id if job.position else None, job.description,
            job.salary, job.frequency.value if job.frequency else None,
            job.pay_details, job.post_message.jump_url if job.post_message else None,
            job.start_time, job.end_time, job.candidate.user_id if job.candidate else None,
            [r.user_id for r in job.rejections], job.id
        )
        
################################################################################
    def _update_job_posting_channels(self, manager: JobsManager) -> None:
        
        self.execute(
            "UPDATE bot_config SET temp_jobs_channel = %s, perm_jobs_channel = %s "
            "WHERE guild_id = %s;",
            manager.temporary_jobs_channel.id if manager.temporary_jobs_channel else None,
            manager.permanent_jobs_channel.id if manager.permanent_jobs_channel else None,
            manager.guild_id
        )
        
################################################################################
    def _update_background_check(self, check: BackgroundCheck) -> None:
        
        self.execute(
            "UPDATE bg_checks SET agree = %s, names = %s, venues = %s, "
            "jobs = %s, approved = %s, prev_experience = %s, post_url = %s, "
            "submitted_at = %s, approved_at = %s, approved_by = %s WHERE user_id = %s;",
            check.agree, check.names, 
            [v._to_db_string() for v in check.venues], check.positions, 
            check.approved, check.want_to_train, 
            check.post_message.jump_url if check.post_message is not None else None,
            check.submitted_at, check.approved_at,
            check.approved_by.id if check.approved_by is not None else None,
            check.user_id
        )
        
################################################################################
    def _update_roles(self, role_mgr: RoleManager) -> None:
        
        self.execute(
            "UPDATE roles SET trainer_main = %s, trainer_pending = %s, "
            "trainer_hiatus = %s, staff_main = %s, staff_unvalidated = %s, "
            "venue_owner = %s, trainee = %s, trainee_hiatus = %s WHERE guild_id = %s;",
            role_mgr.trainer_main.id if role_mgr.trainer_main else None,
            role_mgr.trainer_pending.id if role_mgr.trainer_pending else None,
            role_mgr.trainer_hiatus.id if role_mgr.trainer_hiatus else None,
            role_mgr.staff_main.id if role_mgr.staff_main else None,
            role_mgr.staff_unvalidated.id if role_mgr.staff_unvalidated else None,
            role_mgr.venue_management.id if role_mgr.venue_management else None,
            role_mgr.trainee.id if role_mgr.trainee else None,
            role_mgr.trainee_hiatus.id if role_mgr.trainee_hiatus else None,
            role_mgr.guild_id
        )
    
################################################################################
    def _update_channels(self, channel_mgr: ChannelManager) -> None:
        
        self.execute(
            "UPDATE channels SET temp_job = %s, perm_job = %s, venues = %s, "
            "profiles = %s, log_channel = %s, services = %s, welcome = %s, "
            "notification_channels = %s, group_training = %s WHERE guild_id = %s;",
            channel_mgr.temp_job_channel.id if channel_mgr.temp_job_channel else None,
            channel_mgr.perm_job_channel.id if channel_mgr.perm_job_channel else None,
            channel_mgr.venues_channel.id if channel_mgr.venues_channel else None,
            channel_mgr.profiles_channel.id if channel_mgr.profiles_channel else None,
            channel_mgr.log_channel.id if channel_mgr.log_channel else None,
            channel_mgr.services_channel.id if channel_mgr.services_channel else None,
            channel_mgr.welcome_channel.id if channel_mgr.welcome_channel else None,
            [c.id for c in channel_mgr.notification_channels], 
            channel_mgr.group_training_channel.id if channel_mgr.group_training_channel else None,
            channel_mgr.guild_id
        )
        
################################################################################
    def _update_service(self, service: HireableService) -> None:
        
        self.execute(
            "UPDATE services SET name = %s, role = %s, color = %s "
            "WHERE _id = %s;",
            service.name, service.role.id if service.role else None, 
            service.color.value if service.color else None, service.id
        )
        
################################################################################
    def _update_service_profile(self, profile: ServiceProfile) -> None:
        
        self.execute(
            "UPDATE service_profiles SET nsfw = %s, rates = %s, style = %s, "
            "website = %s, discord = %s, thumbnail = %s, main_image = %s "
            "WHERE _id = %s;",
            profile.nsfw, profile.rates, profile.style, profile.website,
            profile.discord, profile.thumbnail, profile.main_image, profile.id
        )
        
################################################################################
    def _update_group_training(self, training: GroupTraining) -> None:
        
        self.execute(
            "UPDATE group_trainings SET name = %s, description = %s, start_time = %s, "
            "end_time = %s, post_url = %s, completed = %s, paid = %s, attended = %s "
            "WHERE _id = %s;",
            training.name, training.description, training.start_time, training.end_time, 
            training.post_message.jump_url if training.post_message else None, 
            training.is_completed, training.is_paid, 
            [user.user_id for user in training.attended_users], training.id
        )
        
################################################################################
    def _update_group_training_signup(self, signup: GroupTrainingSignup) -> None:
        
        self.execute(
            "UPDATE group_training_signups SET level = %s WHERE _id = %s;",
            signup.level.value, signup.id
        )
        
################################################################################
    
    log_channel             = _update_log_channel
    position                = _update_position
    requirement             = _update_requirement
    tuser_config            = _update_tuser_config
    tuser_details           = _update_tuser_details
    availability            = _update_availability
    qualification           = _update_qualification
    training                = _update_training
    signup_message          = _update_signup_message
    profile_details         = _update_profile_details
    profile_ataglance       = _update_profile_ataglance
    profile_personality     = _update_profile_personality
    profile_images          = _update_profile_images
    profile_addl_image      = _update_profile_additional_image
    venue_location          = _update_venue_location
    venue_hours             = _update_venue_hours
    venue                   = _update_venue
    venue_aag               = _update_venue_aag
    venue_post_channel      = _update_venue_post_channel
    venue_urls              = _update_venue_urls
    job_hours               = _update_job_hours
    job_posting             = _update_job_post
    job_posting_channels    = _update_job_posting_channels
    background_check        = _update_background_check
    roles                   = _update_roles
    channels                = _update_channels
    service                 = _update_service
    service_profile         = _update_service_profile
    group_training          = _update_group_training
    group_training_signup   = _update_group_training_signup
    
################################################################################
    