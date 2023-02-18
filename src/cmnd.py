from main import *
from getpass import getpass
import simple_term_menu as stm
from json import load
from os import system as sys, name as os_name
from commons import *
import datetime


def clear_screen(): return sys("cls" if "nt" in os_name else "clear")


def cmndCommands(cmd):
    cmd = cmd[1:].lower()
    logging.info(f"cmndCommands: {cmd}")

    if cmd == "show settings":
        print("<< SETTINGS >>")
        print(str(settings)[1:-1])

    elif cmd == "help":
        print(HELP_TEXT)


cmndhndlr = CommandHandler()
command_mode = bool(settings["commandMode"])

clear_screen()


if command_mode:
    userCreds = (
        input("username: "),
        input("password: ")
        if settings["echoOn"] else
        getpass("password")
    )

    while cmndhndlr.login(*userCreds) == 0:
        clear_screen()
        print(
            "Credentials declined\n"
            "Would you like to \n[L]ogin \n[S]ign Up \n[E]xit"
        )
        s = input()

        if s.lower() == "l":
            continue

        elif s.lower() == "s":
            clear_screen()
            print("selected: Sign Up\n")
            try:
                cmndhndlr.signup(*userCreds)
                del user_credentials
            except Exception as e:
                traceback(str(exc_info()))
                print(ERROR_MSG)

        elif s.lower() == "e":
            cmndhndlr.quit()
            print("Bye")
            exit()

    cmndno = 0
    # command mode loop[for find]
    try:
        while 1:
            logging.info("command loop started")
            # cmndhndlr.get_query()
            query = None
            query = input(f"[{cmndno}]> ")

            if query == "":
                print("GIVE ME COMMANDs :)")
                continue

            elif query == "exit":
                cmndhndlr.quit()
                exit()

            elif query.startswith("*"):
                cmndCommands(query)

            elif query.startswith("$"):
                sys(query[1:])
                logging.info(f"executed on shell: {query[1:]}")

            elif query:
                cmndhndlr.query = query.split()
                code = cmndhndlr.process_query()

                if code == 1:
                    print(cmndhndlr.output)
                    cmndhndlr.output = None
                elif code == 0:
                    print(ERROR_MSG)
                elif code == -1:
                    print("wrong syntax")

                cmndno += 1
                cmndhndlr.query = None

    except Exception as e:
        traceback(exc_info())
        print(ERROR_MSG)


# command mode menu
elif command_mode is False:
    echo_on = settings["echoOn"]

    options = ["Log in", "Sign up"]
    menu = stm.TerminalMenu([
        f"[{i}] {options[i]}"
        for i in range(len(options))
    ])
    option_selected = menu.show()

    if option_selected == 0:
        login_code = cmndhndlr.login(
            input("username: "),
            getpass("password")
            if settings["echoOn"] is False
            else
            input(("password: "))
        )

        if login_code == 0:
            print("LOGIN FAILED!")

    elif option_selected == 1:
        signup_code = cmndhndlr.signup(
            input("username: "),
            getpass("password")
            if settings["echoOn"] is False
            else
            input(("password: "))
        )

    # menu loop[for find]
    menu_options = cmndhndlr.commands + ["exit"]
    while cmndhndlr.logged_in:
        clear_screen()
        menu = stm.TerminalMenu([
            f"[{i}] {menu_options[i]}"
            for i in range(len(menu_options))
        ])
        user_selection = menu.show()
        selected_option = menu_options[user_selection]

        # 0:set
        # 1:get
        # 2:delete
        # 3:update

        # menu for SET
        if selected_option == "exit":
            clear_screen()
            print("Good Bye")
            cmndhndlr.quit()

        if user_selection == 0:
            pid = input("<<<< Password Identifier >>>>\n> ")
            password =\
                input("<<<< Password >>>>\n> ") \
                if echo_on else\
                getpass("<<<< Password >>>>\n> ")

            cmndhndlr.query = (selected_option, pid, password)
            del password
            cmndhndlr.process_query()
            cmndhndlr.query = None
            clear_screen()

        # menu for GET
        elif user_selection == 1:
            print("<< GET >>")
            pid = input("<<<< Password Identifier >>>>\n> ")
            cmndhndlr.query = (selected_option, pid)
            cmndhndlr.process_query()

            if cmndhndlr.output:
                # copy/print menu
                options = ["copy", "print"]
                menu = stm.TerminalMenu([
                    f"[{i}] {str(options[i])}"
                    for i in range(len(options))
                ])
                clear_screen()

                print("<< GET >>")
                selection = menu.show()

                if selection == 1:
                    print(cmndhndlr.output)

                    if settings["letPasswordStill"]:
                        print("won't vanish until u press enter")
                        input()
                    else:
                        time = settings["vanishTime"]
                        print(f"will vanish in {time}")
                        sleep(time)

                elif selection == 0:
                    try:
                        from clipboard import copy
                        copy(cmndhndlr.output)
                        print("copied to your clipboard")

                    except Exception as e:
                        logger.error(e)
                        traceback(exc_info())
                        print(ERROR_MSG)
            else:
                print("Nothing")
                input()

            cmndhndlr.output = None
            clear_screen()

        # menu for DELETE
        elif user_selection == 2:
            print("<< DELETE >>")
            pid = input("<<<< Password Identifier >>>>\n> ")
            cmndhndlr.query = (selected_option, pid)
            cmndhndlr.process_query()
            clear_screen()

        # menu for UPDATE
        elif user_selection == 3:
            print("<< UPDATE >>")
            pid = input("<<<< Password Identifier >>>>\n> ")
            newPassword = input("<<<< New PASSWORD >>>>\n")
            cmndhndlr.query = (selected_option, pid, newPassword)
            cmndhndlr.process_query()
            clear_screen()
