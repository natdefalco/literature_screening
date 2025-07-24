
import requests
import xml.etree.ElementTree as ET
import pandas as pd
from urllib.parse import quote
import time
import datetime
import json

# --- API Keys and URLs ---
SPRINGER_API_KEY = "your_key" #Springer: Get a free API key at https://dev.springernature.com
SPRINGER_URL = "https://api.springernature.com/meta/v2/json"
CORE_API_KEY = "your_key" #CORE: Register at https://core.ac.uk/services#api
CORE_URL = "https://api.core.ac.uk/v3/search/works"
ARXIV_URL = "http://export.arxiv.org/api/query"
SEMANTIC_URL = "https://api.semanticscholar.org/graph/v1/paper/search"
SCOPUS_API_KEY = "your_key" #Scopus (Elsevier): Requires institutional access or personal API key: https://dev.elsevier.com
OPENALEX_URL = "https://api.openalex.org/works"
PUBMED_SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
CROSSREF_URL = "https://api.crossref.org/works"

# --- Search Parameters --- # 🔠 Define your search topic using Boolean logic, quotes, AND/OR/NOT etc.
SEARCH_QUERY = ('"see_instructions"') #check the instruction for your query
ENCODED_QUERY = quote(SEARCH_QUERY) # 🌐 Encode the search term for safe use in URLs
TOTAL_PAPERS = 20

# --- Shared Result List ---
results = []

def papers_left():
    return TOTAL_PAPERS - len(results)

# --- Springer ---
def fetch_springer():
    page = 1
    print("🔍 Fetching from Springer...")
    while papers_left() > 0:
        url = f"{SPRINGER_URL}?q={ENCODED_QUERY}&api_key={SPRINGER_API_KEY}&p=10&s={page}"
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            data = response.json()
            for record in data.get("records", []):
                results.append({
                    "source": "Springer",
                    "title": record.get("title", "N/A"),
                    "authors": ", ".join([a.get("creator", "") for a in record.get("creators", [])]),
                    "year": record.get("publicationDate", "N/A")[:4],
                    "abstract": record.get("abstract", "N/A"),
                    "url": record.get("url", [{}])[0].get("value", "N/A")
                })
                if papers_left() <= 0:
                    return
            page += 1
            time.sleep(5)
        except Exception as e:
            print(f"❌ Springer error: {e}")
            break

# --- CORE ---
def fetch_core():
    offset = 0
    print("🔍 Fetching from CORE...")
    while papers_left() > 0:
        url = f"{CORE_URL}?apiKey={CORE_API_KEY}&q={ENCODED_QUERY}&limit=10&offset={offset}"
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            data = response.json()
            for item in data.get("results", []):
                results.append({
                    "source": "CORE",
                    "title": item.get("title", "N/A"),
                    "authors": "N/A",
                    "year": item.get("yearPublished", "N/A"),
                    "abstract": item.get("description", "N/A"),
                    "url": item.get("downloadUrl", "N/A")
                })
                if papers_left() <= 0:
                    return
            offset += 10
            time.sleep(5)
        except Exception as e:
            print(f"❌ CORE error: {e}")
            break

# --- arXiv ---
def fetch_arxiv():
    start = 0
    print("🔍 Fetching from arXiv...")
    while papers_left() > 0:
        url = f"{ARXIV_URL}?search_query=all:{ENCODED_QUERY}&start={start}&max_results=10"
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            root = ET.fromstring(response.text)
            ns = {'arxiv': 'http://www.w3.org/2005/Atom'}
            for entry in root.findall('arxiv:entry', ns):
                results.append({
                    "source": "arXiv",
                    "title": entry.find('arxiv:title', ns).text.strip(),
                    "authors": ", ".join([a.find('arxiv:name', ns).text for a in entry.findall('arxiv:author', ns)]),
                    "year": entry.find('arxiv:published', ns).text[:4],
                    "abstract": entry.find('arxiv:summary', ns).text.strip(),
                    "url": entry.find('arxiv:id', ns).text.strip()
                })
                if papers_left() <= 0:
                    return
            start += 10
            time.sleep(5)
        except Exception as e:
            print(f"❌ arXiv error: {e}")
            break

# --- Semantic Scholar ---
def fetch_semanticscholar():
    offset = 0
    print("🔍 Fetching from Semantic Scholar...")
    headers = {"Accept": "application/json"}
    while papers_left() > 0:
        url = f"{SEMANTIC_URL}?query={ENCODED_QUERY}&limit=10&offset={offset}&fields=title,abstract,authors,year,url"
        try:
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            data = response.json()
            for paper in data.get("data", []):
                results.append({
                    "source": "Semantic Scholar",
                    "title": paper.get("title", "N/A"),
                    "authors": ", ".join([a.get("name", "") for a in paper.get("authors", [])]),
                    "year": paper.get("year", "N/A"),
                    "abstract": paper.get("abstract", "N/A"),
                    "url": paper.get("url", "N/A")
                })
                if papers_left() <= 0:
                    return
            offset += 10
            time.sleep(5)
        except Exception as e:
            print(f"❌ Semantic Scholar error: {e}")
            break

# --- Scopus / Elsevier ---
def fetch_elsevier_scopus():
    print("🔍 Fetching from Scopus (Elsevier)...")
    headers = {
        "X-ELS-APIKey": SCOPUS_API_KEY,
        "Accept": "application/json"
    }
    url = f"https://api.elsevier.com/content/search/scopus?query={ENCODED_QUERY}&count=10"
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
        for item in data.get("search-results", {}).get("entry", []):
            results.append({
                "source": "Scopus",
                "title": item.get("dc:title", "N/A"),
                "authors": item.get("dc:creator", "N/A"),
                "year": item.get("prism:coverDate", "N/A")[:4],
                "abstract": item.get("dc:description", "N/A"),
                "url": item.get("prism:url", "N/A")
            })
            if papers_left() <= 0:
                return
    except Exception as e:
        print(f"❌ Scopus error: {e}")

# --- OpenAlex ---
def fetch_openalex():
    print("🔍 Fetching from OpenAlex...")
    try:
        response = requests.get(f"{OPENALEX_URL}?search={ENCODED_QUERY}&per-page=10", timeout=15)
        response.raise_for_status()
        data = response.json()
        for item in data.get("results", []):
            results.append({
                "source": "OpenAlex",
                "title": item.get("title", "N/A"),
                "authors": ", ".join([a.get("author", {}).get("display_name", "") for a in item.get("authorships", [])]),
                "year": item.get("publication_year", "N/A"),
                "abstract": item.get("abstract", "N/A"),
                "url": item.get("id", "N/A")
            })
            if papers_left() <= 0:
                return
    except Exception as e:
        print(f"❌ OpenAlex error: {e}")

# --- PubMed ---
def fetch_pubmed():
    print("🔍 Fetching from PubMed...")
    try:
        search_resp = requests.get(f"{PUBMED_SEARCH_URL}?db=pubmed&retmode=json&retmax=10&term={ENCODED_QUERY}")
        search_resp.raise_for_status()
        ids = search_resp.json().get("esearchresult", {}).get("idlist", [])
        if not ids:
            return
        ids_str = ",".join(ids)
        fetch_resp = requests.get(f"{PUBMED_FETCH_URL}?db=pubmed&id={ids_str}&retmode=xml")
        fetch_resp.raise_for_status()
        root = ET.fromstring(fetch_resp.text)
        for article in root.findall(".//PubmedArticle"):
            title = article.findtext(".//ArticleTitle", "N/A")
            year = article.findtext(".//PubDate/Year", "N/A")
            abstract = article.findtext(".//AbstractText", "N/A")
            authors = ", ".join([
                a.findtext("LastName", "") + " " + a.findtext("ForeName", "")
                for a in article.findall(".//Author")
            ])
            results.append({
                "source": "PubMed",
                "title": title,
                "authors": authors,
                "year": year,
                "abstract": abstract,
                "url": f"https://pubmed.ncbi.nlm.nih.gov/{ids[0]}"
            })
            if papers_left() <= 0:
                return
    except Exception as e:
        print(f"❌ PubMed error: {e}")

# --- Crossref ---
def fetch_crossref():
    print("🔍 Fetching from Crossref...")
    try:
        response = requests.get(f"{CROSSREF_URL}?query={ENCODED_QUERY}&rows=10", timeout=15)
        response.raise_for_status()
        data = response.json()
        for item in data.get("message", {}).get("items", []):
            results.append({
                "source": "Crossref",
                "title": item.get("title", ["N/A"])[0],
                "authors": ", ".join([f"{a.get('given', '')} {a.get('family', '')}" for a in item.get("author", [])]),
                "year": str(item.get("published-print", {}).get("date-parts", [[None]])[0][0]),
                "abstract": item.get("abstract", "N/A"),
                "url": item.get("URL", "N/A")
            })
            if papers_left() <= 0:
                return
    except Exception as e:
        print(f"❌ Crossref error: {e}")

# --- Save and Main ---
def save_to_excel():
    df = pd.DataFrame(results)
    df.to_excel("literature_screening.xlsx", index=False)
    print("✅ Saved to 'literature_screening.xlsx'")

def main():
    start_time = datetime.datetime.now()
    fetch_springer()
    fetch_core()
    fetch_arxiv()
    fetch_semanticscholar()
    fetch_elsevier_scopus()
    fetch_openalex()
    fetch_pubmed()
    fetch_crossref()
    save_to_excel()
    end_time = datetime.datetime.now()
    print(f"📊 Total papers fetched: {len(results)}")
    print(f"⏱️ Runtime: {end_time - start_time}")

if __name__ == "__main__":
    main()
