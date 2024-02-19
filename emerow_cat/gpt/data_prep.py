import json
import sqlite3


def prep_data():
    Businesses = {}
    Representatives = {}
    Inbox = {}
    Sent = {}
    conn = sqlite3.connect(
        r'C:\Users\seren\OneDrive\Documents\Emeow_cat\emeow_cat_web\emaildb.db')
    cursor1 = conn.cursor()
    cursor2 = conn.cursor()
    cursor3 = conn.cursor()
    cursor4 = conn.cursor()
    cursor5 = conn.cursor()

    # Business
    cursor1.execute('SELECT Company FROM Businesses')
    companies = cursor1.fetchall()
    cursor2.execute('SELECT Type FROM Businesses')
    types = cursor2.fetchall()

    for company, type in zip(companies, types):
        Businesses[company[0]] = type[0]

    # Representatives
    cursor1.execute('SELECT Reps FROM Representatives')
    cursor2.execute('SELECT Email FROM Representatives')
    cursor3.execute('SELECT Company FROM Representatives')
    reps = cursor1.fetchall()
    emails = cursor2.fetchall()
    companies = cursor3.fetchall()
    n = 1
    for rep, email, company in zip(reps, emails, companies):
        Representatives[n] = {}
        Representatives[n]['rep'] = rep[0]
        Representatives[n]['email'] = email[0]
        Representatives[n]['company'] = company[0]
        n += 1

    # Inbox
    cursor1.execute('SELECT Email FROM Inbox')
    cursor2.execute('SELECT Subject FROM Inbox')
    cursor3.execute('SELECT Body FROM Inbox')
    cursor4.execute('SELECT Time FROM Inbox')
    cursor5.execute('SELECT Reps FROM Inbox')

    emails = cursor1.fetchall()
    subjects = cursor2.fetchall()
    bodies = cursor3.fetchall()
    times = cursor4.fetchall()
    reps = cursor5.fetchall()

    n = 1
    for email, subject, body, time, rep in zip(emails, subjects, bodies, times, reps):
        Inbox[n] = {}
        Inbox[n]['email'] = email[0]
        Inbox[n]['subject'] = subject[0]
        Inbox[n]['body'] = body[0]
        Inbox[n]['time'] = time[0]
        Inbox[n]['rep'] = rep[0]
        n += 1

    # Sent
    cursor1.execute('SELECT Email FROM Sent')
    cursor2.execute('SELECT Subject FROM Sent')
    cursor3.execute('SELECT Body FROM Sent')
    cursor4.execute('SELECT Time FROM Sent')

    emails = cursor1.fetchall()
    subjects = cursor2.fetchall()
    bodies = cursor3.fetchall()
    times = cursor4.fetchall()

    n = 1
    for email, subject, body, time in zip(emails, subjects, bodies, times):
        Sent[n] = {}
        Sent[n]['email'] = email[0]
        Sent[n]['subject'] = subject[0]
        Sent[n]['body'] = body[0]
        Sent[n]['time'] = time[0]
        n += 1

    cursor1.close()
    cursor2.close()
    cursor3.close()
    cursor4.close()
    cursor5.close()
    conn.close()

    # Combine all dictionaries into one
    all_data = {
        "Businesses": Businesses,
        "Representatives": Representatives,
        "Inbox": Inbox,
        "Sent": Sent
    }

    return all_data


# Call the function to retrieve data
all_data = prep_data()
# print(all_data)

# Save all data to a single JSON file
with open('emerow_cat\gpt\email_data.json', 'w') as f:
    json.dump(all_data, f, indent=4)
