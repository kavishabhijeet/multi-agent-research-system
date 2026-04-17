from dotenv import load_dotenv
load_dotenv()
from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(querry : str) -> str:
    """Search the web for recent and reliable information on a topic. Returns Titles, URLs and snippets."""
    results = tavily.search(query=querry,max_results=3)
    out =[]

    for r in results['results']:
        out.append(
            f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:200]}\n"
        )
    return "\n----\n".join(out)
print(web_search.invoke("What is news of war"))    

@tool
def scrap_url(url : str) -> str:
    """Scrape and return clean text content from a given URL for deeper reading."""
    try:
        resp = requests.get(url, timeout=8, headers={"User-Agent: Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, "htnl.parser")
        for tag in soup(["script","style","nav","footer"]):
            tag.decompose()
        return soup.get_text(separator=" ",strip=True)[:2100]
    except Exception as e:
        return f"Couldnot scrape URL: {str(e)}"    
