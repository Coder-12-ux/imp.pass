import bcrypt
from commons import *
import db


def authorize(username, password):
    """
    will tell whether the user and
    password combination is correct or not
    """

    CREDS = json.loads(mss_dmss.fDemessify(open("creds")))
    DATA = json.loads(mss_dmss.fDemessify(open("data")))

    # salt
    SALT_UNAME, SALT_PASSWORD = CREDS["salt"]["username"], CREDS["salt"]["password"]
    datab = db.DBTalker(DATA["databases"]["salt"])
    datab.connect(SALT_UNAME, SALT_PASSWORD)
    datab.read("a", "namk", username=username)
    output = datab.fetchone()

    if output is None:
        return (False, None)

    salt = output[0]
    # got the salt

    datab = db.DBTalker(DATA["databases"]["hash"])

    HASH_UNAME, HASH_PASSWORD = CREDS["hash"]["username"], CREDS["hash"]["password"]
    datab.connect(HASH_UNAME, HASH_PASSWORD)

    # print(password, salt)
    # generating the hashed version of the password
    generated_hash = bcrypt.hashpw(password.encode(
        ENCODING_FORMAT), salt)

    # getting the hash from database
    datab.read("a", 'weird', username=username)
    output = datab.fetchone()
    db_hash = output[0] if output else None
    # got the hash
    datab.close()

    return (generated_hash == db_hash, salt)


def sign_up(user: str, password: str):
    """
    CREATES a new user and
    a new table in the database
    """

    CREDS = json.loads(mss_dmss.fDemessify(open("creds")))
    DATA = json.loads(mss_dmss.fDemessify(open("data")))

    # this is the master database connector
    master_db = db.DBTalker(DATA["databases"]["master"])
    master_db.connect(
        user=CREDS["master"]["username"],
        host=HOSTS[selected_host],
        passwd=CREDS["master"]["password"]
    )

    datab = db.DBTalker(DATA["databases"]["salt"])
    password_salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(
        password=password.encode(ENCODING_FORMAT),
        salt=password_salt
    )

    # saving salt
    datab.connect(
        user=CREDS["salt"]["username"],
        passwd=CREDS["salt"]["password"]
    )
    datab.write("a", user, str(password_salt)[2:-1], where=None)
    datab.commit()

    # changing the database to hash database
    datab = db.DBTalker(DATA["databases"]["hash"])

    datab.connect(
        user=CREDS["hash"]["username"],
        passwd=CREDS["hash"]["password"]
    )

    datab.write("a", user, str(password_hash)[2:-1])

    # creating table for storing user's passwords
    master_db.execute(
        f"create table {user}(pid VARCHAR(20), penc VARBINARY(255))")

    # granting user the required permissions on it's table
    master_db.create_user(
        user=user, host=HOSTS[selected_host], password=password)
    master_db.grant_permissions(
        user, HOSTS[selected_host],
        f"{DATA['databases']['master']}.{user}",
        "SELECT", "INSERT", "DROP", "DELETE", "UPDATE"
    )

    master_db.commit()
    datab.commit()
    datab.close()

    return password_salt
