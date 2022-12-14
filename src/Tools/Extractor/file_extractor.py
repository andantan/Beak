import os
import sys
import traceback


def token_reader() -> str:
    __target = "Token.txt"

    path = os.path.join(
        os.getcwd(),
        "Admin",
        "Data",
        __target
    )

    try:
        with open(path, "r") as fd:
            token = fd.readline().strip()

    except Exception as ERO:
        print(f"Can't open or read file: {__target}")
        print(f" -> Error: {ERO}\n")

        traceback.print_exc()

        sys.exit(0)

    
    return token