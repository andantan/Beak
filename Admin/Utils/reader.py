import sys
import json
import traceback

from typing import Dict, Any


from Class.superclass import Block

from Data.Paraments.settings import PATH


class Reader(Block.Instanctiating):
    @staticmethod
    def read_json(run_mode: str) -> Dict[str, Any]:
        mode: Dict[str, str] = {
            "administrator": "administrator_json_path",
            "configuration": "configuration_json_path"
        }

        if run_mode in mode.keys():
            path = PATH.get(mode.get(run_mode))
            try:
                with open(path, "r", encoding="UTF-8") as handler:
                    json_data = json.load(handler)

            except FileNotFoundError:
                sys.stderr.write(f"File does not exist(PATH: {path})")
                sys.exit(1)
            
            except Exception:
                sys.stderr.write(traceback.format_exc())
                sys.exit(1)
            
            return json_data
