from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('reps/', views.reps_list, name="reps"),
    path('inbox/', views.inbox, name="inbox"),
    path('companies/', views.company_list, name="companies"),
    path('mail/', views.mail, name="mail")
]
