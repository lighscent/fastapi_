import os, dotenv, time
from mistralai import Mistral
import httpx
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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


if __name__ == "__main__":
    messages = [{"role": "user", "content": "Quel est le meilleur fromage français ?"}]

    try:
        reply = safe_chat_request(messages)
        print("Réponse :", reply)
    except Exception as e:
        logger.error(f"Erreur finale: {e}")
