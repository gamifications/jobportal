from django.urls import include, path
from .views import Profile

urlpatterns = [
	path('', Profile.as_view(), name='home'),
]
