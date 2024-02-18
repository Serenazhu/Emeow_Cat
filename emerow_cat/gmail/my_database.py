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
        subject = self.subject.replace("Re: ", "")
        cursor.execute(
            'SELECT * FROM Inbox WHERE Subject = ?', (subject,))
        row = cursor.fetchone()

        if row is None:
            cursor.execute(
                'INSERT INTO Inbox (Email, Subject, Body, Time, Id, Reps) VALUES (?, ?, ?, ?, ?, ?)', (
                    self.reps_address, subject, self.body, self.time, self.id, self.reps_name)
            )

        else:
            cursor.execute(
                'DELETE FROM Inbox WHERE Subject = ?', (subject,))

            cursor.execute(
                'INSERT INTO Inbox (Email, Subject, Body, Time, Id, Reps) VALUES (?, ?, ?, ?, ?, ?)', (
                    self.reps_address, subject, self.body, self.time, self.id, self.reps_name)
            )
        conn.commit()
        conn.close()

    def sent(self):
        conn = sqlite3.connect('emaildb.db')
        cursor = conn.cursor()
        receiver_address = self.reps_address
        subject = self.subject.replace("Re: ", "")
        cursor.execute(
            'SELECT * FROM Sent WHERE Subject = ?', (subject,))
        row = cursor.fetchone()
        if row is None:
            cursor.execute(
                'INSERT INTO Sent (Email, Subject, Body, Time, Id) VALUES (?, ?, ?, ?, ?)', (
                    receiver_address, subject, self.body, self.time, self.id)
            )
        else:
            cursor.execute('DELETE FROM Sent WHERE Subject = ?',
                           (subject,))
            cursor.execute(
                'INSERT INTO Sent (Email, Subject, Body, Time, Id) VALUES (?, ?, ?, ?, ?)', (
                    receiver_address, subject, self.body, self.time, self.id)
            )

        conn.commit()
        conn.close()

    def choose(self):
        conn = sqlite3.connect('emaildb.db')
        cursor = conn.cursor()
        subject = self.subject.replace("Re: ", "")
        cursor.execute(
            'SELECT Body FROM Sent WHERE Subject = ?', (subject,))
        sent_body = cursor.fetchall()
        cursor.execute(
            'SELECT Body FROM Inbox WHERE Subject = ?', (subject,))
        inbox_body = cursor.fetchall()

        if len(sent_body) < len(inbox_body) and len(sent_body) != 0 and len(inbox_body) != 0:
            cursor.execute("UPDATE Sent SET Body = NULL")
            for body in inbox_body:
                body = body[0]
                cursor.execute(
                    'INSERT INTO Sent (Body) VALUES (?)', (body,)
                )

        elif len(inbox_body) < len(sent_body) and len(sent_body) != 0 and len(inbox_body) != 0:
            cursor.execute("UPDATE Inbox SET Body = NULL")
            for body in sent_body:
                body = body[0]
                cursor.execute(
                    'INSERT INTO Inbox (Body) VALUES (?)', (body,)
                )

        conn.commit()  # Don't forget to commit the changes
        conn.close()
