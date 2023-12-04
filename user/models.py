
from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
# Create your models here.
class UserProfiles(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    openai_token = models.CharField(max_length=255)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','password','openai_token']