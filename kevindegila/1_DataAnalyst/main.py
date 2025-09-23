import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os


def sl():
    w = 99
    print(" ─" * (w // 2) + "→")


if __name__ == "__main__":

    sl()

    # //2do simplifier path
    pathFile = "D:\\fastapi\\kevindegila\\1_DataAnalyst\\datasets\\COVID-19-geographic-disbtribution-worldwide-2020-12-14.xls"
    if os.path.exists(pathFile):
        df = pd.read_excel(pathFile)
    else:
        print("Fichier introuvable :", pathFile)
        exit()

    print(df)
    sl()
