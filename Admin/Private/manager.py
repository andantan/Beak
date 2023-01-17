import sys
import traceback

from typing import Dict, List, Tuple, Any, Optional

from Class.superclass import Block

from Admin.Utils.reader import Reader

class Manager(Block.Instanctiating):
    @staticmethod
    def get_configuration(value: str, logging: bool) -> Optional[Dict[str, str]]:
        json_data: Dict[str, Dict[str, str]] = Reader.read_json("configuration")

        data: Optional[Dict[str, str]] = None

        if value.__eq__("config"):
            data = json_data.get(value)

        elif value.__eq__("commands"):
            data = json_data.get(value)

        if logging:
            print("{\n\t" + f"{value}" + ": {")

            for k, v in data.items():
                print(f"\t\t\"{k}\": \"{v}\"")
            else:
                print("\t}\n}")

        return data


    @staticmethod
    def get_administrators(logging: bool) -> Tuple[int]:
        administrator_data: Dict[str, Any] = Reader.read_json("administrator")

        administrators: List[Dict] = administrator_data.get("administrator")

        administrator_identifications: List[int] = list()


        for i in range(0, len(administrators)):
            administrator_info: Dict[str, Any] = administrators.__getitem__(i)

            try:
                identification: int = int(administrator_info.get("identification"))

            except (ValueError, TypeError):
                sys.stderr.write(f"Invalid literal detected in administrator.json: {administrator_info.get('identification')}\n")
                sys.exit(1)

            except Exception:
                sys.stderr.write(traceback.format_exc())
                sys.exit(1)

            administrator_identifications.append(identification)


        if logging:
            print("{\n\tadministrators: [")

            for index, _identification in enumerate(administrator_identifications):
                print(f"\t\t\"Admin-{index + 1}\": \"{_identification}\"")
            else:
                print("\t}\n}")


        return tuple(administrator_identifications)
