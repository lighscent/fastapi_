from tools import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

if __name__ == "__main__":

    w = 178

    sl(w)

    # x = ["2016", "2017", "2018", "2019"]
    # y = [3, 8, 5, 12]

    # OU:

    data = [("2016", 3), ("2017", 8), ("2018", 5), ("2019", 13)]
    sns.set_style("whitegrid")

    df = pd.DataFrame(data, columns=["Années", "Valeurs"])
    x = df["Années"]
    y = df["Valeurs"]
    print(df)

    # Version directe avec pandas
    # df.plot(
    #     x="Années",
    #     y="Valeurs",
    #     kind="line",
    #     marker="o",
    #     color="blue",
    #     figsize=(8, 5),
    #     title="Évolution des valeurs",
    # )
    # plt.ylabel("Valeurs")
    # plt.tight_layout() # Rempli le layout
    # plt.show()

    # Simple grap (MatLab)

    # plt.figure("Titre de la figure")  # nom de la fenetre
    # plt.title("Notre simple graph")
    # plt.xlabel("Axe des x")
    # plt.ylabel("Axe des y")
    # plt.tight_layout()
    # plt.plot(x, y)
    # plt.show()

    # # Graphs évolué(Matplot object)
    # fig, ax = plt.subplots(figsize=(16, 4), nrows=1, ncols=3)
    # fig.canvas.manager.set_window_title("Différents graphs")  # nom de la fenetre

    # ax[0].set_title("Graph en Lignes")
    # ax[0].plot(x, y)
    # ax[0].set_xlabel("Axe des x")
    # ax[0].set_ylabel("Axe des y")

    # ax[1].set_title("Graph en Points")
    # ax[1].set_xlabel("Années")
    # ax[1].set_ylabel("Valeurs")
    # ax[1].scatter(
    #     x,
    #     y,
    #     color="red",
    #     s=500,
    #     marker="*",
    #     alpha=0.5,
    #     edgecolors="black",
    #     linewidths=2,
    # )

    # # 🔹 Graph 3 : superposition ligne + étoiles
    # ax[2].set_title("Graph combiné")
    # ax[2].plot(x, y, color="blue", label="Ligne")
    # ax[2].scatter(
    #     x,
    #     y,
    #     color="red",
    #     s=50,
    #     marker="o",
    #     alpha=0.5,
    #     edgecolors="black",
    #     linewidths=2,
    #     label="Points",
    # )
    # ax[2].set_xlabel("X")
    # ax[2].set_ylabel("Y")
    # ax[2].legend()

    # plt.tight_layout()
    # sns.set_style("whitegrid")
    # # plt.show()

    # plt.xlabel("Category")
    # plt.ylabel("Taille")
    # x = ["Hommes", "Femmes"]
    # y = [180, 160]
    # plt.bar(x, y)
    # plt.show()


    # Version recommandée
    # creer une figure
    fig = plt.figure(figsize=(16, 8))
    # definir le nombre de subplot et creer les axes
    ax1 = fig.add_subplot(211)  # 2 nrow, 1 ncols, graph #1
    ax2 = fig.add_subplot(212)  # 2 nrow, 1 ncols, graph #2

    # modifier chaque ax pour faire l'affichage
    ax1.set_xlabel("x")
    ax1.set_ylabel("y")
    ax1.plot(x, y)

    ax2.set_xlabel("Category")
    ax2.set_ylabel("Taille")
    x = ["Hommes", "Femmes"]
    y = [180, 160]
    ax2.bar(x, y)

    plt.tight_layout()
    plt.show()
