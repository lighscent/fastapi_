import argparse, webbrowser, time

parser = argparse.ArgumentParser()
parser.add_argument("--session", "-s", type=int, default=4, help="Nombre de session")
parser.add_argument(
    "--duree", "-d", help="Duree d'une session en minute", type=int, default=20
)
parser.add_argument(
    "--pause", "-p", help="La durée de la pause en minute", type=int, default=3
)
args = parser.parse_args()

# For 4 sessions of 20 min work and 3 min pause in between :
# python main.py --session 4 --duree 20 --pause 3


def session(duree, pause):
    """
    Lance une session de travail de "durée" minute,
    ouvre une vidéo dans le navigateur
    et fais une pause de "pause" minute
    :param duree:
    :param pause:
    :return:
    """
    print("Une session a commencé")
    time.sleep(duree * 60)
    webbrowser.open("https://www.youtube.com/watch?v=yzg94Iamm_c")
    print("Pause en cours")
    time.sleep(pause * 60)


for i in range(args.session):
    session(args.duree, args.pause)
    nsr = args.session - i - 1
    print(f"Session {i + 1} terminée, il reste {nsr} session{'s' if nsr > 1 else ''}")
