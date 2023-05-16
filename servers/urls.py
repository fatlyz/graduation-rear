from django.urls import path
from servers import views

urlpatterns = [
    path('login/',views.login),
    path('register/',views.register),
    path('getinfo/',views.getinfo),
    path('search/',views.search),
    path('getuplist/',views.getuplist)
]