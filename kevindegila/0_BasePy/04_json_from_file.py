import json
from textwrap import indent

with open("datasets/03j_maradona.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# print(data)
print(indent(json.dumps(data, indent=2), "    "))
