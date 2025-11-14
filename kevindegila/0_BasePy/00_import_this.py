import codecs, random, this

from tools import *

if __name__ == "__main__":

    # cls()

    sl()
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
