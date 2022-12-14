import os
import sys
import traceback


def read_token() -> str:
    __target: str = "Token.txt"

    __path = os.path.join(
        os.getcwd(),
        "Admin",
        "Data",
        __target
    )

    try:
        with open(__path, "r") as fd:
            token: str = fd.readline().strip()

    except Exception as ERO:
        #TODO: Need Logger
        print(f"Can't open or read file: {__target}")
        print(f" -> Error: {ERO}\n")

        traceback.print_exc()

        sys.exit(0)

    return token


def read_id() -> int:
    __target: str = "Admin_ID.txt"

    __path = os.path.join(
        os.getcwd(),
        "Admin",
        "Data",
        __target
    )

    try:
        with open(__path, "r") as fd:
            __fd_id: str = fd.readline().strip()
            
    except Exception as ERO:
        print(f"Can't open or read file: {__target}")
        print(f" -> Error: {ERO}\n")
        traceback.print_exc()
        
        sys.exit(0)
    
    try:
        __id = int(__fd_id)
        
    except Exception as ERO:
        print(f"Can't convert to string f\"{__id}\" extracted from {__target}")
        print(f" -> Error: {ERO}\n")
        traceback.print_exc()
        
        sys.exit(0)

    return id
