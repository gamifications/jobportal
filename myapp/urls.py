from django.urls import include, path
from .views import job, accountsettings
app_name='job'
urlpatterns = [
	path('', job.JobListView.as_view(), name='list'),
	path('create/', job.JobView.as_view(), name='create'),
	path('view/<int:pk>/', job.JobDetailView.as_view(), name='view'),
	path('edit/<int:pk>/', job.JobView.as_view(), name='edit'),
	path('delete/<int:pk>/', job.JobDeleteView.as_view(), name='delete'),

	path('settings/', accountsettings.Profile.as_view(), name='profile'),
	# path("settings/", accountsettings.profile, name="profile"),
	path("settings/billing/", accountsettings.billing, name="billing"),
	path("settings/company/", accountsettings.CompanyView.as_view(), name="company"),
]
