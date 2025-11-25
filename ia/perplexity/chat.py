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
resp = client.chat.completions.create(
    model="sonar-small-chat",
    messages=[{"role": "user", "content": "Qu'est-ce que GPT-5 ?"}],
)

print(resp.choices[0].message["content"])
