from django.db import models
from django.contrib.auth.models import User

class ProfileF(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='images /', blank=True, null=True)

    def __str__(self):
        return self.user.username
