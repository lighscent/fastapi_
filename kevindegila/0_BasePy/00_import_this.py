import codecs, os, random, sys, this

current_dir = os.path.dirname(os.path.abspath(__file__))
tools_path = os.path.abspath(os.path.join(current_dir, "..", ".."))
sys.path.append(tools_path)
from tools import *

if __name__ == "__main__":

    w = 97
    # cls()
    sl(w)
    print(current_dir, "\n", tools_path)

    sl(w)
    lines = this.s.strip().split("\n")
    lines = [l for l in lines if l.strip()]

    a_random_dentence = random.choice(lines)
    print(
        "A random sentence    :",
        a_random_dentence,
        f"\n→ Decoded with ROT-13:",
        codecs.decode(a_random_dentence, "rot_13"),
    )
    print("(See CLI above to see all this.s if cls() is commented...)")
    sl(w)
