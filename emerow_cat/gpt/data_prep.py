import sqlite3
import json


def prep_data():
    conn = sqlite3.connect(
        r'C:\Users\seren\OneDrive\Documents\Emeow_cat\emeow_cat_web\emaildb.db')
    cursor1 = conn.cursor()

    Businesses = {}
    Representatives = {}
    Inbox = {}
    Sent = {}

    # Business
    cursor1.execute('SELECT Company, Type FROM Businesses')
    for company, type in cursor1.fetchall():
        Businesses[company] = type

    # Representatives
    cursor1.execute('SELECT Company, Reps, Email FROM Representatives')
    for company, rep, email in cursor1.fetchall():
        Representatives.setdefault(company, []).append(
            {'rep': rep, 'email': email})

    # Inbox
    cursor1.execute(
        'SELECT Company, Email, Subject, Body, Time, Reps FROM Inbox')
    for company, email, subject, body, time, rep in cursor1.fetchall():
        Inbox.setdefault(company, []).append(
            {'email': email, 'subject': subject, 'body': body, 'time': time, 'rep': rep})

    # Sent
    cursor1.execute('SELECT Email, Subject, Body, Time FROM Sent')
    for email, subject, body, time in cursor1.fetchall():
        Sent.setdefault('Sent', []).append(
            {'email': email, 'subject': subject, 'body': body, 'time': time})

    all_data = {
        "Businesses": Businesses,
        "Representatives": Representatives,
        "Inbox": Inbox,
        "Sent": Sent
    }

    return all_data


try:
    with open('emerow_cat\gpt\email_data.txt', 'r') as f:
        existing_data = json.load(f)
except FileNotFoundError:
    existing_data = {}

# Prepare new data
new_data = prep_data()
temp = {}
# Check for new entries and add them to existing data
for key, value in new_data.items():
    for sub_key, sub_value in value.items():
        if sub_key not in existing_data.get(key, {}):
            if key not in temp:
                temp[key] = {}
            temp[key][sub_key] = sub_value
            print(key)
            print(sub_key)
            print(sub_value)

# Save updated data to file
with open('emerow_cat\gpt\email_data.txt', 'w') as f:
    json.dump(new_data, f)
if temp:
    with open('emerow_cat\gpt\email_data_new.txt', 'w') as f:
        json.dump(temp, f)
