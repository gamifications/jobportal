from django.urls import include, path
from . import views
app_name='job'
urlpatterns = [
	path('', views.JobListView.as_view(), name='list'),
	path('new/', views.job_view, name='create'),
]
