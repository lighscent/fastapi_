import dotenv, os, httpx, logging, time
from mistralai import Mistral


# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

dotenv.load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MODEL = "mistral-embed"

client = Mistral(api_key=MISTRAL_API_KEY)

# Phrases en français pour l'embedding
phrases_francaises = [
    "Quelle est la capitale de la France ?",
    "Trouvez-moi les monuments clés de cette ville.",
]

max_retries = 5
last_exception = None

for attempt in range(max_retries):
    try:
        embeddings_response = client.embeddings.create(
            model=MODEL, inputs=phrases_francaises
        )

        print("Embeddings générés pour les phrases françaises :")
        for i, phrase in enumerate(phrases_francaises):
            emb = embeddings_response[i].embedding
            print(f"{i+1}. {phrase}")
            print(
                f"   Dimension du vecteur : {len(emb)}"
            )
            print(f"   Premiers éléments : {emb[:5]}")
        print()

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
