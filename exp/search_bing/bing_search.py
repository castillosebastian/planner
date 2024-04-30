import os
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
import json
load_dotenv()

subscription_key = os.environ['BING_SEARCH_KEY']

def get_embedding(text):
    pass

def score_page(embedding, keywords):
    pass

def search_and_rank(keywords, num_pages):
    # Bing search
    # https://github.com/Azure-Samples/cognitive-services-REST-api-samples/blob/master/python/Search/BingCustomSearchv7.py
    search_url = "https://api.bing.microsoft.com/v7.0/search"
   
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    params = {"q": keywords, "textDecorations": True, "textFormat": "HTML"}
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()

    # Extract text from num_pages pages of search results
    bing_search_results = []
    
    for result in search_results["webPages"]["value"][:num_pages]:
        
        # If the result does not have a URL or ends with 'pdf', skip it
        if "url" not in result or result["url"].endswith(".pdf"):
            continue
        url = result["url"]
        page = {'url': url}
        # Download the page with error handling
        try:
            response = requests.get(url)            
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error downloading page {url}: {e}")
            continue
        # Parse the page using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")
        page["content"] = soup.get_text()
        bing_search_results.append(page)

    # Clean text: remove newlines, extra spaces, etc.
    for page in bing_search_results:
        page["content"] = page["content"].replace("\n", " ")
        page["content"] = " ".join(page["content"].split())

    # Get embedding for each page
    for page in bing_search_results:
        page["embedding"] = get_embedding(page["content"])

    # Score each page based on the embedding and the keywords
    for page in bing_search_results:
        page["score"] = score_page(page["embedding"], keywords)

    # Sort the results by score in descending order
    bing_search_results.sort(key=lambda x: x["score"], reverse=True)

    # Select the top 3 pages
    bing_search_results = bing_search_results[:3]

    # Print the top 3 pages
    for i, page in enumerate(bing_search_results):
        print(f"Page {i+1}: {page['url']}")
    

    # Save search results as json file
    with open("search_results.json", "w", encoding="utf-8") as file:
        json.dump(bing_search_results, file, ensure_ascii=False, indent=4)

    print("Search and download complete.")

# Example usage
search_and_rank("finance function", 10)