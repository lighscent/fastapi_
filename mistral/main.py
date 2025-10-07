import os
import dotenv
import time
import json
import sqlite3
import pandas as pd
from datetime import datetime
from typing import List, Dict, Union, Any

from mistralai import Mistral
import httpx
import logging
from colorama import init, Fore, Style

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logging.getLogger("httpx").setLevel(logging.WARNING)

# Charger les variables d'environnement
dotenv.load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

if not MISTRAL_API_KEY:
    raise ValueError("MISTRAL_API_KEY non trouvée dans .env")

# Configuration Mistral
MODEL = "mistral-large-latest"
client = Mistral(api_key=MISTRAL_API_KEY)

# Configuration globale
REAL_AI_USE = True
REAL_AI_USE = False  # Mettre à False pour ne PAS utiliser l'API réelle


def safe_chat_request(
    messages: List[Dict[str, str]], max_retries: int = 5, max_tokens: int = 300
) -> str:
    """
    Effectue une requête chat avec retry automatique.

    Args:
        messages: Liste des messages pour l'IA
        max_retries: Nombre max de tentatives
        max_tokens: Limite de tokens

    Returns:
        str: Réponse du modèle IA

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
                temperature=0.7,
            )
            return response.choices[0].message.content

        except httpx.HTTPStatusError as e:
            last_exception = e
            if e.response.status_code == 429:
                wait_time = min(2**attempt, 30)
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


def structured_data(spending_text: str) -> List[Dict[str, str]]:
    """
    Transforme un texte de dépense en messages structurés pour l'IA.

    Args:
        spending_text: Description de la dépense

    Returns:
        List[Dict[str, str]]: Messages formatés pour l'IA
    """
    system_prompt = """
    Tu es un assistant intelligent de dépense. Je souhaite te donner une description de mes dépenses et je souhaite que tu transformes la description en format json avec les champs suivants.

    designation : la chose pour laquelle la dépense a été effectuée,
    moyen_paiement : Le moyen de paiement dans la liste [Cash, Mobile money, Chèque, Carte de crédit],
    categorie : la catégorie de la dépense dans cette liste: 
    [transport, shopping, electricité, eau, loyer, voiture, television, sport, santé, loisirs, autres]
    montant : le montant de la dépense

    Tu ne retournes que le format json. Aucun autre texte.
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": spending_text},
        {
            "role": "user",
            "content": "Pour le taxi pour rentrer, j'ai fait un chèque de 30 euros.",
        },
        {
            "role": "user",
            "content": "j'ai acheté des pâtes pour 25 euros par carte bancaire.",
        },
    ]
    return messages


def simu_reponse() -> List[Dict[str, Union[str, int]]]:
    """
    Retourne des données de dépenses simulées pour les tests.

    Returns:
        List[Dict[str, Union[str, int]]]: Liste de dépenses simulées
    """
    return [
        {
            "designation": "Transport en commun",
            "moyen_paiement": "Cash",
            "categorie": "transport",
            "montant": 20,
        },
        {
            "designation": "Taxi retour",
            "moyen_paiement": "Chèque",
            "categorie": "transport",
            "montant": 30,
        },
        {
            "designation": "Achats alimentaires - Pâtes",
            "moyen_paiement": "Carte de crédit",
            "categorie": "shopping",
            "montant": 27,
        },
    ]


def create_db(db_file: str) -> None:
    """
    Crée la base de données SQLite avec la table depenses.

    Args:
        db_file: Chemin du fichier de base de données
    """
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS depenses (
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

    conn.commit()
    conn.close()


def save_to_sql(
    data: List[Dict[str, Union[str, int]]], db_file: str = "depenses.db"
) -> None:
    """
    Sauvegarde les données de dépenses dans la base SQLite.

    Args:
        data: Liste des dépenses à sauvegarder
        db_file: Chemin du fichier de base de données
    """
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    current_date = datetime.now().strftime("%Y-%m-%d")

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
                current_date,
            ),
        )

    conn.commit()
    conn.close()


def read_from_sql(db_file: str = "depenses.db") -> pd.DataFrame:
    """
    Lit les dernières dépenses depuis la base de données.

    Args:
        db_file: Chemin du fichier de base de données

    Returns:
        pd.DataFrame: DataFrame contenant les dépenses
    """
    conn = sqlite3.connect(db_file)
    df = pd.read_sql_query("SELECT * FROM depenses ORDER BY id DESC LIMIT 10", conn)
    conn.close()
    return df


def text_to_sql(question: str) -> str:
    """
    Convertit une question en langage naturel en requête SQL.

    Args:
        question: Question de l'utilisateur

    Returns:
        str: Requête SQL générée
    """
    system_prompt = """
    J'ai une table SQL nommée "depenses" avec les colonnes suivantes :
        id INTEGER PRIMARY KEY,
        date DATE,
        designation TEXT,
        categorie TEXT,
        moyen_paiement TEXT,
        montant REAL
        
    Transforme la question suivante en requête SQL qui répond à la question. 
    Tu ne retournes que la requête SQL, aucun autre texte introductif.
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question},
    ]

    return safe_chat_request(messages)


def reformule_answer(user_question: str, sql_result: Union[float, int, str]) -> str:
    """
    Reformule la réponse SQL en langage naturel.

    Args:
        user_question: Question originale de l'utilisateur
        sql_result: Résultat de la requête SQL

    Returns:
        str: Réponse reformulée en français
    """
    system_prompt = """
    En te basant sur une table SQL avec le schéma suivant, génère une réponse courte en langage naturel :
        id INTEGER PRIMARY KEY,
        date DATE,
        designation TEXT,
        categorie TEXT,
        moyen_paiement TEXT,
        montant REAL
    """

    user_prompt = f"""
    Voici la question qu'a posé l'utilisateur : {user_question}
    La réponse : {sql_result}
    Si la réponse est un montant, l'unité monétaire est euros.
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    return safe_chat_request(messages)
def render_simple_markdown(text: str) -> str:
    """
    Applique un rendu simple du Markdown avec des couleurs ANSI.
    """
    import re

    # Gras (**texte**)
    text = re.sub(
        r"\*\*(.*?)\*\*", 
        f"{Fore.YELLOW}{Style.BRIGHT}\\1{Style.RESET_ALL}", 
        text
    )

    # Italique (*texte*)
    text = re.sub(
        r"(?<!\*)\*([^*]+?)\*(?!\*)", 
        f"{Fore.CYAN}\\1{Style.RESET_ALL}", 
        text
    )

    # Lignes de séparation
    text = text.replace("---", "─" * 77)

    return text


def main() -> None:
    """
    Fonction principale du programme.
    """
    # Initialisation
    # init()  # Colorama

    # Configuration
    MESSAGE_INI = "J'ai payé 20 euros en cash pour le transport."
    DB_FILE = "depenses.db"
    question = "Quel est le total de mes dépenses de transport ?"

    # Création de la base si nécessaire
    if not os.path.exists(DB_FILE):
        create_db(DB_FILE)

    # Initialisation des données
    reply = []

    # Récupération des données (IA ou simulation)
    if REAL_AI_USE:
        try:
            messages = structured_data(MESSAGE_INI)
            json_reply = safe_chat_request(messages)
            parsed_reply = json.loads(json_reply)

            # Normalisation en liste
            if isinstance(parsed_reply, dict):
                reply = [parsed_reply]
            elif isinstance(parsed_reply, list):
                reply = parsed_reply
            else:
                logger.error(f"Format de réponse inattendu: {type(parsed_reply)}")
                reply = simu_reponse()

        except Exception as e:
            logger.error(f"Erreur en mode réel, passage en simulation: {e}")
            reply = simu_reponse()
    else:
        reply = simu_reponse()

    # Affichage et traitement
    print("─" * 77)
    print(render_simple_markdown(f"Message initial : **{MESSAGE_INI}**\n"))

    if reply:
        # Affichage des données récupérées
        df = pd.DataFrame(reply)
        print(render_simple_markdown("*Données récupérées en réponse :*"))
        print(df.to_markdown(index=False), "\n")

        # Sauvegarde en base
        save_to_sql(reply, DB_FILE)

        # Traitement de la question
        print(render_simple_markdown(f"Question posée: **{question}**"))

        # Exécution de la requête SQL
        sql_query = "SELECT SUM(montant) FROM depenses WHERE categorie='transport';"

        try:
            conn = sqlite3.connect(DB_FILE)
            sql_result = pd.read_sql_query(sql_query, conn).iloc[0, 0]
            conn.close()

            print(render_simple_markdown(f"Résultat SQL pur : **{int(sql_result)}**"))

            # Reformulation de la réponse
            if REAL_AI_USE:
                answer = reformule_answer(question, sql_result)
            else:
                answer = f"Vous avez dépensé {int(sql_result)} euros en transport."

            print("Réponse reformulée :", render_simple_markdown(f"**{answer}**"))

        except Exception as e:
            logger.error(f"Erreur SQL: {e}")
    else:
        logger.error("Aucune donnée à traiter")


if __name__ == "__main__":
    main()
    print ('Mode', 'REAL' if REAL_AI_USE else 'SIMU', 'terminé.')
