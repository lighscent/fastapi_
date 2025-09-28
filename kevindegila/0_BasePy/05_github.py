from textwrap import indent
from sl import sl
import json
from urllib.request import urlopen
from pprint import pprint

if __name__ == "__main__":
    sl()

    req = urlopen("https://api.github.com/users/kevindegila")
    req = urlopen("https://api.github.com/users/grcote7")
    data = json.loads(req.read())
    print(data)
    
    sl()
    pprint(data)
    
    sl()
    print(data['blog'])

    with open('datasets/github_user.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
