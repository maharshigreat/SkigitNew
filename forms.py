from .models import *
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
import itertools
import re
from django.conf import settings
from django.contrib.auth.models import Group

#from skigit.models import UploadedVideo
#from skigit.models import Video_Detail


class RegistrationForm(forms.Form):
 
    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Username"), error_messages={'invalid': _("This value must contain only letters, numbers and underscores.")})
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Email address"))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password (again)"))
 
    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("The username already exists. Please try another one."))
 
    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data

class UserForm(forms.ModelForm):
    class Meta: 
        model = User
        widgets = {
            'username':  forms.TextInput(attrs={'placeholder': 'User Name', 'required':'True'}),
            'email':   forms.TextInput(attrs={'placeholder': 'E-mail Address ', 'required':'True'}),
            'password':  forms.TextInput(attrs={'required':'True', 'max_length':'30', 'render_value':'False'}),
        }
        fields = ('username', 'email', 'first_name', 'last_name')

class ProfileForm(forms.ModelForm):
 
    class Meta: 
        model = Profile
        widgets = {
            'profile_img'   : forms.FileInput(attrs={'placeholder': 'Profile Picture',}),
            #'cover_img'  : forms.FileInput(attrs={'placeholder': 'Cover Images','multiple':'multiple'}),
            'birthdate': forms.TextInput(attrs={'placeholder': 'Date Of Birth', 'required':'True'}),
            'zip_Code': forms.TextInput(attrs={'placeholder': 'zip_Code', 'required':'True'}),
            'gender': forms.Select(attrs={'placeholder': 'Gender', 'required':'True'}),
            'language': forms.TextInput(attrs={'placeholder': 'Language', 'required':'True'}),
            'country': forms.TextInput(attrs={'placeholder': 'country', 'required':'True'}),
            'state': forms.TextInput(attrs={'placeholder': 'state', 'required':'True'}),
            'city': forms.TextInput(attrs={'placeholder': 'city', 'required':'True'}),
        }
        #'cover_img'
        fields = ('profile_img', 'gender', 'birthdate', 'about_me', 'language', 'country', 'state', 'city', 'zip_Code', )

class SignupForm(forms.Form):
    pass

    def signup(self, request, user):
        user.is_active = False
        role = request.session.get('user_type')
        #group = role or "Default"
        g = Group.objects.get(name=settings.GENERAL_USER)
        user.groups.add(g)
        user.save()



class Business_user_ProfileForm(forms.ModelForm):
 
    class Meta: 
        model = Profile
        widgets = {
            'profile_img'   : forms.FileInput(attrs={'placeholder': 'Profile Picture',}),
            'logo_img'   : forms.FileInput(attrs={'placeholder': 'Profile Picture',}),
            #'cover_img'  : forms.FileInput(attrs={'placeholder': 'Cover Images','multiple':'multiple'}),
            'birthdate': forms.TextInput(attrs={'placeholder': 'Date Of Birth', 'required':'True'}),
            'zip_Code': forms.TextInput(attrs={'placeholder': 'zip_Code', 'required':'True'}),
            'gender': forms.Select(attrs={'placeholder': 'Gender', 'required':'True'}),
            'language': forms.TextInput(attrs={'placeholder': 'Language', 'required':'True'}),
            'country': forms.TextInput(attrs={'placeholder': 'country', 'required':'True'}),
            'state': forms.TextInput(attrs={'placeholder': 'state', 'required':'True'}),
            'city': forms.TextInput(attrs={'placeholder': 'city', 'required':'True'}),
        }
        #'cover_img'
        fields = ('logo_img','profile_img', 'gender', 'birthdate', 'about_me', 'language', 'country', 'state', 'city', 'zip_Code',)


class Profile_Notification_Form(forms.ModelForm):
    class Meta: 
        model = Profile
        widgets = {
            'notifications_message': forms.RadioSelect(attrs={'required':'True'}),
            'notifications_friends_1': forms.RadioSelect(attrs={'required':'True'}),
            'notifications_friends_2': forms.RadioSelect(attrs={'required':'True'}),
            'notifications_Plug_1': forms.RadioSelect(attrs={'required':'True'}),
            'notifications_Plug_2': forms.RadioSelect(attrs={'required':'True'}),
            'notifications_following': forms.RadioSelect(attrs={'required':'True'}),
        }
        #'cover_img'
        fields = ('notifications_message', 'notifications_friends_1', 'notifications_friends_2', 'notifications_Plug_1', 'notifications_Plug_2', 'notifications_following')



class Profile_imgForm(forms.ModelForm):
 
    class Meta: 
        model = Profile_img
        widgets = {
            #'profile_img'   : forms.FileInput(attrs={'placeholder': 'Location','required':'True'}),
            'profile_img': forms.FileInput(attrs={'placeholder': 'Cover Images', 'multiple':'multiple'}),
            #'author'     : forms.TextInput(attrs={'placeholder': 'Author'}),
            #'zip_Code'       : forms.TextInput(attrs={'placeholder': 'zip_Code'}),
            #'description': forms.Textarea(attrs={'placeholder': 'Description'}),
        }
        #'cover_img'
        fields = ('profile_img', )

class YoutubeUploadForm(forms.Form):
    token = forms.CharField()
    title = forms.CharField()
    file = forms.FileField(required=True)

class SkigitUploadForm(forms.ModelForm):
    class Meta:
        model = Video_Detail
        widgets = {
            'add_logo': forms.Select(attrs={'name': 'add_logo','required':'True'}), 
            'title': forms.TextInput(attrs={'placeholder': 'Enter your Skigit Title', 'required': True}),
            'category' : forms.Select(attrs={'placeholder': 'Select a skigit category', 'required':'True'}),
            'bought_at' : forms.TextInput(attrs={'placeholder': 'Enter item URL', 'required': True}),
            'why_rocks' : forms.Textarea(attrs={'required': True}),
            }
#        widgets = {
#            #'profile_img'   : forms.FileInput(attrs={'placeholder': 'Profile Picture','required':'True',}),
#            #'cover_img'  : forms.FileInput(attrs={'placeholder': 'Cover Images','multiple':'multiple'}),
#            'birthdate': forms.TextInput(attrs={'placeholder': 'Date Of Birth', 'required':'True'}),
#            'zip_Code': forms.TextInput(attrs={'placeholder': 'zip_Code', 'required':'True'}),
#            'gender': forms.Select(attrs={'placeholder': 'Gender', 'required':'True'}),
#            'language': forms.TextInput(attrs={'placeholder': 'Language', 'required':'True'}),
#            'country': forms.TextInput(attrs={'placeholder': 'country', 'required':'True'}),
#            'state': forms.TextInput(attrs={'placeholder': 'state', 'required':'True'}),
#            'city': forms.TextInput(attrs={'placeholder': 'city', 'required':'True'}),
#        }    
        exclude = ('skigit_id', 'business_user', 'status', 'is_share', 'share_skigit', 'inappropriate_skigit', 'is_plugged', 'is_sperk', 'plugged_skigit', 'incentive', 'is_active')    


class YoutubeDirectUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedVideo 
        widgets = {
            'file_on_server': forms.FileInput(attrs={'name': 'file_on_server','required':'True'})
            }
        

