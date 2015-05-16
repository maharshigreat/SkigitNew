from django.contrib.auth.models import User

from allauth.account.models import EmailAccount
from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class MyAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # This isn't tested, but should work
        try:
            user = User.objects.get(email=sociallogin.email)
            sociallogin.connect(request, user)
            # Create a response object
            raise ImmediateHttpResponse(response)
        except User.DoesNotExist:
            pass
            #account_uid = SocialAccount.objects.filter(user_id=request.user.id, provider='facebook')
            account_uid[0].get_avatar_url()
            account_uid[0].extra_data['username']
            account_uid[0].extra_data['first_name']
            account_uid[0].extra_data['last_name']
            account_uid[0].extra_data['gender']
            account_uid[0].extra_data['email']
            account_uid[0].extra_data['link']
            account_uid[0].extra_data['uid']