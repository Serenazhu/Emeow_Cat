from django.urls import reverse
import os
import logging
from django.shortcuts import render, redirect
from django.shortcuts import render, HttpResponse
from .models import Businesses, Representatives, Inbox, Sent
import json
from django.http import JsonResponse
from .forms import CredentialForm
from django.http import HttpResponseRedirect


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
    return render(request, "mail.html", {'subjects': email_subject, 'emails': emails, 'email_body': html_body, 'tf': "From: "})


def outbox(request):
    emails = Sent.objects.all()
    return render(request, "outbox.html", {'emails': emails})


def outbox_mail(request):
    email_subject = request.GET.get('subject')
    print("SUBJECT " + email_subject)
    emails = Sent.objects.filter(Subject=email_subject)
    for email in emails:
        email_body = email.Body
        html_body = email_body.replace('\n', '<br>')
        # print(email.Body)
    return render(request, "mail.html", {'subjects': email_subject, 'emails': emails, 'email_body': html_body, 'tf': "To: "})


def write_credential(cred):
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Navigate to the parent directory
    parent_dir = os.path.abspath(os.path.join(current_dir, '..'))

    # Construct the path to the file in the parent directory
    file_path = os.path.join(parent_dir, 'gmail/credential.yml')

    with open(file_path, 'w') as f:
        f.write(cred)


def credential_form(request):
    if request.method == "POST":
        form = CredentialForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            key = form.cleaned_data['key']
            file = form.cleaned_data['file']
            print(email)
            print(key)
            print(file)
            email = 'user: "'+email+'"'
            key = 'password: "'+key+'"'
            c = email + '\n' + key
            write_credential(c)
            return redirect("main")

    else:
        form = CredentialForm()
        print('hi')

    return render(request, 'credential.html', {'form': form})
