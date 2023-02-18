from math import log


def fMessify(fp):
    messified = messify(fp.read())
    fp.seek(0)
    fp.write(messified)
    fp.close()


def fDemessify(fp):
    return demessify(fp.read())


def messify(string):
    cache = {} 
    new_string = ""

    for character in string:
        # storing the log value of each character
        if character not in cache:
            cache[character] = str(log(ord(character), len(string)))
            new_string += cache[character] + "-"

        else:
            new_string += cache[character] + "-"

    new_string += str(len(string))

    return new_string


def demessify(string):
    cache = {}
    string = string.split("-")
    base = int(string.pop())
    solved_string = ""

    for c in string:
        if c in cache:
            solved_string += cache[c]
            continue

        else:
            cache[c] = chr(round(base ** float(c)))
        solved_string += cache[c]

    return solved_string


pdm = lambda x: fDemessify(open("x"))
