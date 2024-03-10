import sqlite3
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

# Navigate to the parent directory
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))

# Construct the path to the file in the parent directory
parent_dir = os.path.abspath(os.path.join(parent_dir, '..'))

db_path = os.path.join(
    parent_dir, "emaildb.db")


print("PATH: " + db_path)


class Database:

    def __init__(self, company_name, reps_name, reps_address, subject, body, time, n):
        self.company_name = company_name
        self.reps_name = reps_name
        self.reps_address = reps_address
        self.subject = subject
        self.body = body
        self.time = time
        self.n = n

    def businesses_db(self):
        Businesses = {}
        conn = sqlite3.connect(
            db_path)
        cursor = conn.cursor()

        cursor.execute(
            'SELECT * FROM Businesses WHERE Company = ?', (self.company_name,))

        # Fetch one row
        row = cursor.fetchone()
        if row is None:
            Businesses[self.company_name] = "Client"
            cursor.execute(
                'INSERT INTO Businesses (Company) VALUES (?)', (
                    self.company_name,)
            )
            conn.commit()

        return Businesses

    def representatives_db(self):
        Representatives = {}
        conn = sqlite3.connect(
            db_path)
        cursor = conn.cursor()

        cursor.execute(
            'SELECT * FROM Representatives WHERE Email = ?', (self.reps_address,))

        # Fetch one row
        row = cursor.fetchone()
        if row is None:
            Representatives.setdefault(self.company_name, []).append(
                {'rep': self.reps_name, 'email': self.reps_address})
            cursor.execute(
                'INSERT INTO Representatives (Reps, Email, Company) VALUES (?, ?, ?)', (
                    self.reps_name, self.reps_address, self.company_name)
            )
            conn.commit()

        return Representatives

    def inbox_db(self):
        Inbox = {}
        conn = sqlite3.connect(
            db_path)
        cursor = conn.cursor()
        subject = self.subject.replace("Re: ", "")
        cursor.execute(
            'SELECT * FROM Inbox WHERE Subject = ?', (subject,))
        row = cursor.fetchone()

        if row is None:
            Inbox['email'] = self.reps_address
            Inbox['subject'] = subject
            Inbox['body'] = self.body
            Inbox['time'] = self.time
            Inbox['rep'] = self.reps_name
            cursor.execute(
                'INSERT INTO Inbox (Email, Subject, Body, Time, Reps, Company) VALUES (?, ?, ?, ?, ?, ?)', (
                    self.reps_address, subject, self.body, self.time, self.reps_name, self.company_name)
            )

            conn.commit()

        return Inbox

    def sent(self):
        Sent = {}
        conn = sqlite3.connect(
            db_path)
        cursor = conn.cursor()
        receiver_address = self.reps_address
        subject = self.subject.replace("Re: ", "")
        cursor.execute(
            'SELECT * FROM Sent WHERE Subject = ?', (subject,))
        row = cursor.fetchone()
        if row is None:
            Sent['email'] = receiver_address
            Sent['subject'] = subject
            Sent['body'] = self.body
            Sent['time'] = self.time
            Sent['rep'] = self.reps_name
            cursor.execute(
                'INSERT INTO Sent (Email, Subject, Body, Time) VALUES (?, ?, ?, ?)', (
                    receiver_address, subject, self.body, self.time, )
            )

            conn.commit()
            conn.close()
        return Sent
