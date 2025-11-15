import numpy as np
import pandas as pd

if __name__ == "__main__":

    url = "https://fr.wikipedia.org/wiki/Liste_des_pr%C3%A9sidents_des_%C3%89tats-Unis_par_long%C3%A9vit%C3%A9"

    # Add headers to mimic a browser request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    tables = pd.read_html(url, storage_options=headers)

    df = tables[0]

    # print(df.head(3))
    print(df)
