from member import Member
import sqlite3


class DBHelper:
    def __init__(self, dbname="twonai.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def setup(self):
        stmt = "CREATE TABLE IF NOT EXISTS members_delay (id INTEGER PRIMARY KEY, name TEXT, delay_number INTEGER DEFAULT 0, pendencies_number INTEGER DEFAULT 0)"
        self.conn.execute(stmt)
        self.conn.commit()

    def add_pending(self, member_name):
        stmt = "UPDATE members_delay SET pendencies_number = pendencies_number+1 WHERE name = (?)"
        args = (member_name, )
        self.conn.execute(stmt, args)
        self.conn.commit()

    def deleteAllPendencies(self):
        stmt = "UPDATE members_delay SET pendencies_number = 0"
        self.conn.execute(stmt)
        self.conn.commit()

    def deletePendingFrom(self, member_name):
        stmt = "UPDATE members_delay SET pendencies_number = 0 WHERE name = (?)"
        args = (member_name, )
        self.conn.execute(stmt, args)
        self.conn.commit()

    def decreasePendenciesFrom(self, member_name):
        stmt = "UPDATE members_delay SET pendencies_number = pendencies_number-1 WHERE name = (?)"
        args = (member_name, )
        self.conn.execute(stmt, args)
        self.conn.commit()

    def add_delay(self, member_name):
        stmt = "UPDATE members_delay SET delay_number = delay_number+1 WHERE name = (?)"
        args = (member_name, )
        self.conn.execute(stmt, args)
        self.conn.commit()

    def add_member(self, member_name):
        stmt = "INSERT INTO members_delay (name) VALUES (?)"
        args = (member_name, )
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_member(self, member_name):
        stmt = "DELETE FROM members_delay WHERE name = (?)"
        args = (member_name, )
        self.conn.execute(stmt, args)
        self.conn.commit()

    def deleteAllDelays(self):
        stmt = "UPDATE members_delay SET delay_number = 0"
        self.conn.execute(stmt)
        self.conn.commit()

    def deleteDelaysFrom(self, member_name):
        stmt = "UPDATE members_delay SET delay_number = 0 WHERE name = (?)"
        args = (member_name, )
        self.conn.execute(stmt, args)
        self.conn.commit()

    def decreaseDelaysFrom(self, member_name):
        stmt = "UPDATE members_delay SET delay_number = delay_number-1 WHERE name = (?)"
        args = (member_name, )
        self.conn.execute(stmt, args)
        self.conn.commit()

    def deleteAll(self):
        stmt = "DELETE FROM members_delay"
        self.conn.execute(stmt)
        self.conn.commit()

    def exists(self, name):
        stmt = "SELECT 1 FROM members_delay WHERE name = (?)"
        args = (name, )
        cursor = self.conn.execute(stmt, args)
        return cursor.fetchall() > 0

    def get_members_delay(self):
        stmt = "SELECT name, delay_number FROM members_delay"
        members = []
        cursor = self.conn.execute(stmt)
        for member in cursor:
            member = Member(member[0], member[1])
            members.append(member)
        return members