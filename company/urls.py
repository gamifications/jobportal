from django.conf.urls import url, include
from django.urls import path
from django.views.generic import RedirectView
from django.views.generic import TemplateView

from . import views

urlpatterns = [
	path('', TemplateView.as_view(template_name="company/company.html"), name='company'),
    path('applyjob/', views.applyjob, name='applyjob'),

    # redirect urls such http://microsoft.localhost:8000/account/login/?next=/payment/ 
    # to http://microsoft.localhost:8000/
    url(r'^.*', RedirectView.as_view(pattern_name='company', permanent=False)),
]