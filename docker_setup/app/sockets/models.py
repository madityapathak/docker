from django.db import models
from django.conf import settings


class ChatRoom(models.Model):
    participant1=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='participant1')
    participant2=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='participant2')


