from django.urls import include, path
from . import views
app_name='job'
urlpatterns = [
	path('', views.JobListView.as_view(), name='list'),
	# path('new/', views.job_view, name='job'),
	path('new/', views.JobView.as_view(), name='job'),
	path('edit/<int:pk>/', views.JobView.as_view(), name='edit'),
	
	path('create/', views.MyUpdateView.as_view(), name='create'),
	path('update/<int:pk>/', views.MyUpdateView.as_view(), name='update'),
]
