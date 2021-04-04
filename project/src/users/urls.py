from django.urls import path
from . import views

#Adding URL patterns for various user authenitcation tasks. These URLS are used to request TOKEN during TEST CASES.
urlpatterns = [
    path('register/', views.register),
    path('token/', views.token),
    path('token/refresh/', views.refresh_token),
    path('token/revoke/', views.revoke_token),
]
