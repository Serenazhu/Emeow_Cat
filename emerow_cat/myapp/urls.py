from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name="main"),
    path('reps/', views.reps_list, name="reps"),
    path('inbox/', views.inbox, name="inbox"),
    path('companies/', views.company_list, name="companies"),
    path('mail/', views.mail, name="mail"),
    path('outbox/', views.outbox, name="outbox"),
    path('outbox_mail/', views.outbox_mail, name="outbox_mail"),
    path('credentials/', views.credential_form, name="credentials"),
    path('refresh/', views.refresh, name="refresh"),
    path('new/', views.new, name="new")
]
