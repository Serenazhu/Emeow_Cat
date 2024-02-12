import sqlite3


class Database:
    def __init__(self, company_name, reps_name, reps_address, subject, body, time, id):
        self.company_name = company_name
        self.reps_name = reps_name
        self.reps_address = reps_address
        self.subject = subject
        self.body = body
        self.time = time
        self.id = id

    def businesses_db(self):
        conn = sqlite3.connect('emaildb.db')
        cursor = conn.cursor()

        cursor.execute(
            'SELECT * FROM Businesses WHERE Company = ?', (self.company_name,))

        # Fetch one row
        row = cursor.fetchone()
        if row is None:
            cursor.execute(
                'INSERT INTO Businesses (Company) VALUES (?)', (
                    self.company_name,)
            )
            conn.commit()
            conn.close()

    def representatives_db(self):
        conn = sqlite3.connect('emaildb.db')
        cursor = conn.cursor()

        cursor.execute(
            'SELECT * FROM Representatives WHERE Email = ?', (self.reps_address,))

        # Fetch one row
        row = cursor.fetchone()
        if row is None:
            cursor.execute(
                'INSERT INTO Representatives (Reps, Email, Company) VALUES (?, ?, ?)', (
                    self.reps_name, self.reps_address, self.company_name)
            )
            conn.commit()
            conn.close()

    def inbox_db(self):
        conn = sqlite3.connect('emaildb.db')
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM Inbox WHERE Subject = ?', (self.subject,))
        row = cursor.fetchone()
        if row is None:
            cursor.execute(
                'INSERT INTO Inbox (Email, Subject, Body, Time, Id, Reps) VALUES (?, ?, ?, ?, ?, ?)', (
                    self.reps_address, self.subject, self.body, self.time, self.id, self.reps_name)
            )
        conn.commit()
        conn.close()

    def sent(self):
        conn = sqlite3.connect('emaildb.db')
        cursor = conn.cursor()

        cursor.execute(
            'INSERT INTO Sent (Email, Subject, Body, Time, Id) VALUES (?, ?, ?, ?, ?)', (
                self.reps_address, self.subject, self.body, self.time, self.id)
        )
        conn.commit()
        conn.close()
