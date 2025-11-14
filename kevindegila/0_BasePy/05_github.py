from textwrap import indent
import json
from urllib.request import urlopen
from pprint import pprint

from tools import *


if __name__ == "__main__":

    cls()

    req = urlopen("https://api.github.com/users/kevindegila")
    # req = urlopen("https://api.github.com/users/grcote7")
    data = json.loads(req.read())
    print(data)

    sl()
    pprint(data)

    sl()
    print(data["bio"])

    with open("datasets/github_user.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
