import json
import os

from typing import Dict

Path = os.path.join(
    os.getcwd(),
    "Admin",
    "Data",
    "admin_configure.json"
)


with open(Path, "r") as handler:
    data: Dict = json.load(handler)
    administrator: list = data.get("administrator")
    administrator_entity_1st: dict = administrator.__getitem__(0)
    id = int(administrator_entity_1st.get("identification"))


    print(id)