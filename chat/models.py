from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

class User(models.Model):
    name = models.CharField(max_length=20)
    phone = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.name

class Contact(models.Model):
    user = models.ForeignKey(User, related_name='friends', on_delete=models.CASCADE)
    friends = models.ManyToManyField('self', blank=True)
    
    def __str__(self):
        return self.user.name


class Message(models.Model):
    contact = models.ForeignKey(Contact, related_name = 'messages', on_delete = models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add = True )
    # picture = models.FileField(upload_to='attachments/')

    def __str__(self):
        return '[{timestamp}] {contact}: {content}'.format(**self.as_dict())
    
    def as_dict(self):
        return {'contact': self.contact, 'content': self.content, 'timestamp': self.timestamp}

class Chat(models.Model):
    participants = models.ManyToManyField(Contact, related_name='chats')
    messages = models.ManyToManyField(Message, blank=True)

    def __str__(self):
        return '{}'.format(self.pk)
