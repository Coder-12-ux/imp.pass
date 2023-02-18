import mariadb
from commons import *


class DBTalker:
    connection = None
    cursor = None

    def __init__(self, database_name=None):
        self.dbname = database_name

    def __enter__(self):
        return self.cursor()

    def __exit__(self):
        self.close()

    def connect(self, user: str, passwd: str, host=HOSTS[selected_host]):
        """Creates a connection with the database"""
        conn_params = {
            "host": host,
             "user": user,
              "passwd": passwd}

        if self.dbname is not None:
            conn_params["db"] = self.dbname

        self.connection = mariadb.connect(**conn_params)
        self.cursor = self.connection.cursor()

    def disconnect(self):
        """Disconnects from the connected database"""
        self.connection = None
        self.cursor = None

    def execute(self, query: str):
        logger.info("query executed")
        logger.info(query)
        try:
            self.cursor.execute(query + ";")
        except mariadb.Error as e:
            logger.info(query)
            traceback(exc_info())
            print(ERROR_MSG)

    def fetchall(self):
        try:
            return self.cursor.fetchall()
        except Exception as e:
            traceback(exc_info())
            print(ERROR_MSG)

    def fetchone(self):
        try:
            return self.cursor.fetchone()
        except Exception as e:
            traceback(exc_info())
            print(ERROR_MSG)

    def fetchmany(self, n):
        try:
            return self.cursor.fetchmany(n)
        except Exception as e:
            traceback(exc_info())
            print(ERROR_MSG)

    def close(self):
        self.cursor.close()
        self.connection.close()

    def commit(self):
        """Commit the done changes"""
        self.connection.commit()

    def read(self, table, *cols, **where):
        if len(cols) == 0:
            sql_query = f"SELECT * FROM {table}"

        elif len(cols) == 1:
            sql_query = f"SELECT {cols[0]} FROM {table}"

        else:
            col = str(cols)[1:-1].replace("'", "")
            sql_query = f"SELECT {col} FROM {table}"

        logger.info(sql_query)

        if where:
            sql_query += " WHERE " + " AND ".join(
                f"{key}='{where[key]}'" for key in where
            )

        self.execute(sql_query)

    def write(self, table, *values, where=None):
        if where is None:
            self.execute(f"INSERT INTO {table} VALUES ({str(values)[1:-1]})")
        else:
            self.execute(
                f"INSERT INTO {table} VALUES ({str(values)[1:-1]}) where={where}")

    def grant_permissions(self, user, host, sql_obj, *permissions):
        sql_query = "GRANT %s ON %s TO '%s'@'%s'" % \
                    (', '.join(permissions),
                     sql_obj, user, host)

        logger.info("permissions %s granted for '%s'@'%s' on %s" %
                     (permissions, user, host, sql_obj))

        self.execute(sql_query)

    def revoke_permissions(self, user, host, sql_obj, *permissions):
        sql_query = "REVOKE %s ON %s FROM %s@%s" % \
                    (', '.join(p for p in permissions),
                     sql_obj, user, host)

        logger.info("permissions %s revoked for '%s'@'%s' on %s" %
                     (permissions, user, host, sql_obj))
        print(sql_query)
        self.execute(sql_query)

    def drop_user(self, user, host):
        self.execute(f"DROP USER '{user}'@'{host}'")

    def create_user(self, user, host, password):
        self.execute(
            f"CREATE USER '{user}'@'{host}' IDENTIFIED BY '{password}'")
