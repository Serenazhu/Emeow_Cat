from django.urls import reverse
import os
import logging
from django.shortcuts import render, redirect
from django.shortcuts import render, HttpResponse
from .models import Businesses, Representatives, Inbox, Sent
import subprocess
from django.http import JsonResponse
from .forms import CredentialForm, TypeForm
from django.http import HttpResponseRedirect
import sqlite3


def home(request):
    company = list(Businesses.objects.filter(Type=None))
    # print('hi')
    count = 0
    for _ in company:
        count += 1
    print(count)
    return render(request, "main.html", {'new_company_count': count})


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


def write_credential(cred, choose):
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Navigate to the parent directory
    parent_dir = os.path.abspath(os.path.join(current_dir, '..'))

    # Construct the path to the file in the parent directory
    if choose == 1:
        file_path = os.path.join(parent_dir, 'gmail/credential.yml')
    elif choose == 2:
        file_path = os.path.join(parent_dir, 'gpt/credential.json')

    with open(file_path, 'w') as f:
        f.write(cred)


def credential_form(request):
    if request.method == "POST":
        form = CredentialForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            key = form.cleaned_data['key']
            # api = form.cleaned_data['api']
            api = request.FILES['api']
            print(email)
            print(key)
            api = api.read()
            api = api.decode('utf-8')
            write_credential(api, choose=2)
            email = 'user: "'+email+'"'
            key = 'password: "'+key+'"'
            c = email + '\n' + key
            write_credential(c, choose=1)
            first_time = r"myapp\new_user.py"
            run = subprocess.Popen(["python", first_time])
            run.communicate()
            return redirect("main")

    else:
        form = CredentialForm()
        print('hi')

    return render(request, 'credential.html', {'form': form})


def refresh(request):
    if request.method == 'POST':
        refresh_script = r"myapp/refresh.py"
        run = subprocess.Popen(["python", refresh_script])
        run.communicate()
        return redirect("main")


def new(request):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(
        os.path.join(current_dir, os.pardir, os.pardir))
    db_path = os.path.join(parent_dir, "emaildb.db")
    print('DB PATH' + db_path)

    if request.method == 'POST':
        selected_values = {}
        for key, value in request.POST.items():
            selected_values[key] = value
        selected_values = list(selected_values.items())
        selected_values = selected_values[1:]
        print(selected_values)
        conn = sqlite3.connect(
            db_path)
        cursor = conn.cursor()
        for c, t in selected_values:
            cursor.execute('UPDATE Businesses SET Type = ? WHERE Company = ?',
                           (t, c))
        conn.commit()
        conn.close()
        return redirect("main")
    else:
        company = list(Businesses.objects.filter(Type=None))
        return render(request, 'new_companies.html', {'company': company})
