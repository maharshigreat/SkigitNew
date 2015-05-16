from .forms import *
from .models import *
from allauth.account.models import EmailAddress
from allauth.account.signals import email_confirmed
from allauth.account.signals import user_signed_up
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.auth.views import password_reset
from django.contrib.auth.views import password_reset_confirm
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.core import serializers
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.dispatch import receiver
from django.forms import ModelForm
from django.forms.models import model_to_dict
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import Context
from django.template import RequestContext
from django.template import Template
from django.template import loader
from django.template.context import RequestContext
from django.utils.text import slugify
from django.utils.translation import ugettext as _
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView
import json
import logging
from skigit.api import AccessControl
from skigit.api import Api
from skigit.api import ApiError
from skigit.forms import *
from skigit.forms import SkigitUploadForm
from skigit.forms import YoutubeDirectUploadForm
from skigit.forms import YoutubeUploadForm
from skigit.models import *
from skigit.models import Video
from skigit.models import Video_Detail
from skigit.models import video_created
#from skigit.views_file import *

# Create your views here.

@receiver (user_signed_up)
def complete_social_signup(sender, **kwargs):
    """
    Receives user_signed_up signal and provides a hook for populating additional user data.
    The user_signed_up signal is sent when a user signs up for an account. This signal is typically 
    followed by a user_logged_in, unless e-mail verification prohibits the user to log in.

    You may populate user data collected from social login's extra info, or other user data here.

    """
    user = kwargs.pop('user')
    request = kwargs.pop('request')
    #sociallogin = request.session['socialaccount_sociallogin']
    group = Group.objects.get(name=settings.GENERAL_USER)
    user.groups.add(group)
    user.save() 
    #urlopen('/api/v1/user/', urlencode(group))

@receiver(email_confirmed)
def email_confirmed_(request, email_address, **kwargs):
    #new_email_address = EmailAddress.objects.get(email=email_address)
    user = User.objects.get(email=email_address.email) 
    user.is_active = True
    messages.success(request, 'Your Account Activated SuccessFully')
    user.save()
    #login(request,user)
    
    #user = User.objects.get(new_email_address.user)
    #user.is_active = True

@csrf_protect
def register(request):
    context = {}
    context = RequestContext(request)
    user = None
    user_profile = None
    category = Category.objects.filter(is_active=True)   
    context.update({'category_list': category,})
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                                            username=form.cleaned_data['username'],
                                            password=form.cleaned_data['password1'],
                                            email=form.cleaned_data['email']
                                            )
            #user = User.objects.get(username=form.cleaned_data['username'])
           
            context['user'] = User.objects.get(username=form.cleaned_data['username'])
            
            return render_to_response('registration/success.html',context,)
    else:
        form = RegistrationForm()
        
    context = RequestContext(request, {'form': form})
    return render_to_response('registration/register.html', context, )
 
@login_required
def user_profile(request):
    context = {}
    context = RequestContext(request)
    user = None
    user_profile = None
    category = Category.objects.filter(is_active=True)   
    context.update({'category_list': category,})
    user = request.user
    
    if request.method == 'POST' and 'basic_profile_submit' in request.POST:
        
        if user.groups.all()[0].name == settings.GENERAL_USER:
            form1 = UserForm(request.POST,instance=request.user)
            form2 = ProfileForm(request.POST,request.FILES,instance=request.user.profile)
        elif user.groups.all()[0].name == settings.BUSINESS_USER:   
            form1 = UserForm(request.POST,instance=request.user)
            form2 = Business_user_ProfileForm(request.POST,request.FILES,instance=request.user.profile)
        else:
            logout(request)
            return HttpResponseRedirect('/')
        #form3 =  Profile_imgForm(request.POST,request.FILES,instance=request.user.profile.cover_img)
        #return HttpResponse(form3)
        if form1.is_valid() and form2.is_valid():
            form1.save()
            form2 = form2.save()
            messages.success(request, 'Profile Upadate Successfully. . ')
            #messages.add_message(request, messages.success, 'Profile Upadate Successfully. . ')
            #form.save(commit=False)        
            #form.cover_img = form3
            #form.save()        
            #cover_img =  profile.cover_img    
            if user.groups.all()[0].name == settings.GENERAL_USER:
                form1 = UserForm(instance=user)
                form2 = ProfileForm(instance=user.profile)
            elif user.groups.all()[0].name == settings.BUSINESS_USER:   
                form1 = UserForm(instance=user)
                form2 = Business_user_ProfileForm(instance=user.profile)
            else:
                logout(request)
                return HttpResponseRedirect('/')
            #form3 =  Profile_imgForm(instance=cover_img)
            
            #context.update(csrf(request))
            #user = request.user
            #profile = user.profile
            #context.update(csrf(request))
            
            #context['form1'] = form1
            #context['form'] = form2     #user_profile_form
            #context['form3'] = form3
            
        else:
            messages.error(request, 'Please Correct the following form error..')
#            #context.update(csrf(request))
#            context['form1'] = form1
#            context['form'] = form2 #user_profile_form
            
            #context['form3'] = form3
    else:
        
        #profile = user.profile
        #cover_img =  profile.cover_img
        user_profile = Profile.objects.get_or_create(user=user)
        #settings.BUSINESS_USER
        #settings.GENERAL_USER
        if user.groups.all()[0].name == settings.GENERAL_USER:
            form1 = UserForm(instance=user)
            form2 = ProfileForm(instance=user.profile)
        elif user.groups.all()[0].name == settings.BUSINESS_USER:   
            form1 = UserForm(instance=user)
            form2 = Business_user_ProfileForm(instance=user.profile)
        else:
            logout(request)
            return HttpResponseRedirect('/')
        
    user_profile = Profile.objects.get(user=user)
    context.update(csrf(request))    
    context['form1'] = form1
    context['form'] = form2        
    context['user'] = user
    context['user_profile'] = user_profile
    context['category_list'] = category
    
    
    #context.update({'user': user,'user_profile' :user_profile})
    #context['form3'] = form3
    return render_to_response('profile/basic_profile.html',context,)
    
def index(request):
    context = {}
    context = RequestContext(request)
    user = None
    user_profile = None
    category = Category.objects.filter(is_active=True)   
    context.update({'category_list': category,})
    
    #vid_latest_uploaded = Video_Detail.objects.order_by('-updated_date').select_related('skigit_id')[0]
    vid_latest_uploaded = Video.objects.order_by('-id').select_related('user')
    if vid_latest_uploaded:
        vid_latest_uploaded = vid_latest_uploaded[0]
    #vid_latest_uploaded = Video.objects.order_by('-id').select_related('user')[0]
    vid_all = Video_Detail.objects.order_by('-updated_date').select_related('skigit_id')
    videos_latest = Video.objects.order_by('-id').select_related('user')
    video_likes = Like.objects.filter(user_id=request.user.id,status=True)
    like_dict = []
    for likes in video_likes:
        like_dict.append(likes.skigit_id)
    
    context.update({'video_likes': like_dict ,'vid_latest_uploaded': vid_latest_uploaded, 'vid_all': vid_all,'videos_latest':videos_latest})
    
    if request.user.is_authenticated():    
        user = request.user
        user = User.objects.get(pk=request.user.id)
        #user_profile = Profile.objects.get_or_create(user=user)
        try:
            user = User.objects.get(pk=request.user.id)
            user_profile = Profile.objects.get(user=user)
            
            if user.groups.all()[0].name == settings.GENERAL_USER:
                if  user.username == '' or user.username is None or user.first_name == '' or user.first_name is None or user.last_name == '' or user.last_name is None or user.email == '' or user.email is None or user_profile.birthdate == '' or user_profile.birthdate is None or user_profile.language == '' or user_profile.language is None or user_profile.country == '' or user_profile.country is None or user_profile.state == '' or user_profile.state is None or user_profile.city == '' or user_profile.city is None or user_profile.zip_Code == '' or user_profile.zip_Code is None:
                    messages.error(request,'Please Fill The Complete Profile Detail')
                    raise ObjectDoesNotExist
                elif user_profile.profile_img == '' or user_profile.profile_img is None:
                    messages.error(request,'Please Upload Your Profile Picture')
                    raise ObjectDoesNotExist
            elif user.groups.all()[0].name == settings.BUSINESS_USER:   
                if  user.username == '' or user.username is None or user.first_name == '' or user.first_name is None or user.last_name == '' or user.last_name is None or user.email == '' or user.email is None or user_profile.birthdate == '' or user_profile.birthdate is None or user_profile.language == '' or user_profile.language is None or user_profile.country == '' or user_profile.country is None or user_profile.state == '' or user_profile.state is None or user_profile.city == '' or user_profile.city is None or user_profile.zip_Code == '' or user_profile.zip_Code is None:
                    messages.error(request,'Please Fill The Complete Profile Detail')
                    raise ObjectDoesNotExist
                elif user_profile.profile_img == '' or user_profile.profile_img is None:
                    messages.error(request,'Please Upload Your Profile Picture')
                    raise ObjectDoesNotExist
                elif user_profile.logo_img == '' or user_profile.logo_img is None:
                    messages.error(request,'Please Upload Your Business Logo')
                    raise ObjectDoesNotExist
            else:
                logout(request)
                return HttpResponseRedirect('/')
            
        except ObjectDoesNotExist:
                #form2 = ProfileForm(instance=request.user)   
    #            messages.warning(request,'Please Fill The Complete Profile Detail. .')
    #            messages.debug(request, '%s SQL statements were executed.' % count)
    #            messages.info(request, 'Three credits remain in your account.')
    #            messages.success(request, 'Profile details updated.')
    #            messages.warning(request, 'Your account expires in three days.')
    #            messages.error(request, 'Document deleted.')
                return HttpResponseRedirect('/profile') #HttpResponseRedirect
        
        user_profile = Profile.objects.get(user=user)
        context.update({'user': user,'user_profile':user_profile})
        return render_to_response('skigit/index.html',context,)
        
    elif request.method == 'POST' and 'login_submit' in request.POST:
        username = request.POST.get('log',None)
        password = request.POST.get('pwd',None)
        user = authenticate(username=username, password=password)
        if user is not None:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                # An inactive account was used - no logging in!
                context = RequestContext(request)
                context.update(csrf(request))
                context.update({'vid_latest_uploaded': vid_latest_uploaded, 'vid_all': vid_all,'videos_latest':videos_latest})
                context.update({'login_error':'Your Skigit account is disabled.'})
                return render_to_response('skigit/index.html',context,)
            
        else:
            # Bad login details were provided. So we can't log the user in.
            context.update(csrf(request))
            str = "Invalid login details: {0}, {1}".format(username, password)
            context.update({'login_error':str})
            context.update({'vid_latest_uploaded': vid_latest_uploaded, 'vid_all': vid_all,'videos_latest':videos_latest})
            return render_to_response('skigit/index.html',context,)

    else:
        context.update(csrf(request))
        return render_to_response('skigit/index.html',context,)

def login_require(request):
    context = {}
    context = RequestContext(request)
    user = None
    user_profile = None
    category = Category.objects.filter(is_active=True)   
    context.update({'category_list': category,})
    
    if  request.user.is_authenticated():
        logout(request)
        return HttpResponseRedirect('/')
    elif request.method == 'POST' and 'login_submit_required' in request.POST:
        username = request.POST.get('log', None)
        password = request.POST.get('pwd', None)
        user = authenticate(username=username, password=password)
        if user is not None:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                # An inactive account was used - no logging in!
                context.update(csrf(request))
                context.update({'login_error':'Your Skigit account is disabled.'})
                return render_to_response('registration/login_required.html', context,)
            
        else:
            # Bad login details were provided. So we can't log the user in.
            context.update(csrf(request))
            str = "Invalid login details: {0}, {1}".format(username, password)
            context.update({'login_error':str})
            return render_to_response('registration/login_required.html', context,)

    else:
        context.update(csrf(request))
        return render_to_response('registration/login_required.html', context,)


def register_type(request):
    context = {}
    context = RequestContext(request)
    user = None
    user_profile = None
    category = Category.objects.filter(is_active=True)   
    context.update({'category_list': category,})
    
    if request.method == 'POST':
        if 'register_type' in request.POST: #if register type form submit
            form = request.POST.get('acc_type', None)
            if form is not None and form in ('general'):
                form = RegistrationForm()
                context.update({'form': form})
                return render_to_response('registration/register_as_general_user.html', context,)
            elif form is not None and form in ('business'):
                form = RegistrationForm()
                context.update({'form': form})
                return render_to_response('registration/register_as_business_user.html', context,)
            else: #if register type submit not match with genral or businesss account reload this form    
                context.update(csrf(request))
                return render_to_response('registration/registration_type.html', context)
        elif 'register_as_general_user' in request.POST:    #IF Genral user register
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = User.objects.create_user(
                                                username=form.cleaned_data['username'],
                                                password=form.cleaned_data['password1'],
                                                email=form.cleaned_data['email']
                                                )
                user = User.objects.get(username=form.cleaned_data['username'])
                g = Group.objects.get(name=str(settings.GENERAL_USER))
                g.user_set.add(user)
                
                context.update({'user': user})                                
                return render_to_response('registration/register_success.html', context,)
            else:
                context.update({'form': form})
                return render_to_response('registration/register_as_general_user.html', context,)
        elif 'register_as_business_user' in request.POST:    #IF Genral user register
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = User.objects.create_user(
                                                username=form.cleaned_data['username'],
                                                password=form.cleaned_data['password1'],
                                                email=form.cleaned_data['email']
                                                )
                user = User.objects.get(username=form.cleaned_data['username'])
                g = Group.objects.get(name=str(settings.BUSINESS_USER))
                g.user_set.add(user)
                
                context.update({'user': user})                                
                return render_to_response('registration/register_success.html', context,)
            else:
                context.update({'form': form})
                return render_to_response('registration/register_as_business_user.html', context,)    
        else:    
            context.update(csrf(request))
            return render_to_response('registration/registration_type.html', context)
        
    else:
        context.update(csrf(request))
        #return render_to_response('registration/registration_type.html',context,context_instance = RequestContext(request))
        #return HttpResponseRedirect('/')
        return render_to_response('registration/registration_type.html', context)
        
@login_required
def user_profile_notifications(request):
    context = {}
    context = RequestContext(request)
    user = None
    user_profile = None
    category = Category.objects.filter(is_active=True)   
    context.update({'category_list': category,})
    user = request.user
        
    if request.method == 'POST' and 'user_profile_notification_submit' in request.POST:
        
        form1 = Profile_Notification_Form(request.POST,instance=user.profile)
        if form1.is_valid():
            form1.save()
            #form.save(commit=False)        
            #form.cover_img = form3
            #form.save()        
            #cover_img =  profile.cover_img    
            form1 = Profile_Notification_Form(instance=user.profile)
            #form3 =  Profile_imgForm(instance=cover_img)
            
            #context.update(csrf(request))
            #user = request.user
            #profile = user.profile
            #context.update(csrf(request))
            
            #context['form1'] = form1
            #context['form'] = form2     #user_profile_form
            #context['form3'] = form3
            
#        else:
#            
#            #context.update(csrf(request))
#            context['form1'] = form1
#            context['form'] = form2 #user_profile_form
            
            #context['form3'] = form3
    else:
        
        #profile = user.profile
        #cover_img =  profile.cover_img
        form1 = Profile_Notification_Form(instance=user.profile)
        #form3 =  Profile_imgForm(instance=cover_img)
        user_profile = Profile.objects.get_or_create(user=user)
    
    user_profile = Profile.objects.get(user=user)
    context.update(csrf(request))    
    context['form1'] = form1
    context['user'] = user
    context['user_profile'] = user_profile
    
    
    #context.update({'user': user,'user_profile' :user_profile})
    #context['form3'] = form3
    return render_to_response('profile/user_profile_eNotifications.html',context,)


@login_required
def user_profile_delete(request):
    context = {}
    context = RequestContext(request)
    user = None
    user_profile = None
    category = Category.objects.filter(is_active=True)   
    context.update({'category_list': category,})
    user = request.user
        
    if request.method == 'POST' and 'user_profile_delete' in request.POST:
        delete_account = request.POST.get('delete-account',None)
        if delete_account == '1':
            user = User.objects.get(pk=request.user.id).delete()
            logout(request)
            messages.success(request,'Your Account Successfully Deactivate')
            return HttpResponseRedirect('/')
        else:
            messages.error(request,'There Is Something Wrong in deactivate')            
    else:
        user_profile = Profile.objects.get_or_create(user=user)
        
    user_profile = Profile.objects.get(user=user)
    context.update(csrf(request))
    context['user'] = user
    context['user_profile'] = user_profile
    return render_to_response('profile/user_profile_delete.html',context,)

#def reset_confirm(request, uidb64=None, token=None):
#    return password_reset_confirm(request, template_name='registration/password_reset_confirm.html',
#        uidb36=uidb64, token=token, post_reset_redirect=reverse('reset_done'))
        
def reset_confirm(request, uidb64=None, token=None):
    context = {}
    context = RequestContext(request)
    user = None
    user_profile = None
    category = Category.objects.filter(is_active=True)   
    context.update({'category_list': category,})
    
    #context= RequestContext(request)
    
    # Wrap the built-in reset confirmation view and pass to it all the captured parameters like uidb64, token
    # and template name, url to redirect after password reset is confirmed.
    return password_reset_confirm(request, template_name='registration/password_reset_confirm.html',
        uidb64=uidb64, token=token, post_reset_redirect=reverse('reset_done'),extra_context=context,)

        
def reset_done(request):
    context = {}
    context = RequestContext(request)
    user = None
    user_profile = None
    category = Category.objects.filter(is_active=True)   
    context.update({'category_list': category,})
    return render_to_response('registration/password_reset_complete.html',context,)

def reset_success(request):
    context = {}
    context = RequestContext(request)
    user = None
    user_profile = None
    category = Category.objects.filter(is_active=True)   
    context.update({'category_list': category,})
    return render_to_response('registration/password_resets_done.html',context,)

def reset(request):
    context = {}
    context = RequestContext(request)
    user = None
    user_profile = None
    category = Category.objects.filter(is_active=True)   
    context.update({'category_list': category,})
        
    return password_reset(request, template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/recovery_email_subject.txt',
        post_reset_redirect=reverse('reset_success'),
        extra_context= context,)

def logout_user(request):
    logout(request)
    messages.info(request, 'Your Account Logout SuccessFully')
    return HttpResponseRedirect('/')
    #return HttpResponseRedirect('/')

def aboust_us_view(request):
    context = {}
    context = RequestContext(request)
    user = None
    user_profile = None
    category = Category.objects.filter(is_active=True)   
    context.update({'category_list': category,})
    return render_to_response('aboutus/about_us.html',context)

def faq_view(request):
    context = {}
    context = RequestContext(request)
    user = None
    user_profile = None
    category = Category.objects.filter(is_active=True)   
    context.update({'category_list': category,})
    return render_to_response('aboutus/FAQ.html',context)

def privacy_policy_view(request):
    context = {}
    context = RequestContext(request)
    user = None
    user_profile = None
    category = Category.objects.filter(is_active=True)   
    context.update({'category_list': category,})
    return render_to_response('aboutus/privacy_policy.html',context)

def t_and_c_view(request):
    context = {}
    context = RequestContext(request)
    user = None
    user_profile = None
    category = Category.objects.filter(is_active=True)   
    context.update({'category_list': category,})
    return render_to_response('aboutus/t_and_c.html',context)

def acceptable_use_policy_view(request):
    context = {}
    context = RequestContext(request)
    user = None
    user_profile = None
    category = Category.objects.filter(is_active=True)   
    context.update({'category_list': category,})
    return render_to_response('aboutus/acceptable_use_policy.html',context)

def copyright_policy_view(request):
    context = {}
    context = RequestContext(request)
    user = None
    user_profile = None
    category = Category.objects.filter(is_active=True)   
    context.update({'category_list': category,})
    return render_to_response('aboutus/Copyright_policy.html',context)

def skigit_for_business_view(request):
    context = {}
    context = RequestContext(request)
    user = None
    user_profile = None
    category = Category.objects.filter(is_active=True)   
    context.update({'category_list': category,})
    return render_to_response('aboutus/skigit_for_business.html',context)

def business_terms_of_service(request):
    context = {}
    context = RequestContext(request)
    user = None
    user_profile = None
    category = Category.objects.filter(is_active=True)   
    context.update({'category_list': category,})
    return render_to_response('aboutus/Business_Terms_of_Service.html',context)

def investors_view(request):
    context = {}
    context = RequestContext(request)
    user = None
    user_profile = None
    category = Category.objects.filter(is_active=True)   
    context.update({'category_list': category,})
    return render_to_response('aboutus/Investors.html',context)

def guidelines_view(request):
    context = {}
    context = RequestContext(request)
    user = None
    user_profile = None
    category = Category.objects.filter(is_active=True)   
    context.update({'category_list': category,})
    return render_to_response('guidelines/guidelines.html',context)

def skigitology_view(request):
    context = {}
    context = RequestContext(request)
    user = None
    user_profile = None
    category = Category.objects.filter(is_active=True)   
    context.update({'category_list': category,})
    return render_to_response('guidelines/skigitology.html',context)

def skigit_length_view(request):
    context = {}
    context = RequestContext(request)
    user = None
    user_profile = None
    category = Category.objects.filter(is_active=True)   
    context.update({'category_list': category,})
    return render_to_response('guidelines/skigit_length.html',context)

def making_your_skigit_view(request):
    context = {}
    context = RequestContext(request)
    user = None
    user_profile = None
    category = Category.objects.filter(is_active=True)   
    context.update({'category_list': category,})
    return render_to_response('guidelines/making_your_skigit_view.html',context)

def allowed_video_formats_view(request):
    context = {}
    context = RequestContext(request)
    user = None
    user_profile = None
    category = Category.objects.filter(is_active=True)   
    context.update({'category_list': category,})
    return render_to_response('guidelines/allowed_video_formats_view.html',context)

logger = logging.getLogger(__name__)

def _video_params(request, video_id):

    width = request.GET.get("width", "70%")
    height = request.GET.get("height", "350")
    origin = request.get_host()

    return {"video_id": video_id, "origin": origin, "width": width, "height": height}


def check_video_availability(request, video_id):
    """
    Controls the availability of the video. Newly uploaded videos are in processing stage.
    And others might be rejected.

    Returns:
        json response
    """
    # Check video availability
    # Available states are: processing
    api = Api()
    api.authenticate()
    availability = api.check_upload_status(video_id)

    if availability is not True:
        data = {'success': False}
    else:
        data = {'success': True}

    return HttpResponse(json.dumps(data), content_type="application/json")


def video(request, video_id):
    """
    Displays a video in an embed player
    """

    # Check video availability
    # Available states are: processing
    api = Api()
    api.authenticate()
    availability = api.check_upload_status(video_id)

    if availability is not True:
        # Video is not available
        video = Video.objects.filter(video_id=video_id).get()

        state = availability["upload_state"]

        # Add additional states here. I'm not sure what states are available
        if state == "failed" or state == "rejected":
            return render_to_response(
                                      "youtube/yt_video_failed.html",
                                      {"video": video, "video_id": video_id, "message":
                                      _("Invalid video."), "availability": availability},
                                      context_instance=RequestContext(request)
                                      )
        else:
            return render_to_response(
                                      "youtube/yt_video_unavailable.html",
                                      {"video": video, "video_id": video_id,
                                      "message": _("This video is currently being processed"), "availability": availability},
                                      context_instance=RequestContext(request)
                                      )

    video_params = _video_params(request, video_id)

    return render_to_response(
                              "youtube/yt_video.html",
                              video_params,
                              context_instance=RequestContext(request)
                              )


def video_list(request, username=None):
    """
    list of videos of a user
    if username does not set, shows the currently logged in user
    """

    # If user is not authenticated and username is None, raise an error
    if username is None and not request.user.is_authenticated():
        from django.http import Http404
        raise Http404

    from django.contrib.auth.models import User
    user = User.objects.get(username=username) if username else request.user

    # loop through the videos of the user
    videos = Video.objects.filter(user=user).all()
    video_params = []
    for video in videos:
        video_params.append(_video_params(request, video.video_id))

    return render_to_response(
                              "youtube/yt_videos.html",
                              {"video_params": video_params},
                              context_instance=RequestContext(request)
                              )


@csrf_exempt
@login_required
def direct_upload(request):
    """
    direct upload method
    starts with uploading video to our server
    then sends the video file to youtube

    param:
        (optional) `only_data`: if set, a json response is returns i.e. {'video_id':'124weg'}

    return:
        if `only_data` set, a json object.
        otherwise redirects to the video display page
    """
    return_only_data = None
    category = Category.objects.filter(is_active=True)
    if request.method == "POST":
        try:
            primary_form = YoutubeDirectUploadForm(request.POST, request.FILES)
            secondary_from = SkigitUploadForm(request.POST)
            # upload the file to our server
            if primary_form.is_valid() and secondary_from.is_valid():
                
                title = request.POST.get("title", "%s's video on %s" % (request.user.username, request.get_host()))
                description = request.POST.get("why_rocks", "")
                keywords = request.POST.get("keywords", "")
                
                category = request.POST.get("category", "")
                subject_category = request.POST.get("subject_category", "")
                made_by = request.POST.get("made_by", "")
                bought_at = request.POST.get("bought_at", "")
                made_by_option = request.POST.get("made_by_option", "")
                add_logo = request.POST.get("add_logo", "")
                why_rocks = request.POST.get("why_rocks", "")
                
                uploaded_video = primary_form.save() # Saves the video only

                # send this file to youtube
                api = Api()
                api.authenticate()
                video_entry = api.upload_direct(uploaded_video.file_on_server.path, title)

                # get data from video entry
                swf_url = video_entry.GetSwfUrl()
                youtube_url = video_entry.id.text

                # getting video_id is tricky, I can only reach the url which
                # contains the video_id.
                # so the only option is to parse the id element
                # https://groups.google.com/forum/?fromgroups=#!topic/youtube-api-gdata/RRl_h4zuKDQ
                url_parts = youtube_url.split("/")
                url_parts.reverse()
                video_id = url_parts[0]

                # save video_id to video instance
                video = Video()
                video.user = request.user
                video.video_id = video_id
                video.title = title
                video.description = description
                video.youtube_url = youtube_url
                video.swf_url = swf_url
                video.save()
                
                # Save video details
                
                child_instance = Video_Detail()
                child_instance.skigit_id = video
                child_instance.category = Category.objects.get(pk=category)
                child_instance.subject_category = Subject_Category.objects.get(pk=subject_category)
                child_instance.made_by = request.user
                child_instance.bought_at = bought_at
                child_instance.title = title 
                child_instance.made_by_option = made_by_option
                child_instance.add_logo = add_logo
                child_instance.why_rocks = why_rocks

                child_instance.save() # save data to video_detail model

                # send a signal
                video_created.send(sender=video, video=video)

                # delete the uploaded video instance
                uploaded_video.delete()

                # return the response
                return_only_data = request.GET.get('only_data')
                if return_only_data:
                    return HttpResponse(json.dumps({"video_id": video_id}), content_type="application/json")
                else:
                    # Redirect to the video page or the specified page
                    try:
                        next_url = settings.YOUTUBE_UPLOAD_REDIRECT_URL
                    except AttributeError:
                        next_url = reverse(
                                           "youtube:skigit.views.video", kwargs={"video_id": video_id})

                    return HttpResponseRedirect(next_url)
        except:
            import sys
            logger.error("Unexpected error: %s - %s" % (sys.exc_info()[
                         0], sys.exc_info()[1]))
            # @todo: proper error management
            return HttpResponse("error happened")

    primary_form = YoutubeDirectUploadForm()
    secondary_from = SkigitUploadForm()

    if return_only_data:
        return HttpResponse(json.dumps({"error": 500}), content_type="application/json")
    else:
        return render_to_response(
                                  "youtube/yt_direct-upload.html",
                                  {"primary_form": primary_form, "secondary_form":secondary_from, 'category_list': category,},
                                  context_instance=RequestContext(request)
                                  )


@login_required
def upload(request):
    """
    Displays an upload form
    Creates upload url and token from youtube api and uses them on the form
    """
    if request.user.is_authenticated():    
        try:
            user = User.objects.get(pk=request.user.id)
            user_profile = Profile.objects.get(user=user)
            if user_profile.profile_img == '' or user_profile.profile_img is None or user.username == '' or user.username is None or user.first_name == '' or user.first_name is None or user.last_name == '' or user.last_name is None or user.email == '' or user.email is None or user_profile.birthdate == '' or user_profile.birthdate is None or user_profile.language == '' or user_profile.language is None or user_profile.country == '' or user_profile.country is None or user_profile.state == '' or user_profile.state is None or user_profile.city == '' or user_profile.city is None or user_profile.zip_Code == '' or user_profile.zip_Code is None:
                
                raise ObjectDoesNotExist
        except ObjectDoesNotExist:
            #form2 = ProfileForm(instance=request.user)   
            messages.warning(request,'Complete Your Profle Detail. .')
#            messages.debug(request, '%s SQL statements were executed.' % count)
#            messages.info(request, 'Three credits remain in your account.')
#            messages.success(request, 'Profile details updated.')
#            messages.warning(request, 'Your account expires in three days.')
#            messages.error(request, 'Document deleted.')
            return HttpResponseRedirect('/profile')
    
    category = Category.objects.filter(is_active=True)
    if request.method == "POST":
    
        # Get the optional parameters
        
        secondary_from = SkigitUploadForm(request.POST)
        
        if secondary_from.is_valid():
            
            title = request.POST.get("title", "%s's video on %s" %(request.user.username, request.get_host()))
            description = request.POST.get("why_rocks", "")
            keywords = request.POST.get("keywords", "")
            request.session['title'] = request.POST.get("title", "")
            request.session['category'] = request.POST.get("category", "")
            request.session['subject_category'] = request.POST.get("subject_category", "")
            request.session['made_by'] = request.POST.get("made_by", "")
            request.session['bought_at'] = request.POST.get("bought_at", "")
            request.session['made_by_option'] = request.POST.get("made_by_option", "")
            request.session['add_logo'] = request.POST.get("add_logo", "")
            request.session['why_rocks'] = request.POST.get("why_rocks", "")
            
            
            # Try to create post_url and token to create an upload form
            try:
                api = Api()

                # upload method needs authentication
                api.authenticate()

                # Customize following line to your needs, you can add description, keywords or developer_keys
                # I prefer to update video information after upload finishes
                data = api.upload(title, description=description, keywords=keywords,
                                  access_control=AccessControl.Unlisted)
            except ApiError as e:
                # An api error happened, redirect to homepage
                messages.add_message(request, messages.ERROR, e.message)
                return HttpResponseRedirect("/")
            except:
                # An error happened, redirect to homepage
                messages.add_message(request, messages.ERROR, _(
                                     'An error occurred during the upload, Please try again.'))
                return HttpResponseRedirect("/")

            # Create the form instance
            
            
            primary_form = YoutubeUploadForm(initial={"token": data["youtube_token"]})
        
            protocol = 'https' if request.is_secure() else 'http'
            next_url = '?nexturl=%s://%s%s/' % (protocol, request.get_host(), reverse("youtube:skigit.views.upload_return"))
            return render_to_response(
                                      "youtube/yt_upload.html",
                                      {"primary_form": primary_form, "secondary_form":secondary_from, "post_url": data["post_url"], "next_url": next_url, "title": title,'category_list': category,'user': user,'user_profile' :user_profile},
                                      context_instance=RequestContext(request)
                                      )
        else:
            primary_form = YoutubeUploadForm()
            secondary_from = SkigitUploadForm(request.POST) 
            protocol = 'https' if request.is_secure() else 'http'
            next_url = '?nexturl=%s://%s%s/' % (protocol, request.get_host(), reverse("youtube:skigit.views.upload"))
                
    else:
        primary_form = YoutubeUploadForm()
        secondary_from = SkigitUploadForm() 
        protocol = 'https' if request.is_secure() else 'http'
        #next_url = '%s://%s%s/' % (protocol, request.get_host(), reverse("skigit.views.upload"))
    return render_to_response(
                              "youtube/yt_upload.html",
                              {"primary_form": primary_form, "secondary_form":secondary_from,'category_list': category,'user': user,'user_profile' :user_profile },
                              context_instance=RequestContext(request)
                              )    

        

@login_required
def upload_return(request):
    """
    The upload result page
    Youtube will redirect to this page after upload is finished
    Saves the video data and redirects to the next page

    Params:
        status: status of the upload (200 for success)
        id: id number of the video
    """
    status = request.GET.get("status")
    video_id = request.GET.get("id")

    if status == "200" and video_id:
        # upload is successful

        # save the video entry
        video = Video()
        video.user = request.user
        video.video_id = video_id
        sk_id = video.video_id
        video.save()
        
        # Add Details into video_detail table
        
        child_instance = Video_Detail()
        child_instance.skigit_id = video
        child_instance.category = Category.objects.get(pk=request.session['category'])
        child_instance.subject_category = Subject_Category.objects.get(pk=request.session['subject_category'])
        child_instance.made_by = request.user
        child_instance.bought_at = request.session['bought_at']
        child_instance.title = request.session['title'] 
        child_instance.made_by_option = request.session['made_by_option']
        child_instance.add_logo = request.session['add_logo']
        child_instance.why_rocks = request.session['why_rocks']
        
        child_instance.save()

        # send a signal
        video_created.send(sender=video, video=video)

        # Redirect to the video page or the specified page
        try:
            next_url = settings.YOUTUBE_UPLOAD_REDIRECT_URL
        except AttributeError:
            next_url = reverse(
                               "youtube:skigit.views.video", kwargs={"video_id": video_id})

        return HttpResponseRedirect(next_url)
    else:
        # upload failed, redirect to upload page
        from django.contrib import messages
        messages.add_message(
                             request, messages.ERROR, _('Upload failed, Please try again.'))
        return HttpResponseRedirect(reverse("youtube:skigit.views.upload"))


@login_required
@require_http_methods(["POST"])
def remove(request, video_id):
    """
    Removes the video from youtube and from db
    Requires POST
    """

    # prepare redirection url
    try:
        next_url = settings.YOUTUBE_DELETE_REDIRECT_URL
    except AttributeError:
        next_url = reverse("youtube:skigit.views.upload")

    # Remove from db
    try:
        Video.objects.get(video_id=video_id).delete()
    except:
        from django.contrib import messages
        messages.add_message(
                             request, messages.ERROR, _('Video could not be deleted.'))

    # Return to upload page or specified page
    return HttpResponseRedirect(next_url)


# End of code added for youtube upload


# For category view


def category_view(request):
    return render_to_response('sk_cat/category.html', {
                                  'category': Category.objects.all(),
#                                  'cat_all': category,
                                  })

    
def category_detail_view(request,cat_slug):
    
    category_current = Category.objects.get(cat_slug=cat_slug)
    category = Category.objects.filter(is_active=True)
    vid = Video_Detail.objects.filter(category__cat_slug=cat_slug).order_by('-updated_date').select_related('skigit_id,skigit_id__user')
    videos_latest = Video.objects.order_by('-id').select_related('user')
    user = None
    user_profile = None
    
    video_likes = Like.objects.filter(user_id=request.user.id,status=True)
    like_dict = []
    for likes in video_likes:
        like_dict.append(likes.skigit_id)
    
    if request.user.is_authenticated():    
        user = User.objects.get(pk=request.user.id)
        user_profile = Profile.objects.get(user=user)
        if user_profile.profile_img == '' or user_profile.profile_img is None or user.username == '' or user.username is None or user.first_name == '' or user.first_name is None or user.last_name == '' or user.last_name is None or user.email == '' or user.email is None or user_profile.birthdate == '' or user_profile.birthdate is None or user_profile.language == '' or user_profile.language is None or user_profile.country == '' or user_profile.country is None or user_profile.state == '' or user_profile.state is None or user_profile.city == '' or user_profile.city is None or user_profile.zip_Code == '' or user_profile.zip_Code is None:
        
            user_profile = Profile.objects.get(user=user)
            
    return render_to_response('sk_cat/category_detail_view.html', {
                                  'video_detail': vid,
                                  'category_current': category_current,
                                  'category_list': category,
                                  'user': user,
                                  'user_profile' :user_profile,
                                  'video_likes': like_dict 
#                                  'cat_all': category,
                                  })
                                  
def popup_page(request, video_id):
    """
    Displays a video in an embed player
    """
    vid = Video_Detail.objects.filter(skigit_id__id=video_id).select_related('skigit_id,skigit_id__user,category,subject_category')[0]
    user = None
    user_profile = None
    
    if request.user.is_authenticated():    
        user = User.objects.get(pk=request.user.id)
        user_profile = Profile.objects.get(user=user)
        if user_profile.profile_img == '' or user_profile.profile_img is None or user.username == '' or user.username is None or user.first_name == '' or user.first_name is None or user.last_name == '' or user.last_name is None or user.email == '' or user.email is None or user_profile.birthdate == '' or user_profile.birthdate is None or user_profile.language == '' or user_profile.language is None or user_profile.country == '' or user_profile.country is None or user_profile.state == '' or user_profile.state is None or user_profile.city == '' or user_profile.city is None or user_profile.zip_Code == '' or user_profile.zip_Code is None:
        
            user_profile = Profile.objects.get(user=user)
    
    # query below return uploaded latest 7 videos by user whos video opend in popup
    skigits_might_like = Video_Detail.objects.filter(skigit_id__user_id=vid.skigit_id.user_id).exclude(skigit_id__id=video_id).order_by('-updated_date').select_related('skigit_id,skigit_id__user,category,subject_category')[:7]
    
    return render_to_response("youtube/yt_popuppage.html", {
                                  'vid': vid,
                                  'user': user,
                                  'user_profile':user_profile,
                                  'skigits_might_like' : skigits_might_like,
                                  #                                  'cat_all': category,
                                  })


@login_required                       
def skigit_like(request):
    """
    To insert detail about like/unlike of skigit
    """    
    if request.method == 'POST' and request.is_ajax():
        skigit_id = request.POST['skigit_id']
        user_id = request.user.id
        #Check whether the post is liked before with same post_ID AND user_id
        is_liked = Like.objects.filter(skigit_id=skigit_id,user_id=user_id)
        
        if is_liked.count() == 0:
            # Not liked before (Code for like skigit and insert details)
            like = Like()
            like.skigit = Video.objects.get(pk=skigit_id)
            like.user = request.user
            like.status = 1
            like.save()
            is_liked = 1
            like_count = Like.objects.filter(skigit_id=skigit_id,status=True).count()
            message = 'Skigit Liked Sussessfully'
            
            # This post is liked before with same post_id and user_id
        elif is_liked.count() == 1:
            
            already_liked = Like.objects.filter(skigit_id=skigit_id,user_id=user_id,status=True)
            
            if already_liked:
            #Check the status (if already liked then status=True)    
                
                is_liked.update(status=False) # Update the status from True to False (For Unlike)
                message = 'Unliked Successfully'
                is_liked = 0
                like_count = Like.objects.filter(skigit_id=skigit_id,status=True).count()
            
            else:
                is_liked.update(status=True)
                message = 'Liked Successfully'
                is_liked = 1
                like_count = Like.objects.filter(skigit_id=skigit_id,status=True).count()
            
        else:
            is_liked = 0
            message = 'More than one like for the same post and same user'
            
    response_data = {}
    response_data['is_liked'] = is_liked
    response_data['message'] = message
    response_data['like_count'] = like_count
    
    
    return HttpResponse(json.dumps(response_data), content_type="application/json")
                                             
