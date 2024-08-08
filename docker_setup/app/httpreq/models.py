from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token




def get_profile_image_filepath(self, filename):
	return 'profile_images/' + str(self.pk) + '/profile_image.png'

def get_default_profile_image():
	return "webchat/default_profile_image.png"



class User(AbstractUser):
    email=models.EmailField(unique=True)
    profile_image=models.ImageField(max_length=255, upload_to=get_profile_image_filepath, null=True, blank=True, default=get_default_profile_image)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def set_profile_image_to_default(self):
        self.profile_image.delete()
        self.profile_image = get_default_profile_image()
        self.save()