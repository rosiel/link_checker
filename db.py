#!/Users/rlefaive/.venv/bin/python
import sqlite3


class DB:
    def __init__(self, database):
        self.con = sqlite3.connect(database)
        self.con.row_factory = sqlite3.Row
        self.cur = self.con.cursor()
        self.initialize_tables()

    def __del__(self):
        self.con.close()

    def initialize_tables(self):
        # Link table
        try:
            r = self.cur.execute("PRAGMA table_info(link)")
            if r.fetchone() is None:
                self.con.execute("CREATE TABLE link(id INTEGER PRIMARY KEY NOT NULL, "
                                 "record INTEGER, url TEXT, ind2 INT)")
                self.con.commit()
        except sqlite3.OperationalError:
            print("Operational error.")
            exit(1)

        # Response table
        try:
            r = self.cur.execute("PRAGMA table_info(response)")
            if r.fetchone() is None:
                self.con.execute("CREATE TABLE response(id INTEGER PRIMARY KEY NOT NULL, link INTEGER, "
                                 "timestamp TEXT, status_code TEXT, final_url TEXT, has_title TEXT)")
                self.con.commit()
        except sqlite3.OperationalError:
            print('Operational error')
            exit(1)

    def add_link(self, row):
        default_data = {'record': '', 'url': '', 'ind2': ''}
        row = {**default_data, **row}
        print(row)
        self.cur.execute("SELECT id FROM link WHERE url = ? and record = ?", (row['url'], row['record']))
        if self.cur.fetchone() is None:
            self.cur.execute("INSERT INTO link (record, url, ind2) VALUES(:record, :url, :ind2)", row)
            print('Adding row [{}]'.format(row))
        else:
            print("Not adding link, already in database. [{}]".format(row['url']))
        self.con.commit()

    def add_links(self, rows):
        for row in rows:
            self.add_link(row)

    def get_links(self, batch=100):
        links = self.cur.execute("SELECT * FROM link WHERE id NOT IN (SELECT link FROM response) limit ?", (batch,))
        return links.fetchall()

    def add_response(self, data):
        self.cur.execute("INSERT INTO response (link, timestamp, status_code, final_url) "
                         "VALUES(:link, datetime('now', 'localtime'), :status_code, :final_url)", data)
        self.con.commit()

    def get_responses(self, timestamp='1900-01-01'):
        responses = self.cur.execute("SELECT link.id, link.record, link.url, "
                                     "response.status_code, response.final_url, response.timestamp "
                                     "FROM link JOIN response ON link.id = response.link "
                                     "WHERE timestamp > ?", (timestamp,))
        return responses.fetchall()
