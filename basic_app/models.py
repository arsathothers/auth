from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfileInfo(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #additional
    portfolio_site = models.URLField(blank=True)
    # Below line will upload the profile pictures into profile_pics folder wich is under media folder
    profile_pic = models.ImageField(upload_to="profile_pics", blank=True)

    def __str__(self):
        # username is the default attribute for the object user
        return self.user.username