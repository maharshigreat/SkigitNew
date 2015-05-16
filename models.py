from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.providers import registry
from allauth.socialaccount.providers.oauth.provider import OAuthProvider
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider
import datetime
from datetime import datetime
import django
from django import forms
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import permalink
from django.db.models.signals import post_syncdb
import django.dispatch
from django.forms import ModelForm
from django.utils import timezone
from django.utils.translation import ugettext as _
from skigit.api import AccessControl
from skigit.api import Api
import sys
#from django.contrib.sessions.models import Session
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.contrib.auth.models import User
User._meta.get_field('email')._unique = True

from django.conf import settings
from django.contrib.auth.models import Group


# Create your models here.

class Incentive(models.Model):
    title = models.CharField(max_length=200, blank=False, verbose_name="Incentive Title")
    created_date = models.DateTimeField(auto_now_add=True, blank=False)
    updated_date = models.DateTimeField(auto_now=True, blank=False)
    is_active = models.BooleanField(default=True)


class Category(models.Model):
    cat_name = models.CharField(max_length=100, unique=True)
    cat_slug = models.SlugField(max_length=100, unique=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=False)
    updated_date = models.DateTimeField(auto_now=True, blank=False)
    is_active = models.BooleanField(default=True)  
 
    def __str__(self): 
        return self.cat_name
    
    @permalink
    def get_absolute_url(self):
        return ('category_detail_view', None, {'cat_slug': self.cat_slug})       
    
class Subject_Category(models.Model):
    sub_cat_name = models.CharField(max_length=150, unique=True)
    sub_cat_slug = models.SlugField(max_length=150, unique=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=False)
    updated_date = models.DateTimeField(auto_now=True, blank=False)
    is_active = models.BooleanField(default=True)  
    
    def __str__(self): 
        return self.sub_cat_name

    
# code added by mitesh

def setup_dummy_social_apps(sender, ** kwargs):
    """
    `allauth` needs tokens for OAuth based providers. So let's
    setup some dummy tokens
    """
    site = Site.objects.get_current()
    for provider in registry.get_list():
        if (isinstance(provider, OAuth2Provider) 
            or isinstance(provider, OAuthProvider)):
            try:
                SocialApp.objects.get(provider=provider.id,
                                      sites=site)
            except SocialApp.DoesNotExist:
                print ("Installing dummy application credentials for %s."
                       " Authentication via this provider will not work"
                       " until you configure proper credentials via the"
                       " Django admin (`SocialApp` models)" % provider.id)
                app = SocialApp.objects.create(provider=provider.id,
                                               secret='secret',
                                               client_id='client-id',
                                               name='Dummy %s app' % provider.id)
                app.sites.add(site)


# We don't want to interfere with unittests et al
if 'syncdb' in sys.argv:
    post_syncdb.connect(setup_dummy_social_apps, sender=sys.modules[__name__])


# End of code added by mitesh

# code added for youtube upload


class Video(models.Model):
   
    #below fields provided by django-youtube
    title = models.CharField(max_length=200, blank=False, db_index=True, verbose_name="My Skigit Title")
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    video_id = models.CharField(max_length=255, unique=True, null=True,
                                help_text=_("The Youtube id of the video"))
    
    description = models.TextField(null=True, blank=True)
    keywords = models.CharField(max_length=200, null=True, blank=True,
                                help_text=_("Comma seperated keywords"))
    youtube_url = models.URLField(max_length=255, null=True, blank=True)
    swf_url = models.URLField(max_length=255, null=True, blank=True)
    access_control = models.SmallIntegerField(max_length=1,
                                              choices=(
                                              (AccessControl.Public,
                                              "Public"),
                                              (AccessControl.Unlisted,
                                              "Unlisted"),
                                              (AccessControl.Private,
                                              "Private"),
                                              ),
                                              default=AccessControl.Public)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        """
        Returns the swf url
        """
        return self.swf_url

    def entry(self):
        """
        Connects to Youtube Api and retrieves the video entry object

        Return:
            gdata.youtube.YouTubeVideoEntry
        """
        api = Api()
        api.authenticate()
        return api.fetch_video(self.video_id)

    def save(self, * args, ** kwargs):
        """
        Syncronize the video information on db with the video on Youtube
        The reason that I didn't use signals is to avoid saving the video instance twice.
        """

        # if this is a new instance add details from api
        if not self.id:
            # Connect to api and get the details
            entry = self.entry()

            # Set the details
            self.title = entry.media.title.text
            self.description = entry.media.description.text
            self.keywords = entry.media.keywords.text
            self.youtube_url = entry.media.player.url
            self.swf_url = entry.GetSwfUrl()
            if entry.media.private:
                self.access_control = AccessControl.Private
            else:
                self.access_control = AccessControl.Public

            # Save the instance
            super(Video, self).save(*args, ** kwargs)

            # show thumbnails
            for thumbnail in entry.media.thumbnail:
                t = Thumbnail()
                t.url = thumbnail.url
                t.video = self
                t.save()
        else:
            # updating the video instance
            # Connect to API and update video on youtube
            api = Api()

            # update method needs authentication
            api.authenticate()

            # Update the info on youtube, raise error on failure
            api.update_video(self.video_id, self.title, self.description,
                             self.keywords, self.access_control)

        # Save the model
        return super(Video, self).save(*args, ** kwargs)
    
    def delete(self, * args, ** kwargs):
        """
        Deletes the video from youtube

        Raises:
            OperationError
        """
        api = Api()

        # Authentication is required for deletion
        api.authenticate()

        # Send API request, raises OperationError on unsuccessful deletion
        api.delete_video(self.video_id)

        # Call the super method
        return super(Video, self).delete(*args, ** kwargs)

    def default_thumbnail(self):
        """
        Returns the 1st thumbnail in thumbnails
        This method can be updated as adding default attribute the Thumbnail model and return it

        Returns:
            Thumbnail object
        """
        return self.thumbnail_set.all()[0]
        
    def get_profile_img(self):    
        return Profile.objects.get(user_id=self.user_id)
    
    def get_like_status(self):    
        status =  Like.objects.filter(user_id=self.user_id,skigit_id=self.id,status=True)
        if status:
            return 'liked'
        else:
            return 'like'
    
    def get_like_count(self):    
        count =  Like.objects.filter(skigit_id=self.id,status=True).count()
        if count:
            return count
        else:
            return 0
    
        
class Video_Detail(models.Model):
    
    # New added code
    
    title = models.CharField(max_length=200, blank=False, db_index=True, verbose_name="My Skigit Title")
    category = models.ForeignKey(Category, verbose_name="My Skigit Category", default=0)
    subject_category = models.ForeignKey(Subject_Category, verbose_name="My Subject Category", default=0)
    made_by = models.ForeignKey(User, limit_choices_to={'groups__name': settings.BUSINESS_USER}, verbose_name="My awesome thing was made by", related_name="video_made_by", default=0)
    made_by_option = models.CharField(max_length=200, blank=True, verbose_name="If not found in the list above, add maker or proprietor name", default='')
    bought_at = models.CharField(max_length=200, blank=False, verbose_name="I bought my awesome thing at", default='')
    IS_LOGO_TRUE = 1
    IS_LOGO_FALSE = 0
    LOGO_CHOICES = [(IS_LOGO_TRUE, 'Yes'), (IS_LOGO_FALSE, 'No')]
    add_logo = models.IntegerField(choices=LOGO_CHOICES, default=IS_LOGO_FALSE)
    why_rocks = models.TextField(default='')
    
    # End of new added code
    
    skigit_id = models.ForeignKey(Video) #Skigit Post id
    #user = models.ForeignKey(User, related_name="%(class)s_requests_created") #Current login user_id
    business_user = models.ForeignKey(User, blank=True, null=True, related_name="skigit_business_user") #user_id (if cuurent user is business user(is_billable=True))
    status = models.IntegerField(blank=False, default=0) # Approved=1 or Pending=0
    is_share = models.BooleanField(default=False) # shared=1 or normal=0
    share_skigit = models.ForeignKey(Video, blank=True, null=True, related_name="%(class)s_requests_created") # Skigit post id if above shared bit is 1
    inappropriate_skigit = models.BooleanField(default=False) # 1=inappropriate, 0=appropriate
    is_plugged = models.BooleanField(default=False) # 1=plugged
    is_sperk = models.BooleanField(default=False) # 1= sperk logo visible 
    plugged_skigit = models.ForeignKey(Video, blank=True, null=True, related_name="plugged_skigit") # if is_plugged bit true, skigit post id here
    incentive = models.ForeignKey(Incentive, blank=True, null=True) #1=Receive, 2= Donate, 3=None
    
    created_date = models.DateTimeField(auto_now_add=True, blank=False) 
    updated_date = models.DateTimeField(auto_now=True, blank=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
    def get_profile_img(self):  
        return Profile.objects.get(user_id=self.skigit_id.user)
        #return Video.get_profile_img(Video_Detail.objects.get(pk=self.id).select_related('skigit_id,skigit_id__user'))
    
    def get_like_status(self):    
        status =  Like.objects.filter(user_id=self.skigit_id.user,skigit_id=self.skigit_id,status=True)
        if status:
            return 'liked'
        else:
            return 'like'
    
    def get_like_count(self):    
        count =  Like.objects.filter(skigit_id=self.skigit_id,status=True).count()
        if count:
            return count
        else:
            return 0
        
class Thumbnail(models.Model):
    video = models.ForeignKey(Video, null=True)
    url = models.URLField(max_length=255)

    def __unicode__(self):
        return self.url

    def get_absolute_url(self):
        return self.url


class UploadedVideo(models.Model):
    """
    temporary video object that is uploaded to use in direct upload
    """

    file_on_server = models.FileField(upload_to='videos', null=True,
                                      help_text=_("Temporary file on server for \
                                              using in `direct upload` from \
                                              your server to youtube"))

    def __unicode__(self):
        """string representation"""
        return self.file_on_server.url
#
# Signal Definitions
#

video_created = django.dispatch.Signal(providing_args=["video"])



#class Skigits(models.Model):
#    title = models.CharField(max_length=200, blank=False, db_index=True, verbose_name="Title")
#    skigit_media = models.FileField(verbose_name="Video", upload_to="skigit/video/%y/%m/%d", blank=True, null=True)
#    url = models.URLField(verbose_name="Url")
#    is_youtube = models.BooleanField(default=False, verbose_name="Youtube Url")
#    created_date = models.DateTimeField(auto_now_add=True, blank=False)
#    updated_date = models.DateTimeField(auto_now=True, blank=False)
#    is_active = models.BooleanField(default=True)
#    
#    def __str__(self): 
#        return self.title
        


#class Detail(models.Model):
#    skigit_detail = models.ForeignKey(Skigits)
#    user = models.ForeignKey(User, related_name="%(class)s_requests_created")
#    business_user = models.ForeignKey(User, blank=True, null=True, related_name="skigit_business_user")
#    status = models.IntegerField(blank=False, default=0)
#    is_share = models.BooleanField(default=False)
#    share_skigit = models.ForeignKey(Skigits, blank=True, null=True, related_name="%(class)s_requests_created")
#    inappropriate_skigit = models.BooleanField(default=False)
#    is_plugged = models.BooleanField(default=False)
#    is_sperk = models.BooleanField(default=False)
#    plugged_skigit = models.ForeignKey(Skigits, blank=True, null=True, related_name="plugged_skigit")
#    incentive = models.ForeignKey(Incentive, blank=True, null=True)
#    created_date = models.DateTimeField(auto_now_add=True, blank=False)
#    updated_date = models.DateTimeField(auto_now=True, blank=False)
#    is_active = models.BooleanField(default=True)

class Like(models.Model):
    skigit = models.ForeignKey(Video)
    user = models.ForeignKey(User)
    status = models.IntegerField(blank=False, default=0)
    created_date = models.DateTimeField(auto_now_add=True, blank=False)
    updated_date = models.DateTimeField(auto_now=True, blank=False)
    is_active = models.BooleanField(default=True)
    
    def get_like_status(self):    
        status =  Like.objects.filter(user_id=self.user_id,skigit_id=self.id,status=True)
        if status:
            return 'liked'
        else:
            return 'like'

class Favorite(models.Model):
    skigit = models.ForeignKey(Video)
    user = models.ForeignKey(User)
    status = models.IntegerField(blank=False, default=0)
    created_date = models.DateTimeField(auto_now_add=True, blank=False)
    updated_date = models.DateTimeField(auto_now=True, blank=False)
    is_active = models.BooleanField(default=True)    
    
class Share(models.Model):
    skigit = models.ForeignKey(Video)
    user = models.ForeignKey(User)  
    social_site = models.CharField(max_length=200, blank=False)
    created_date = models.DateTimeField(auto_now_add=True, blank=False)
    updated_date = models.DateTimeField(auto_now=True, blank=False)
    is_active = models.BooleanField(default=True)    
    
class Follow(models.Model):
    skigit = models.ForeignKey(Video)
    user = models.ForeignKey(User, related_name="following_user") #following (me)
    follow = models.ForeignKey(User, related_name="follower_user") #follower user id 
    created_date = models.DateTimeField(auto_now_add=True, blank=False)
    updated_date = models.DateTimeField(auto_now=True, blank=False)
    is_active = models.BooleanField(default=True)        
    
class Plugged(models.Model):
    skigit = models.ForeignKey(Video)
    user = models.ForeignKey(User, related_name="plugging_user") #who Plugged user id
    plugged = models.ForeignKey(User, related_name="from_plugged") #From Which  user 
    created_date = models.DateTimeField(auto_now_add=True, blank=False)
    updated_date = models.DateTimeField(auto_now=True, blank=False)
    is_active = models.BooleanField(default=True)            
   
class Profile_img(models.Model):    
    #user = models.ForeignKey(User)
    profile_img = models.ImageField(upload_to="skigit/profile/%y/%m/%d", blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=False)
    updated_date = models.DateTimeField(auto_now=True, blank=False)
    is_active = models.BooleanField(default=True)   
   
class Profile(models.Model):
    GENDER_MALE = 0
    GENDER_FEMALE = 1
    GENDER_CHOICES = [(GENDER_MALE, 'Male'), (GENDER_FEMALE, 'Female')]
    
    NOTIFICATION_NO = 0
    NOTIFICATION_YES = 1
    NOTIFICATION_CHOICES = [(NOTIFICATION_NO, 'No'), (NOTIFICATION_YES, 'Yes')]
    
    user = models.OneToOneField(User)
    gender = models.IntegerField(choices=GENDER_CHOICES, verbose_name="Gender", blank=True, null=True)
    profile_img = models.ImageField(upload_to="skigit/profile/%y/%m/%d", verbose_name="Add a personal photo", blank=True, null=True)
    profile_img_thumb = ImageSpecField(source='profile_img',processors=[ResizeToFill(25,25)],format='JPEG',options={'quality': 100})
    logo_img = models.ImageField(upload_to="skigit/logo/%y/%m/%d", blank=True, null=True)
    logo_img_thumb = ImageSpecField(source='logo_img',processors=[ResizeToFill(80,60)],format='JPEG',options={'quality': 100})
    cover_img = models.OneToOneField(Profile_img, blank=True, null=True)
    about_me = models.TextField(verbose_name="About Me", blank=True, null=True)
    birthdate = models.DateField(verbose_name="Date of Birth", blank=True, null=True) #birthdate = forms.DateField(widget=extras.SelectDateWidget)
    language = models.CharField(max_length=30, verbose_name="Language", blank=True, null=True)
    country = models.CharField(max_length=30, verbose_name="Country", blank=True, null=True)
    state  = models.CharField(max_length=30, verbose_name="State", blank=True, null=True)
    city  = models.CharField(max_length=30, verbose_name="City", blank=True, null=True)
    zip_Code  = models.IntegerField(verbose_name="Zip Code", blank=True, null=True)
    billabel = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True, blank=False)
    updated_date = models.DateTimeField(auto_now=True, blank=False)
    notifications_message = models.IntegerField(choices=NOTIFICATION_CHOICES, blank=False, default=NOTIFICATION_YES)  #A member sends you a new message #Send a notification by email when:
    notifications_friends_1 = models.IntegerField(choices=NOTIFICATION_CHOICES, blank=False, default=NOTIFICATION_YES) #A member sends you a friendship request
    notifications_friends_2 = models.IntegerField(choices=NOTIFICATION_CHOICES, blank=False, default=NOTIFICATION_YES) #A member accepts your friendship request
    notifications_Plug_1 = models.IntegerField(choices=NOTIFICATION_CHOICES, blank=False, default=NOTIFICATION_YES) #A member Plugged-into your Primary skigit
    notifications_Plug_2 = models.IntegerField(choices=NOTIFICATION_CHOICES, blank=False, default=NOTIFICATION_YES) #A member Plugged into a skigit you Plugged into
    notifications_following = models.IntegerField(choices=NOTIFICATION_CHOICES, blank=False, default=NOTIFICATION_YES) #A member I'm following posts a new skigit
    
    #is_active = models.BooleanField(default=True)
    
    def greet(self):
        return {GENDER_MALE: 'Hi, boy', GENDER_FEMALE: 'Hi, girl.'}[self.gender]    
        
User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])

class Friend(models.Model):
    from_user = models.ForeignKey(User, related_name="From_friend")
    to_user = models.ForeignKey(User, related_name="To_friend")
    status = models.IntegerField(blank=False, default=0)
    created_date = models.DateTimeField(auto_now_add=True, blank=False)
    updated_date = models.DateTimeField(auto_now=True, blank=False)
    is_active = models.BooleanField(default=True)
    
class Message(models.Model):
    from_user = models.ForeignKey(User, related_name="From_message")
    to_user = models.ForeignKey(User, related_name="To_message")
    is_read = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True, blank=False)
    updated_date = models.DateTimeField(auto_now=True, blank=False)
    is_active = models.BooleanField(default=True)
    
class Message_reply(models.Model):
    message = models.ForeignKey(Message)
    user = models.ForeignKey(User)
    text = models.TextField()
    is_read = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True, blank=False)
    updated_date = models.DateTimeField(auto_now=True, blank=False)
    is_active = models.BooleanField(default=True)    