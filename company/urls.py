from django.conf.urls import url, include
from django.urls import path
from django.views.generic import RedirectView
from django.views.generic import TemplateView

from . import views
app_name = 'company'
urlpatterns = [
	path('', views.companyview, name='company'), #TemplateView.as_view(template_name="company/company.html"), name='company'),
	path('ajax_datatable/jobs/', views.JobsAjaxDatatableView.as_view(), name="ajax_datatable_jobs"),
    path('job/<int:pk>/', views.jobdetails, name='job'),

    path('apply/<int:pk>/', views.applyjob, name='applyjob'),

    # redirect urls such http://microsoft.localhost:8000/account/login/?next=/payment/ 
    # to http://microsoft.localhost:8000/
    # url(r'^.*', RedirectView.as_view(pattern_name='company', permanent=False)),
]