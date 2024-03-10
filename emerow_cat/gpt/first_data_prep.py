import imaplib
import email
import base64
import chardet
import yaml  # To load saved login credentials from a yaml file
from my_database import Database
from datetime import datetime
import email.utils
import json
import os


def data_prep_1():
    n = 0
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Navigate to the parent directory
    parent_dir = os.path.abspath(os.path.join(current_dir, '..'))

    # Construct the path to the file in the parent directory

    credential = os.path.join(
        parent_dir, 'gmail\credential.yml')

    with open(credential) as f:
        content = f.read()

    # from credentials.yml import user name and password
    my_credentials = yaml.load(content, Loader=yaml.FullLoader)

    # Load the user name and passwd from yaml file
    user, password = my_credentials["user"], my_credentials["password"]

    # URL for IMAP connection
    imap_url = 'imap.gmail.com'

    # Connection with GMAIL using SSL
    my_mail = imaplib.IMAP4_SSL(imap_url)

    # Log in using your credentials
    my_mail.login(user, password)

    # Select the Inbox to fetch messages
    my_mail.select('Inbox')

    Businesses = {}
    Representatives = {}
    Inbox = {}
    Sent = {}
    # Search for all emails in the inbox
    _, data = my_mail.search(None, 'ALL')

    mail_id_list = data[0].split()[::-1]

    # Limit the number of emails to fetch to 30
    mail_id_list = mail_id_list[:30]

    msgs = []
    # Iterate through messages and extract data into the msgs list
    for num in mail_id_list:
        # RFC822 returns whole message (BODY fetches just body)
        typ, data = my_mail.fetch(num, '(RFC822)')
        msgs.append(data)

    # Now we have all messages, but with a lot of details
    # Let us extract the right text and print on the screen

    # In a multipart e-mail, email.message.Message.get_payload() returns a
    # list with one item for each part. The easiest way is to walk the message
    # and get the payload on each part:
    # https://stackoverflow.com/questions/1463074/how-can-i-get-an-email-messages-text-content-using-python

    # NOTE that a Message object consists of headers and payloads.
    id_count = 0
    payload = None
    for msg in msgs[::-1]:
        for response_part in msg:
            if type(response_part) is tuple:
                my_msg = email.message_from_bytes((response_part[1]))
                # print("_________________________________________")
                email_address = []
                name = []
                company = []
                # time = []
                # time.append(my_msg["date"])
                time = email.utils.parsedate_to_datetime(my_msg["date"])
                for i, c in enumerate(my_msg['from']):
                    if c == '<':
                        email_address.append(my_msg['from'][i+1:-1])
                        name.append(my_msg['from'][:i])
                # print("subj:", my_msg['subject'])
                subject = my_msg['subject']
                # print("from:", my_msg['from'])
                reps_address = email_address[0]
                for i, c in enumerate(reps_address):
                    if c == '@':
                        company.append(reps_address[i+1:-4])
                reps_name = name[0]
                reps_address = email_address[0]
                company_name = company[0]
                date = my_msg.get("Date")
                time = []
                count = 0
                for i, c in enumerate(date):
                    if c == ":":
                        count += 1
                    if count == 2:
                        time.append(date[:i])

                # print(reps_address)
                # print(reps_name)
                # print(company_name)
                # print("body:")
                # print("date:" + my_msg.get("Date"))
                if my_msg.get("In-Reply-To") or my_msg.get("References"):
                    print("THIS MSG IS A REPLY")

                for part in my_msg.walk():
                    # print(part.get_content_type())
                    if part.get_content_type() == 'text/plain':
                        payload = part.get_payload()
                        if part['Content-Transfer-Encoding'] == 'base64':
                            payload = base64.b64decode(payload)
                            try:
                                encoding = chardet.detect(payload)['encoding']
                                payload = payload.decode(encoding)
                            except UnicodeDecodeError:
                                payload = payload.decode('iso-8859-1')
                        # print(payload)
                mail_id = str(mail_id_list[id_count])
                clean_id = []
                c = 0
                for i in mail_id:
                    if c == 0 or c == 1 or c == 6:
                        c += 1
                        continue
                    else:
                        clean_id.append(i)
                        c += 1
                actual_id = str(''.join(clean_id))

                my_db = Database(company_name, reps_name, reps_address,
                                 subject, payload, time[0], n)
                id_count += 1

                a = my_db.businesses_db()
                if a:
                    Businesses[n] = a

                b = my_db.representatives_db()
                if b:
                    Representatives[n] = b

                c = my_db.inbox_db()
                if c:
                    Inbox[n] = c
                n += 1

    IMAP_PORT = 993

    mail = imaplib.IMAP4_SSL(imap_url)
    mail.login(user, password)
    mail.select('"[Gmail]/Sent Mail"')

    # Search for all emails in the Sent folder
    result, data = mail.search(None, 'ALL')
    mail_id_list = data[0].split()[::-1]

    # Limit the number of emails to fetch to 30
    mail_id_list = mail_id_list[:30]

    msgs = []
    for num in mail_id_list:
        # Fetch the email
        typ, data = mail.fetch(num, '(RFC822)')
        msgs.append(data)

    id_count = 0
    payload = None
    for msg in msgs[::-1]:
        for response_part in msg:
            if isinstance(response_part, tuple):
                my_msg = email.message_from_bytes((response_part[1]))
                print("_________________________________________")
                email_address = []
                name = []
                company = []
                time = []
                time.append(my_msg["date"])
                receiver_address = my_msg['To']
                print("TO" + my_msg['To'])
                print("subj:", my_msg['subject'])
                subject = my_msg['subject']
                date = my_msg.get("Date")
                time = []
                count = 0
                for i, c in enumerate(date):
                    if c == ":":
                        count += 1
                    if count == 2:
                        time.append(date[:i])

                print("date:" + my_msg.get("Date"))
                if my_msg.get("In-Reply-To") or my_msg.get("References"):
                    print("THIS MSG IS A REPLY")

                for part in my_msg.walk():
                    if part.get_content_type() == 'text/plain':
                        payload = part.get_payload()
                        if part['Content-Transfer-Encoding'] == 'base64':
                            payload = base64.b64decode(payload)
                            try:
                                encoding = chardet.detect(payload)['encoding']
                                payload = payload.decode(encoding)
                            except UnicodeDecodeError:
                                payload = payload.decode('iso-8859-1')
                        print(payload)
                mail_id = str(mail_id_list[id_count])
                clean_id = []
                c = 0
                for i in mail_id:
                    if c == 0 or c == 1 or c == 6:
                        c += 1
                        continue
                    else:
                        clean_id.append(i)
                        c += 1
                actual_id = str(''.join(clean_id))

                my_db = Database(None, None, receiver_address,
                                 subject, payload, time[0], n)
                id_count += 1
                s = my_db.sent()
                Sent[n] = s

    all_data = {
        "Businesses": Businesses,
        "Representatives": Representatives,
        "Inbox": Inbox,
        "Sent": Sent
    }
    print(all_data)
    with open('emerow_cat\gpt\email_data.txt', 'w') as f:
        json.dump(all_data, f)
