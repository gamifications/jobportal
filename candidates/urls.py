from django.conf.urls import url, include
from django.urls import path
from django.views.generic import RedirectView
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', views.applyjob, name='applyjob'),
    path('viewjob/', TemplateView.as_view(template_name="view_job.html"), name='viewjob'),

    # redirect urls such http://microsoft.localhost:8000/account/login/?next=/payment/ 
    # to http://microsoft.localhost:8000/
    url(r'^.*', RedirectView.as_view(pattern_name='applyjob', permanent=False)),
]