from django.contrib import admin

# Register your models here.
from django.contrib.auth import get_user_model
from .models import Tag,Keyword

User = get_user_model()

admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Keyword)