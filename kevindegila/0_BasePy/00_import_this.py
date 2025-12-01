from tools import *

if __name__ == "__main__":

    w = 57
    cls()
    import codecs, random, this

    # sl(w)
    lines = this.s.strip().split("\n")
    # print(len(lines))  # Ruler
    # lines = [l for l in lines if l.strip()]
    # print(len(lines))  # Ruler

    sl(w)
    lines = [l for l in lines if l.strip()]

    a_random_dentence = random.choice(lines)
    print(
        "A random sentence    :",
        a_random_dentence,
        f"\n→ Decoded with ROT-13:",
        codecs.decode(a_random_dentence, "rot_13"),
    )
    print("(See CLI above to see all this.s if cls() is commented...)")
