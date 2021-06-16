from django.contrib import admin

# Register your models here.
from django.contrib.auth import get_user_model
from .models import Tag,Keyword, Candidate

User = get_user_model()

admin.site.register(User)
admin.site.register(Keyword)
admin.site.register(Tag)

admin.site.register(Candidate)
