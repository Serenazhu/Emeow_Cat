import imaplib
import email
import base64
import chardet
import yaml  # To load saved login credentials from a yaml file
from my_database import Database
from datetime import datetime, timedelta
import email.utils
import os
current_dir = os.path.dirname(os.path.abspath(__file__))

# Navigate to the parent directory
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))

# Construct the path to the file in the parent directory

credential = file_path = os.path.join(parent_dir, r'gmail/credential.yml')

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

# Select the "Sent" mailbox
my_mail.select('Inbox')

# Search for all emails in the Sent folder
one_month_ago = datetime.now() - timedelta(days=30)
since_date = one_month_ago.strftime('%d-%b-%Y')

# Search for emails from the past month
_, data = my_mail.search(None, 'SINCE', since_date)
mail_id_list = data[0].split()[::-1]

msgs = []
for num in mail_id_list:
    # Fetch the email
    _, data = my_mail.fetch(num, '(RFC822)')
    msgs.append(data)

id_count = 0
payload = None
for msg in msgs[::-1]:
    print("hi")
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
                             subject, payload, time[0], actual_id)
            id_count += 1
            my_db.businesses_db()
            my_db.representatives_db()
            my_db.inbox_db()
