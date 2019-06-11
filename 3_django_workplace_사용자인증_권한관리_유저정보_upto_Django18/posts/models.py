from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.conf import settings

# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    # image = models.ImageField(blank=True)
    image = ProcessedImageField(
        upload_to = 'posts/images/',
        processors = [ResizeToFill(300,300)],
        format = 'JPEG',
        options = {'quality':90},
    )
    created_at = models.DateTimeField(auto_now_add= True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

