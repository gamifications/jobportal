from django.urls import path
from . import views

app_name = "payments"   

urlpatterns = [
  # path("", views.homepage, name="home"),
  path("checkout/", views.checkout, name="checkout"),
  path("create-sub/", views.create_sub, name="create-sub"), #add
  path("complete/", views.complete, name="complete"), #add
  # path("cancel/", views.cancel, name="cancel"), #add this
]