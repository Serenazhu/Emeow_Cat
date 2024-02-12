from django.shortcuts import render, HttpResponse
from .models import Businesses, Representatives, Inbox
import json
from django.http import JsonResponse


def home(request):
    return render(request, "main.html")


def company_list(request):
    type = request.GET.get('type')
    print(type)
    company = Businesses.objects.filter(Type=type)
    print(company)
    return render(request, 'companies.html', {'company': company})


def reps_list(request):
    company_name = request.GET.get('name')
    print(company_name)
    representatives = Representatives.objects.filter(Company=company_name)
    return render(request, 'reps.html', {'representatives': representatives})


def inbox(request):
    email_address = request.GET.get('email')
    emails = Inbox.objects.filter(Email=email_address)
    return render(request, "inbox.html", {'emails': emails})


def mail(request):
    email_subject = request.GET.get('subject')
    print("SUBJECT " + email_subject)
    emails = Inbox.objects.filter(Subject=email_subject)
    for email in emails:
        email_body = email.Body
        html_body = email_body.replace('\n', '<br>')
        # print(email.Body)
    return render(request, "mail.html", {'subjects': email_subject, 'emails': emails, 'email_body': html_body})
