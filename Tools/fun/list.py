import os
import sys
import json

root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

modules = []
filtered_modules = []
funcs = {}

for x in os.listdir(os.path.join(root, "Lib")):
    if x.endswith(".py") and not x.startswith("_"):
        modules.append(x)

for module in modules:
    with open(f"{os.path.join(root, "Lib", module)}") as file:
        if "__all__" in file.read():
            filtered_modules.append(module)

sys.path.append(f"{os.path.join(root, "Lib")}")

for module in filtered_modules:
    module = module.split(".")[0]
    exec(f"import {module}")
    exec(f"funcs[\"{module}\"] = {module}.__all__")
    exec(f"del {module}")

import os

with open(f"{os.path.join(root, "funcs.json")}", 'w') as file:
    json.dump(funcs, file, indent=4)
