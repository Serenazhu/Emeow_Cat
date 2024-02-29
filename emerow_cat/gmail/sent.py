import imaplib
import email
import base64
import chardet
from my_database import Database

# Gmail IMAP server details
IMAP_SERVER = 'imap.gmail.com'
IMAP_PORT = 993

# Your Gmail credentials
EMAIL = 't6264269796@gmail.com'
PASSWORD = 'lcnnbnvlzztfysqd'

# Connect to Gmail server
mail = imaplib.IMAP4_SSL(IMAP_SERVER)
mail.login(EMAIL, PASSWORD)

# Select the "Sent" mailbox
mail.select('"[Gmail]/Sent Mail"')

# Search for all emails in the Sent folder
result, data = mail.search(None, 'ALL')
mail_id_list = data[0].split()[::-1]

# Limit the number of emails to fetch to 30
mail_id_list = mail_id_list[:30]

msgs = []
for num in mail_id_list:
    # Fetch the email
    type, data = mail.fetch(num, '(RFC822)')
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
                             subject, payload, time[0], actual_id)
            id_count += 1
            my_db.sent()
            my_db.choose()
