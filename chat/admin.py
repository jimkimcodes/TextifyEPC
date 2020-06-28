from django.contrib import admin
from .models import Message, User, Chat, Contact

# Register your models here.
admin.site.register(User)
admin.site.register(Contact)
admin.site.register(Message)
admin.site.register(Chat)
