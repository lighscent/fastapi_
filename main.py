from pymox_kit import *
from datetime import datetime


def timestamp2fruuu(ts=1773168642):
    ts = 1773168642
    dt = datetime.fromtimestamp(ts)
    # * [ ] → Kit
    jours = [
        "lundi",
        "mardi",
        "mercredi",
        "jeudi",
        "vendredi",
        "samedi",
        "dimanche",
    ]
    mois = [
        "janvier",
        "fevrier",
        "mars",
        "avril",
        "mai",
        "juin",
        "juillet",
        "aout",
        "septembre",
        "octobre",
        "novembre",
        "decembre",
    ]

    date_fr = (
        f"{jours[dt.weekday()].capitalize()} {dt.day:02d} {mois[dt.month - 1]} "
        f"{dt.year} - {dt:%H:%M:%S}"
    )
    print(date_fr)


from divers.yt_videos.to_see import videos_to_see

if __name__ == "__main__":

    cls()

    # print(*["hello" for _ in range(3)], sep="\n")
    # timestamp2fruuu(1773168642)

    df = videos_to_see()
    
    print(df)

    # display_videos_table(df)

    end()
