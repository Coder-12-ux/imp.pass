import json
from time import sleep
import logging
import simple_term_menu
import mss_dmss
from subprocess import Popen, run
from tempfile import TemporaryFile
from sys import exc_info

HOSTS = json.load(open("HOSTS"))
selected_host = HOSTS["selected_host"]
settings = json.load(open("settings.json"))
requirements = json.load(open("requirments.json"))

ERROR_MSG = "ERROR ENCOUNTERED!\n" \
            "check logs for further details"

ENCODING_FORMAT = "utf-8"


def traceback(trace):
    with open("./logs/traceback.txt", "a+") as t:
        t.write(str(trace) + "\n")


def check_the_system():
    # this function checks:
    # - database with necessary tables
    # - database with necessary users
    # -  


    with TemporaryFile() as op, TemporaryFile() as err:
        process = Popen(["pip", "list"], stdout=op, stderr=err)
        process.wait()
        packages = op.read()

    packages = str(packages)
    packages = tuple(
        _.split() for _ in packages.split("\n")
    )

    if requirements["packages"] in packages:
        return 1
    else:
        return 0


logging.basicConfig(
    level=logging.INFO,
    filename="./logs/logs.txt",
    filemode="w")

logger = logging.getLogger()

HELP_TEXT = "<<<<<<< HELP >>>>>>>\n" \
            "there are 4 commands which are:\n" \
            "\tset, get, delete, update \n\n" \
            "\tset: prameters : <pid> <password>\n\t\tsaves the password with a password identifier\n" \
            "\tget: \n\t\tgets the password using the password identifier\n" \
            "\tdelete: \n\t\tdeletes the password\n" \
            "\tupdate: \n\t\tupdates the password\n"



print("passed :)" if check_the_system() else "failed :(")


