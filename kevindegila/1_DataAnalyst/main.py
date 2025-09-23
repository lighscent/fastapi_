import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

if __name__ == "__main__":
    w = 178
    print("-→" * (w // 2))
    
    # //2do simplifier path
    chemin = "D:\\fastapi\\kevindegila\\1_DataAnalyst\\datasets\\COVID-19-geographic-disbtribution-worldwide-2020-12-14.xls"
    if os.path.exists(chemin):
        df = pd.read_excel(chemin)
        print(df)
        print(df.shape)
    else:
        print("Fichier introuvable :", chemin)
