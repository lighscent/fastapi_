from dotenv import load_dotenv
import dotenv, os, requests
import pandas as pd

# SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# PARENT_DIR = os.path.dirname(SCRIPT_DIR)
# ENV_PATH = os.path.join(PARENT_DIR, ".env")
# load_dotenv(dotenv_path=ENV_PATH)
# DOSSIER_ROOT = os.getenv("DOSSIER_ROOT", "oOo")
# print(PARENT_DIR, DOSSIER_ROOT)
# DOSSIER_D_APPEL = "D:\\fastapi\\kevindegila\\1_DataAnalyst"
# if DOSSIER_ROOT != DOSSIER_D_APPEL:
#     raise ValueError(f"Le script doit être exécuté depuis {DOSSIER_D_APPEL}")

# print(PARENT_DIR)


def getGhCsvFilesAndSaveThem():

    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    PARENT_DIR = os.path.dirname(SCRIPT_DIR)
    # Créer le dossier local s'il n'existe pas
    data_folder = PARENT_DIR + "\\datasets\\sales"
    # print(data_folder)
    os.makedirs(data_folder, exist_ok=True)

    # Lister les fichiers CSV déjà présents
    fichiers_locaux = [f for f in os.listdir(data_folder) if f.endswith(".csv")]

    if len(fichiers_locaux) >= 12:
        print(
            f"{len(fichiers_locaux)} fichiers CSV déjà présents dans '{data_folder}', aucune requête API effectuée."
        )
        paths = [os.path.join(data_folder, f) for f in fichiers_locaux]
    else:
        # API GitHub pour le dossier
        api_url = "https://api.github.com/repos/kevindegila/data-analyst/contents/datasets/SalesAnalysis/Sales_Data"
        response = requests.get(api_url)
        data = response.json()

        # Filtrer les fichiers CSV
        fichiers = [f["name"] for f in data if f["name"].endswith(".csv")]
        # Construire les URLs brutes
        racine_raw = "https://raw.githubusercontent.com/kevindegila/data-analyst/main/datasets/SalesAnalysis/Sales_Data/"
        urls = [racine_raw + f for f in fichiers]

        # Télécharger les fichiers manquants
        for nom_fichier, url in zip(fichiers, urls):
            chemin_local = os.path.join(data_folder, nom_fichier)
            if not os.path.exists(chemin_local):
                try:
                    print(f"Téléchargement de {nom_fichier}...")
                    contenu = requests.get(url).content
                    with open(chemin_local, "wb") as f:
                        f.write(contenu)
                except Exception as e:
                    print(f"Erreur lors du téléchargement de {url} : {e}")
            else:
                print(f"{nom_fichier} déjà présent, pas de téléchargement.")
        paths = [os.path.join(data_folder, f) for f in fichiers]

    # Chargement des fichiers
    frames = []
    for chemin in paths:
        try:
            frames.append(pd.read_csv(chemin))
        except Exception as e:
            print(f"Erreur lors du chargement de {chemin} : {e}")

    if frames:
        # df_total = pd.concat(frames, ignore_index=True)
        df_total = pd.concat(frames)
        # print(f"Fichiers chargés : {paths}")
        print("df.shape:", df_total.shape)
    else:
        print("Aucun fichier CSV n'a pu être chargé.")

    return df_total if frames else None


if __name__ == "__main__":
    # print(*enumerate(getGhCsvFilesAndSaveThem()), sep="\n")
    df = getGhCsvFilesAndSaveThem()
    
    # print("\nlen url: " + str(len(urls)), *enumerate(urls), sep='\n')

    # print (df.head())
    # pass
