from pymox_kit import *
from datetime import datetime


from divers.yt_videos.to_see import (
    toSeeToBp,
    videos_to_see,
    format_remaining_time_fr,
)

from divers.yt_videos.scrap_some import (
    scrap_some
)

if __name__ == "__main__":

    cls()

    # print(*["hello" for _ in range(3)], sep="\n")

    # nbmn=2450
    # print(nbmn, '→', format_remaining_time_fr(nbmn))

    df  = scrap_some()
    print(df)

    # df = videos_to_see()
    # print()

    # print (len(df), df.shape, df.size)

    # md = toSeeToBp(df)
    # print(md)

    # display_videos_table(df)

    end()
