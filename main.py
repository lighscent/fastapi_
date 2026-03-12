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


def toSeeToBp(df):
    md = ""
    for _, row in df.iterrows():
        
        rec = ['titre', 'date', 'vues', 'duree', 'url']
        
        md += f"* [ ] [{row['titre'], row['duree']}]({row['url']})\n"
        
        
        
    # ❌ save this file .md
    return md

from divers.yt_videos.to_see import videos_to_see, format_remaining_time_fr

if __name__ == "__main__":

    cls()

    # print(*["hello" for _ in range(3)], sep="\n")
    # timestamp2fruuu(1773168642)

    df = videos_to_see()
    print()

    # nbmn=2450
    # print(nbmn, '→', format_remaining_time_fr(nbmn))

    md = toSeeToBp(df)
    print(md)

    # display_videos_table(df)

    end()
