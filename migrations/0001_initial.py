# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cat_name', models.CharField(unique=True, max_length=100)),
                ('cat_slug', models.SlugField(unique=True, max_length=100)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.IntegerField(default=0)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('follow', models.ForeignKey(related_name=b'follower_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.IntegerField(default=0)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('from_user', models.ForeignKey(related_name=b'From_friend', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(related_name=b'To_friend', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Incentive',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name=b'Incentive Title')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.IntegerField(default=0)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_read', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('from_user', models.ForeignKey(related_name=b'From_message', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(related_name=b'To_message', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message_reply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('is_read', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('message', models.ForeignKey(to='skigit.Message')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Plugged',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('plugged', models.ForeignKey(related_name=b'from_plugged', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gender', models.IntegerField(blank=True, null=True, verbose_name=b'Gender', choices=[(0, b'Male'), (1, b'Female')])),
                ('profile_img', models.ImageField(upload_to=b'skigit/profile/%y/%m/%d', null=True, verbose_name=b'Add a personal photo', blank=True)),
                ('logo_img', models.ImageField(null=True, upload_to=b'skigit/logo/%y/%m/%d', blank=True)),
                ('about_me', models.TextField(null=True, verbose_name=b'About Me', blank=True)),
                ('birthdate', models.DateField(null=True, verbose_name=b'Date of Birth', blank=True)),
                ('language', models.CharField(max_length=30, null=True, verbose_name=b'Language', blank=True)),
                ('country', models.CharField(max_length=30, null=True, verbose_name=b'Country', blank=True)),
                ('state', models.CharField(max_length=30, null=True, verbose_name=b'State', blank=True)),
                ('city', models.CharField(max_length=30, null=True, verbose_name=b'City', blank=True)),
                ('zip_Code', models.IntegerField(null=True, verbose_name=b'Zip Code', blank=True)),
                ('billabel', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('notifications_message', models.IntegerField(default=1, choices=[(0, b'No'), (1, b'Yes')])),
                ('notifications_friends_1', models.IntegerField(default=1, choices=[(0, b'No'), (1, b'Yes')])),
                ('notifications_friends_2', models.IntegerField(default=1, choices=[(0, b'No'), (1, b'Yes')])),
                ('notifications_Plug_1', models.IntegerField(default=1, choices=[(0, b'No'), (1, b'Yes')])),
                ('notifications_Plug_2', models.IntegerField(default=1, choices=[(0, b'No'), (1, b'Yes')])),
                ('notifications_following', models.IntegerField(default=1, choices=[(0, b'No'), (1, b'Yes')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profile_img',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('profile_img', models.ImageField(null=True, upload_to=b'skigit/profile/%y/%m/%d', blank=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Share',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('social_site', models.CharField(max_length=200)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Subject_Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sub_cat_name', models.CharField(unique=True, max_length=150)),
                ('sub_cat_slug', models.SlugField(unique=True, max_length=150)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Thumbnail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UploadedVideo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file_on_server', models.FileField(help_text='Temporary file on server for                                               using in `direct upload` from                                               your server to youtube', null=True, upload_to=b'videos')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name=b'My Skigit Title', db_index=True)),
                ('video_id', models.CharField(help_text='The Youtube id of the video', max_length=255, unique=True, null=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('keywords', models.CharField(help_text='Comma seperated keywords', max_length=200, null=True, blank=True)),
                ('youtube_url', models.URLField(max_length=255, null=True, blank=True)),
                ('swf_url', models.URLField(max_length=255, null=True, blank=True)),
                ('access_control', models.SmallIntegerField(default=0, max_length=1, choices=[(0, b'Public'), (1, b'Unlisted'), (2, b'Private')])),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Video_Detail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name=b'My Skigit Title', db_index=True)),
                ('made_by_option', models.CharField(default=b'', max_length=200, verbose_name=b'If not found in the list above, add maker or proprietor name', blank=True)),
                ('bought_at', models.CharField(default=b'', max_length=200, verbose_name=b'I bought my awesome thing at')),
                ('add_logo', models.IntegerField(default=0, choices=[(1, b'Yes'), (0, b'No')])),
                ('why_rocks', models.TextField(default=b'')),
                ('status', models.IntegerField(default=0)),
                ('is_share', models.BooleanField(default=False)),
                ('inappropriate_skigit', models.BooleanField(default=False)),
                ('is_plugged', models.BooleanField(default=False)),
                ('is_sperk', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('business_user', models.ForeignKey(related_name=b'skigit_business_user', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('category', models.ForeignKey(default=0, verbose_name=b'My Skigit Category', to='skigit.Category')),
                ('incentive', models.ForeignKey(blank=True, to='skigit.Incentive', null=True)),
                ('made_by', models.ForeignKey(related_name=b'video_made_by', default=0, verbose_name=b'My awesome thing was made by', to=settings.AUTH_USER_MODEL)),
                ('plugged_skigit', models.ForeignKey(related_name=b'plugged_skigit', blank=True, to='skigit.Video', null=True)),
                ('share_skigit', models.ForeignKey(related_name=b'video_detail_requests_created', blank=True, to='skigit.Video', null=True)),
                ('skigit_id', models.ForeignKey(to='skigit.Video')),
                ('subject_category', models.ForeignKey(default=0, verbose_name=b'My Subject Category', to='skigit.Subject_Category')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='thumbnail',
            name='video',
            field=models.ForeignKey(to='skigit.Video', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='share',
            name='skigit',
            field=models.ForeignKey(to='skigit.Video'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='share',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='profile',
            name='cover_img',
            field=models.OneToOneField(null=True, blank=True, to='skigit.Profile_img'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='plugged',
            name='skigit',
            field=models.ForeignKey(to='skigit.Video'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='plugged',
            name='user',
            field=models.ForeignKey(related_name=b'plugging_user', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='like',
            name='skigit',
            field=models.ForeignKey(to='skigit.Video'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='like',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='follow',
            name='skigit',
            field=models.ForeignKey(to='skigit.Video'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='follow',
            name='user',
            field=models.ForeignKey(related_name=b'following_user', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='favorite',
            name='skigit',
            field=models.ForeignKey(to='skigit.Video'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='favorite',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
