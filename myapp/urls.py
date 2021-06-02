from django.urls import include, path
from . import views
app_name='job'
urlpatterns = [
	path('', views.JobListView.as_view(), name='list'),
	path('new/', views.JobCreateView.as_view(), name='create'),
]
