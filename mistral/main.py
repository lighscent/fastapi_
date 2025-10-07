import os, dotenv, time
from mistralai import Mistral
import httpx
import logging
import sqlite3
import pandas as pd
from datetime import datetime

import markdown2
from colorama import init, Fore, Style

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Désactiver les logs httpx
logging.getLogger("httpx").setLevel(logging.WARNING)

# Charger les variables d'environnement
dotenv.load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

if not MISTRAL_API_KEY:
    raise ValueError("MISTRAL_API_KEY non trouvée dans .env")

MODEL = "mistral-large-latest"
client = Mistral(api_key=MISTRAL_API_KEY)


def safe_chat_request(messages, max_retries=5, max_tokens=300):
    """
    Effectue une requête chat avec retry automatique.

    Args:
        messages: Liste des messages
        max_retries: Nombre max de tentatives (défaut: 3)
        max_tokens: Limite de tokens (défaut: 300)

    Returns:
        str: Réponse du modèle

    Raises:
        Exception: Si toutes les tentatives échouent
    """
    last_exception = None

    for attempt in range(max_retries):
        try:
            response = client.chat.complete(
                model=MODEL,
                messages=messages,
                max_tokens=max_tokens,
                temperature=0.7,  # Ajout pour contrôler la créativité
            )

            return response.choices[0].message.content

        except httpx.HTTPStatusError as e:
            last_exception = e
            if e.response.status_code == 429:
                wait_time = min(2**attempt, 30)  # Backoff plus modéré
                logger.warning(
                    f"Rate limit atteint. Attente {wait_time}s (tentative {attempt+1}/{max_retries})"
                )
                time.sleep(wait_time)
            else:
                logger.error(f"Erreur HTTP {e.response.status_code}: {e}")
                break

        except (httpx.TimeoutException, httpx.ConnectError) as e:
            last_exception = e
            wait_time = min(2**attempt, 10)
            logger.warning(
                f"Erreur réseau. Retry dans {wait_time}s (tentative {attempt+1}/{max_retries})"
            )
            time.sleep(wait_time)

        except Exception as e:
            logger.error(f"Erreur inattendue: {e}")
            raise

    raise Exception(
        f"Échec après {max_retries} tentatives. Dernière erreur: {last_exception}"
    )


def structured_data(spending_text):

    syst = """
    Tu es un assistant intelligent de dépense. Je souhaite te donner une description de mes dépenses et je souhaite que tu transformes la description en format json avec les champs suivants.

    designation : la chose pour laquelle la dépense a été effectuée,
    moyen_paiement :  Le moyen de paiement dans la liste [Cash, Mobile money, Chèque ou Carte de crédit],
    categorie :  la catégorie de la dépense dans cette liste: 
    [transport, shopping, electricité, eau, loyer, voiture, television, sport, santé, loisirs, autres
    ]
    montant : le montant de la dépense

    Tu ne retournes que le format json. Aucun autre texte. Même pas "Voici la description de votre première dépense au format JSON
    """

    messages = [
        {"role": "system", "content": syst},
        {"role": "user", "content": spending_text},
        {
            "role": "user",
            "content": "j'ai acheter des pâtes pour 30 euros par carte bancaire.",
        },
    ]
    return messages


def simu_reponse():
    return [
        {
            "designation": "Transport",
            "moyen_paiement": "Cash",
            "categorie": "transport",
            "montant": 20,
        },
        {
            "designation": "Taxi",
            "moyen_paiement": "Chèque",
            "categorie": "transport",
            "montant": 20,
        },
        {
            "designation": "Achats alimentaires - Pâtes",
            "moyen_paiement": "Carte de crédit",
            "categorie": "shopping",
            "montant": 30,
        },
    ]


def create_db(db_file):
    # Connexion à la base de données (crée le fichier s'il n'existe pas)
    conn = sqlite3.connect(db_file)

    # Création d'un curseur pour exécuter des requêtes
    cur = conn.cursor()

    # Création de la table
    cur.execute(
        """
        CREATE TABLE depenses (
            id INTEGER PRIMARY KEY,
            date DATE,
            designation TEXT,
            categorie TEXT,
            moyen_paiement TEXT,
            montant REAL,
            UNIQUE(date, designation, categorie, moyen_paiement, montant)
        )
    """
    )

    # Enregistrement des modifications
    conn.commit()

    # Fermeture de la connexion
    conn.close()


def save_to_sql(data, db_file="depense.db"):
    # Connexion à la base de données
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    # Insertion des données
    for item in data:
        cur.execute(
            """
            INSERT OR IGNORE INTO depenses (designation, categorie, moyen_paiement, montant, date)
            VALUES (?, ?, ?, ?, ?)
        """,
            (
                item["designation"],
                item["categorie"],
                item["moyen_paiement"],
                item["montant"],
                datetime.now().strftime("%Y-%m-%d"),  # Ajout de la date actuelle
            ),
        )

    # Enregistrement des modifications et fermeture de la connexion
    conn.commit()
    conn.close()


def read_from_sql(db_file="depense.db"):
    """Lit les dernières dépenses depuis la base de données"""
    conn = sqlite3.connect(db_file)
    df = pd.read_sql_query("SELECT * FROM depenses ORDER BY id DESC LIMIT 10", conn)
    conn.close()
    return df


def text_to_sql(question):
    syst = """
    J'ai une table SQL nommée "depenses" avec les colonnes suivantes :
        id INTEGER PRIMARY KEY,
        date DATE,
        designation TEXT,
        categorie TEXT,
        moyen_paiement TEXT,
        montant REAL,
        UNIQUE(date, designation, categorie, moyen_paiement, montant)
        
    Transforme la question suivante en requête SQL qui répond à la question. Tu ne retournes que la requête SQL, aucun autre text introductif
    """

    messages = [
        {"role": "system", "content": syst},
        {"role": "user", "content": question},
    ]

    return safe_chat_request(messages)


def reformule_answer(user_question, sql_result):
    syst = """
    En te basant sur le table SQL dont le schema est le
    suivant, génère une réponse courte en langage naturel :
        id INTEGER PRIMARY KEY,
        date DATE,
        designation TEXT,
        categorie TEXT,
        moyen_paiement TEXT,
        montant REAL,
        UNIQUE(date, designation, categorie, moyen_paiement, montant)
    """

    quest = f"""Voici la question qu'a posé l'utilisateur : 
    {user_question}
    La réponse : {sql_result}
    Si la réponse est un montant, l'unité monetaire est euros.
    """
    messages = [{"role": "system", "content": syst}, {"role": "user", "content": quest}]
    return safe_chat_request(messages)


if __name__ == "__main__":
    # init()
    def render_simple_markdown(text):
        import re
        
        # Remplacer **texte** par du texte jaune et gras
        text = re.sub(r'\*\*(.*?)\*\*', f'{Fore.YELLOW}{Style.BRIGHT}\\1{Style.RESET_ALL}', text)
        
        # Remplacer *texte* par du texte cyan
        text = re.sub(r'\*(.*?)\*', f'{Fore.CYAN}\\1{Style.RESET_ALL}', text)
        
        # Remplacer les lignes de séparation
        text = text.replace("---", "─" * 50)
        
        return text
    
    # messages = structured_data("J'ai payé 20 euros en cash pour le transport.")
    # print(messages)

    try:
        # reply = safe_chat_request(messages)
        reply = simu_reponse()

        df = pd.DataFrame(reply)
        print("Données récupérées en réponse :")
        print(df.to_markdown(index=False), "\n")

        db_file = "depense.db"
        # os.remove(db_file) if os.path.exists(db_file) else None
        create_db(db_file) if not os.path.exists(db_file) else None
        save_to_sql(reply, db_file)

        df_after = read_from_sql(db_file)
        print("Données insérées en base :")
        print(df_after.to_markdown(index=False), "\n")

        question = "Quel est le total de mes dépenses de transport ?"

        print(render_simple_markdown(f'**{question}**'))
        # print (text_to_sql(question))
        simulated_sql = "SELECT SUM(montant) FROM depenses WHERE categorie='transport';"
        sql_result = pd.read_sql_query(simulated_sql, sqlite3.connect(db_file)).iloc[
            0, 0
        ]
        print(f"Résultat SQL pur : {sql_result}")

        # answer = reformule_answer(
        #     "Quel est le total de mes dépenses de transport ?", sql_result
        # )

        simulated_answer = """
        Vous avez dépensé **40,00 € en transport**.
        """
        answer = simulated_answer

        # Dans ton main :
        print("Réponse reformulée :")

        print(render_simple_markdown(answer))

    except Exception as e:
        logger.error(f"Erreur finale: {e}")
