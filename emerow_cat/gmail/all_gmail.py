import imaplib
import email
import base64
import chardet
import sqlite3
import yaml  # To load saved login credentials from a yaml file
from my_database import Database

with open("emerow_cat\gmail\credentials.yml") as f:
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

# Search for all emails in the inbox
_, data = my_mail.search(None, 'ALL')

mail_id_list = data[0].split()[::-1]

# Limit the number of emails to fetch to 30
mail_id_list = mail_id_list[:30]

msgs = []  # empty list to capture all messages
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
            print("_________________________________________")
            email_address = []
            name = []
            company = []
            time = []
            time.append(my_msg["date"])
            for i, c in enumerate(my_msg['from']):
                if c == '<':
                    email_address.append(my_msg['from'][i+1:-1])
                    name.append(my_msg['from'][:i])
            print("subj:", my_msg['subject'])
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

            print(reps_address)
            print(reps_name)
            print(company_name)
            print("body:")
            print("date:" + my_msg.get("Date"))
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

            my_db = Database(company_name, reps_name, reps_address,
                             subject, payload, time[0], actual_id)
            id_count += 1
            my_db.businesses_db()
            my_db.representatives_db()
            my_db.inbox_db()
