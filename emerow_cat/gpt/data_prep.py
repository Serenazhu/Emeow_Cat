import json
import sqlite3


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
        cursor1.execute(
            'SELECT Reps FROM Representatives WHERE Company = ?', (company,))
        cursor2.execute(
            'SELECT Email FROM Representatives WHERE Company = ?', (company,))
        reps = cursor1.fetchall()
        emails = cursor2.fetchall()
        n = 1
        for rep, email in zip(reps, emails):
            Representatives[n] = {}
            Representatives[n]['rep'] = rep[0]
            Representatives[n]['email'] = email[0]
            n += 1

        # Inbox
        cursor1.execute(
            'SELECT Email FROM Inbox WHERE Company = ?', (company,))
        cursor2.execute(
            'SELECT Subject FROM Inbox WHERE Company = ?', (company,))
        cursor3.execute('SELECT Body FROM Inbox WHERE Company = ?', (company,))
        cursor4.execute('SELECT Time FROM Inbox WHERE Company = ?', (company,))
        cursor5.execute('SELECT Reps FROM Inbox WHERE Company = ?', (company,))

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
# def generate_paragraph(data):
#     businesses = data.get("Businesses", {})
#     representatives = data.get("Representatives", {})
#     inbox = data.get("Inbox", {})
#     sent = data.get("Sent", {})

#     business_info = ", ".join(
#         [f"{business}: {role}" for business, role in businesses.items()])

#     representatives_info = ""
#     for rep_id, rep_data in representatives.items():
#         representatives_info += f"{rep_data['rep']} can be reached at {rep_data['email']} representing {rep_data['company']}. "

#     inbox_info = ""
#     for email_id, email_data in inbox.items():
#         inbox_info += f"Received an email with subject '{email_data['subject']}' from {email_data['email']} on {email_data['time']}. "

#     sent_info = ""
#     for email_id, email_data in sent.items():
#         sent_info += f"Sent an email with subject '{email_data['subject']}' to {email_data['email']} on {email_data['time']}. "


#     paragraph = f"In this dataset, there are {len(businesses)} businesses involved: {business_info}. "
#     paragraph += f"The representatives associated with these businesses are {representatives_info} "
#     paragraph += f"The inbox contains {len(inbox)} emails. {inbox_info} "
#     paragraph += f"There are also {len(sent)} sent emails. {sent_info}"
#     return paragraph
# Call the function to retrieve data
all_data = prep_data()
# Save all data to a single text file
with open('emerow_cat\gpt\email_data.txt', 'w') as f:
    json.dump(all_data, f)
    # for category, data in all_data.items():
    #     f.write(f"{category}:\n")
    #     if isinstance(data, dict):
    #         for key, values in data.items():
    #             f.write(f"\t{key}:\n")
    #             if isinstance(values, dict):
    #                 for k, v in values.items():
    #                     f.write(f"\t\t{k}: {v}\n")
    #             else:
    #                 f.write(f"\t\t{values}\n")
    #     else:
    #         f.write(f"\t{data}\n")
