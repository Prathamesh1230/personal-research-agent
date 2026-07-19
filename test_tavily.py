from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
results = client.search("latest AI news 2026")

for r in results["results"][:3]:
    print(r["title"])
    print(r["url"])
    print()