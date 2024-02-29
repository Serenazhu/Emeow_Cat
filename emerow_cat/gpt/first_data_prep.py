import sqlite3


def businesses_db():
    Businesses = {}
    conn = sqlite3.connect(
        'emaildb.db')
    cursor = conn.cursor()

    cursor.execute(
        'SELECT * FROM Businesses')

    # Fetch one row
    rows = cursor.fetchall()
    for row in rows:
        company = row[0]
        type = row[1]
        Businesses[company] = type
        conn.commit()
        conn.close()
    return Businesses


def representatives_db():
    Representatives = {}
    conn = sqlite3.connect(
        'emaildb.db')
    cursor = conn.cursor()

    cursor.execute(
        'SELECT * FROM Representatives')

    # Fetch one row
    rows = cursor.fetchall()
    for row in rows:
        rep_name = row[0]
        email = row[1]
        company = row[2]
        Representatives.setdefault(company, []).append(
            {'rep': rep_name, 'email': email})

    conn.commit()
    conn.close()
    return Representatives


def inbox_db():
    Inbox = {}
    conn = sqlite3.connect(
        'emaildb.db')
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM Inbox')
    rows = cursor.fetchall()

    for row in rows:
        email = row[0]
        subject = row[1]
        body = row[2]
        time = row[3]
        reps = row[5]
        Inbox['email'] = email
        Inbox['subject'] = subject
        Inbox['body'] = body
        Inbox['time'] = time
        Inbox['rep'] = reps

    conn.commit()
    conn.close()

    return Inbox


def sent():
    Sent = {}
    conn = sqlite3.connect(
        'emaildb.db')
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM Sent')
    rows = cursor.fetchall()
    for row in rows:
        email = row[0]
        subject = row[1]
        body = row[2]
        time = row[3]
        Sent['email'] = email
        Sent['subject'] = subject
        Sent['body'] = body
        Sent['time'] = time
        # Sent['rep'] = reps_name

    conn.commit()
    conn.close()
    return Sent


Businesses = businesses_db()
Representatives = representatives_db()
Inbox = inbox_db()
Sent = sent()

all_data = {
    "Businesses": Businesses,
    "Representatives": Representatives,
    "Inbox": Inbox,
    "Sent": Sent
}
