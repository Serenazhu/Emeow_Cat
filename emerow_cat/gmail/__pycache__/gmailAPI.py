import re
import base64
import email
import dateutil.parser
from googleapiclient.errors import HttpError
from Google import Create_Service  # Adjust this import as needed


def decode_message(raw_message):
    try:
        message_str = base64.urlsafe_b64decode(
            raw_message['raw'].encode('ASCII')).decode('utf-8')
        parsed_message = email.message_from_string(message_str)

        sender = parsed_message['From']
        subject = parsed_message['Subject']
        time = parsed_message['Date']

        # Extracting the body of the email
        body = ""
        if parsed_message.is_multipart():
            for part in parsed_message.walk():
                if part.get_content_type() == "text/plain":
                    body += part.get_payload(decode=True).decode('utf-8')
        else:
            body = parsed_message.get_payload(decode=True).decode('utf-8')

        return sender, subject, time, body
    except Exception as e:
        print(f"An error occurred decoding the message: {e}")
        return None, None, None, None


def convert_to_local_time(utc_time):
    try:
        parsed_time = dateutil.parser.parse(utc_time)
        local_time = parsed_time.astimezone()
        return local_time.strftime("%Y-%m-%d %H:%M")
    except Exception as e:
        print(f"An error occurred converting time to local timezone: {e}")
        return None


CLIENT_SECRET_FILE = 'c2.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']
service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)


def get_last_20_emails(service):
    try:
        response = service.users().messages().list(
            userId='me', maxResults=11).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        emails_info = []
        for message in messages:
            m_id = message['id']
            full_message = service.users().messages().get(
                userId='me', id=m_id, format='raw').execute()
            sender, subject, utc_time, body = decode_message(full_message)
            local_time = convert_to_local_time(utc_time)
            emails_info.append({
                'sender': sender,
                'subject': subject,
                'time': local_time,
                'body': body
            })

        return emails_info
    except HttpError as error:
        print(f'An error occurred while retrieving emails: {error}')
        return []


# Retrieve and print the information for the last 20 emails
emails_info = get_last_20_emails(service)
for info in emails_info:
    print("Sender:", info['sender'])
    print("Subject:", info['subject'])
    print("Time:", info['time'])
    print("Body:", info['body'])
    print()


def clean_sender_name(sender):
    # Remove any leading or trailing spaces
    sender = sender.strip()

    # Remove any double quotes
    sender = sender.replace('"', '')

    # Remove any extra characters from the sender name
    # These might be due to encoding or formatting issues
    sender_parts = sender.split('-')
    cleaned_sender = '-'.join(part.strip() for part in sender_parts)

    return cleaned_sender


def write_emails_info_to_file(emails_info, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            for info in emails_info:
                sender = clean_sender_name(info['sender'])
                line = f"{sender} - {info['subject']}\n"
                file.write(line)
        print(f"Emails information written to '{file_path}' successfully.")
    except Exception as e:
        print(f"An error occurred while writing to file: {e}")


def remove_lines_with_leading_space(file_path):
    # Read the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Remove lines with leading spaces
    lines = [line for line in lines if not re.match(r'^\s', line)]

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)


# Example usage:
file_path = 'first11.txt'
write_emails_info_to_file(emails_info, file_path)
remove_lines_with_leading_space(file_path)
