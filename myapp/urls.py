from django.urls import include, path
from . import views
app_name='job'
urlpatterns = [
	path('', views.JobListView.as_view(), name='list'),
	path('create/', views.JobView.as_view(), name='create'),
	path('edit/<int:pk>/', views.JobView.as_view(), name='edit'),
	path('delete/<int:pk>/', views.JobDeleteView.as_view(), name='delete'),

]
