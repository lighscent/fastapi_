import os, dotenv
from perplexity import Perplexity

# print(dir(Perplexity))
# exit()
# exit()

dotenv.load_dotenv()

key = os.environ.get("PERPLEXITY_API_KEY")
print("API Key:", os.environ.get("PERPLEXITY_API_KEY"))
exit()

client = Perplexity(api_key=key)

# Exemple : requête de recherche
search = client.search.create(query="Qu'est-ce que le GPT-5 ?", max_results=5)

print("### Réponse synthétique :")
for result in search.results:
    print("-", result.title, "→", result.url)

# Exemple : chat/completion
response = client.chat.create(
    model="sonar-small-online",
    messages=[{"role": "user", "content": "Explique-moi GPT-5"}],
)

print("\n### Réponse du modèle :")
print(response.output_text)
