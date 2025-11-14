import json, os, sys

current_dir = os.path.dirname(os.path.abspath(__file__))
tools_path = os.path.abspath(os.path.join(current_dir, "..", ".."))
sys.path.append(tools_path)
from tools.utils import *

if __name__ == "__main__":

    cls()

    maradona = """
    {
        "prenom": "Diego",
        "nom": "Maradone",
        "Actif": true,
        "equipes": [
            "Boca Juniors",
            "Naples",
            "Barcelone"
        ],
        "enfants": [
            {"prenom": "Dalma", "age": 34},
            {"prenom": "Gianina", "age": 31}
        ],
        "LDC": null
    }
    """

    print(maradona)
    sl()
    import pprint as pprint

    data = json.loads(maradona)
    pprint.pprint(data)

    sl()
    prenom_enfants = [enfant["prenom"] for enfant in data.get("enfants", [])]
    print("prenom_enfants =", prenom_enfants[::-1])

    sl()
    maradona_json = json.dumps(data, indent=2)
    print(type(maradona_json), maradona_json)

    with open("./datasets/03j_maradona.json", "w+", encoding="utf-8") as f:
        # f.write('maradona.json')
        # json.dump(sorted(data.items()), f)
        # json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True)
        json.dump(data, f, ensure_ascii=False, indent=4)
