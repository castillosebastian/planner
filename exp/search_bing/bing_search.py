import os
from bs4 import BeautifulSoup
import requests
import json
import unicodedata
import re
from requests.exceptions import RequestException
from time import sleep
import time
from llama_index.core.node_parser import SentenceSplitter
from dotenv import load_dotenv
load_dotenv()

def clean_and_split_text(pages):
    cleaned_pages = []
    for page in pages:
        try:
            content = page["content"]
            # Check for PDF or non-textual content patterns
            if "%PDF-" in content or re.search(r'\bxref\b|\bstream\b|\bendobj\b', content):
                print("Skipping PDF or non-textual content.")
                continue            
            # Replace single newlines with spaces
            content = page["content"].replace("\n", " ")
            # Replace multiple spaces with a single space
            content = " ".join(content.split())
            # Normalize to NFKC to combine characters and diacritics
            content = unicodedata.normalize('NFKC', content)
            # Remove non-ASCII characters
            content = content.encode('ascii', 'ignore').decode('ascii')
            # Split the content into sentences
            content = SentenceSplitter(chunk_size=1000).split_text(content)
            # Update the page content
            page["content"] = content
            cleaned_pages.append(page)
        except Exception as e:
            print(f"Error processing page: {e}")
            continue
    return cleaned_pages


def get_embedding(text):
    pass

def score_page(embedding, keywords):
    pass


def fetch_pages(keywords, subscription_key, num_pages):
    search_url = "https://api.bing.microsoft.com/v7.0/search"
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    params = {"q": keywords, "textDecorations": False, "textFormat": "HTML", "count": num_pages}

    session = requests.Session()  # Using a session object
    try:
        response = session.get(search_url, headers=headers, params=params, timeout=4)
        response.raise_for_status()
        search_results = response.json()
    except RequestException as e:
        print(f"Failed to retrieve search results: {e}")
        return []

    bing_search_results = []

    for result in search_results.get("webPages", {}).get("value", []):
        url = result.get("url")
        if url and not url.endswith(".pdf"):
            try:
                page_response = session.get(url, timeout=4)
                page_response.raise_for_status()
                soup = BeautifulSoup(page_response.text, "html.parser")
                content = soup.get_text()
                if content:
                    bing_search_results.append({
                        'url': url,
                        'content': content,
                        'content_len': len(content)
                    })
            except RequestException as e:
                print(f"Error downloading page {url}: {e}")

    return bing_search_results


def main(subscription_key=None, 
        keywords=None,
        num_pages=10):
    
    start = time.time()
    results = fetch_pages(keywords, subscription_key, num_pages)
    end = time.time()
    print(f"Time to fetch pages: {end - start} seconds")

    # Clean Text
    start = time.time()
    cleaned_results = clean_and_split_text(results)
    end = time.time()
    print(f"Time to clean text: {end - start} seconds")

    
    # Save search results as json file
    with open("search_results.json", "w", encoding="utf-8") as file:
        json.dump(cleaned_results, file, ensure_ascii=False, indent=4)


    #https://docs.llamaindex.ai/en/stable/examples/vector_stores/FaissIndexDemo/

    # Get embedding for each page
    for page in cleaned_results:
        page["embedding"] = get_embedding(page["content"])

    # Score each page based on the embedding and the keywords
    for page in cleaned_results:
        page["score"] = score_page(page["embedding"], keywords)

    # Sort the results by score in descending order
    #cleaned_results.sort(key=lambda x: x["score"], reverse=True)

    # Select the top 3 pages
    #cleaned_results = cleaned_results[:3]

    # Print the top 3 pages
    #for i, page in enumerate(cleaned_results):
    #    print(f"Page {i+1}: {page['url']}")
            
    ## Example usage
    #search_and_rank("finance function", 10)

    print(cleaned_results)
    print("Search and download complete.")

if __name__ == "__main__":  
    subscription_key = os.environ['BING_SEARCH_KEY']
    keywords = "finance function"
    num_pages = 8
    main(subscription_key=subscription_key, 
         keywords = keywords, num_pages=num_pages)
   


