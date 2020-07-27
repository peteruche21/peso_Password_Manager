import sqlite3


class ActionDB(object):
    def conne(self):
        self.connection = sqlite3.connect('pswdb.db')
        self.cursor = self.connection.cursor()

    def master_key(self, master, first_name, email_address):
        self.conne()
        self.cursor.execute("CREATE TABLE passwords \
                (ID INTEGER PRIMARY KEY AUTOINCREMENT, NAME str, VALUE str)")
        self.cursor.execute(
            "INSERT INTO passwords (NAME, VALUE) VALUES ('master', ?)",
            [master])
        personal_info = [(first_name, email_address)]
        self.cursor.executemany(
            "INSERT INTO passwords (NAME, VALUE) VALUES (?, ?)", personal_info)
        self.cursor.execute(
            "INSERT INTO passwords (NAME, VALUE) VALUES ('onetime', 'None')")
        self.connection.commit()
        self.connection.close()

    def one_psw(self, name):
        self.conne()
        self.cursor.execute("SELECT * from passwords WHERE NAME=?", [name])
        one = self.cursor.fetchone()[0]
        self.connection.commit()
        self.connection.close()
        return one

    def all_psw(self):
        self.conne()
        self.cursor.execute("SELECT * from passwords WHERE ID > 3")
        all_passwords = self.cursor.fetchall()
        self.connection.commit()
        self.connection.close()
        return all_passwords

    def new_psw(self, name, value):
        self.conne()
        psw_details = [(name, value)]
        self.cursor.executemany(
            "INSERT INTO passwords (NAME, VALUE) VALUES (?, ?)", psw_details)
        print('added password successfully')
        self.connection.commit()
        self.connection.close()

    def one_time_psw(self, one_time_key):
        self.conne()
        self.cursor.execute("UPDATE passwords SET VALUE = ? WHERE ID = 3",
                            [one_time_key])
        self.cursor.execute("SELECT VALUE from passwords WHERE ID = 3 ")
        one_time_login_key = self.cursor.fetchone()
        self.cursor.execute('SELECT VALUE from passwords WHERE ID = 2')
        to = self.cursor.fetchone()
        self.connection.commit()
        self.connection.close()
        return one_time_login_key[0], to[0]

    def update_master(self, new_master):
        self.conne()
        self.cursor.execute("UPDATE passwords SET VALUE =? WHERE ID = 1",
                            [new_master])
        self.connection.commit()
        self.connection.close()

    def custom_action(self, action, index):
        self.conne()

        if 'DELETE' in action:
            self.cursor.execute(action + " FROM passwords WHERE ID = ?",
                                [index])
            self.connection.commit()
            self.connection.close()

        elif 'SELECT' in action:
            self.cursor.execute(action + " FROM passwords WHERE ID = ?",
                                [index])
            selection = self.cursor.fetchone()
            self.connection.close()
            return selection[0]
