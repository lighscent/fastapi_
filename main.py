from pymox_kit import *
from datetime import datetime


from divers.yt_videos.to_see import (
    toSeeToBp,
    videos_to_see,
    format_remaining_time_fr,
)

if __name__ == "__main__":

    cls()

    # print(*["hello" for _ in range(3)], sep="\n")
    
    nbmn=2450
    print(nbmn, '→', format_remaining_time_fr(nbmn))

    df = videos_to_see()
    print()


    md = toSeeToBp(df)
    # print(md)

    # display_videos_table(df)

    end()
