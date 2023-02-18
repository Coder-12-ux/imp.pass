from commons import *
import db
import encryption as enc
import accounts as acc

# Checking all the requirements first
# if check_the_systems() == 0:
#     exit()


MASTER_DB = json.loads(
    mss_dmss.fDemessify(
        open("./data")
    )
)["databases"]["master"]


class CommandHandler:
    def __init__(self):
        # each command has a tuple
        # whose elements represent the following:
        # --------------------------
        # 0 - number of parameters
        # 1 - number of options/flags
        # 2 - number

        # self.commands = {"set":(2, 0),
        #                  "get": (1, 2),
        #                  "delete",
        #                  "update",
        #                  "oo"}
        self.commands = ["set", "get", "delete", "update", "oo"]
        self.query = []
        self.output = ""
        self.encryptr = None
        self.database = None
        self.cursor = None
        self.logged_in = False
        self.username = ""

    def login(self, username, password):
        """will log the user into the server"""
        # print("logging in\n")
        logger.info("login called")
        a = acc.authorize(username, password)
        if a[0]:
            logger.info("LOGIN SUCCESSFUL")
            self.logged_in = True
            self.username = username
            self.database = db.DBTalker(MASTER_DB)
            self.database.connect(user=username, passwd=password)
            self.encryptr = enc.AESCipher(password, salt=a[1])
            self.cursor = self.database.cursor
            return 1
        else:
            logger.warning("wrong username and password")
            return 0

    def signup(self, username, password):
        salt = acc.sign_up(username, password)

        self.username = username
        self.database = db.DBTalker(MASTER_DB)

        self.encryptr = enc.AESCipher(password, salt)
        self.database.connect(user=username, passwd=password)
        self.cursor = self.database.cursor

    def get_query(self):
        """will input the query from the user"""
        if self.logged_in:
            self.query = input("-> ").split()
        else:
            raise Exception("not logged in")

    def set(self):
        if self.query[0] != "set" and len(self.query) != 3:
            return -1

        pid = self.query[1]
        password = self.query[2]
        penc = self.encryptr.encrypt(password)
        self.database.write(self.username, pid, str(penc)[2:-1])
        self.database.commit()
        return 1
        # self.output = self.database.fetchall()

    def get(self):
        if self.query[0] != "get" and len(self.query) != 2:
            return -1

        pid = self.query[1]
        self.database.read(self.username, 'penc', pid=pid)
        penc = self.database.fetchone()
        self.output = self.encryptr.decrypt(penc[0]).decode(
            ENCODING_FORMAT) if penc is not None else None
        return 1

    def delete(self):
        if self.query[0] != "delete" and len(self.query) != 2:
            return -1

        pid = self.query[1]
        query = f"DELETE FROM {self.username} WHERE pid='{pid}'"
        self.database.execute(query)
        self.database.commit()
        return 1
        # self.output = self.database.fetchall()

    def update(self):
        if self.query[0] != "update" and len(self.query) != 3:
            return -1

        pid = self.query[1]
        newPassword = self.query[2]
        penc = self.encryptr.encrypt(newPassword)
        del newPassword
        query = f"UPDATE {self.username} "\
                f"SET penc=\"{str(penc)[2:-1]}\" "\
                f"WHERE pid=\"{pid}\""
        self.database.execute(query)
        self.database.commit()

    def reset_pwd(newPassword: str):
        """will change the master password"""
        pass


    def process_query(self):
        """will process the query given by the user"""

        if self.logged_in:
            cmnd = self.query[0]

            if cmnd == self.commands[0]:
                return self.set()

            elif cmnd == self.commands[1]:
                return self.get()

            elif cmnd == self.commands[2]:
                return self.delete()

            elif cmnd == self.commands[3]:
                return self.update()

            else:
                return 0

        else:
            raise Exception("not logged in")
            return -1

        return 1

    def fetch_query(self):
        return self.output

    def quit(self):
        self.logged_in = False
        self.database.close()
        self.database = None
        self.cursor = None
        self.username = None
        self.encryptr = None


if __name__ == "__main__":
    cmd = CommandHandler()
    cmd.login("vipul", "vipul")
    # cmd.get_query()
    print(
        str(cmd.process_query)
    )
