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
from sentence_transformers import SentenceTransformer, util
from sentence_transformers.util import cos_sim
from dotenv import load_dotenv
load_dotenv()

# Embedding with SentenceTransformer
# https://www.sbert.net/docs/pretrained_models.html
#https://huggingface.co/hkunlp/instructor-large
# To work locally do:
#   git clone https://huggingface.co/hkunlp/instructor-large
#   git clone https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2

#model = SentenceTransformer('./instructor-large')
model = SentenceTransformer('./all-MiniLM-L6-v2')

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
            new_content = {
                "url": page["url"],
                "content": content,            
            }            
            # Update the page content            
            cleaned_pages.append(new_content)

        except Exception as e:
            print(f"Error processing page: {e}")
            continue
    return cleaned_pages


def get_embedding(embedding_model, doc):                
    return  embedding_model.encode(doc)    

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
    # with open("search_results.json", "w", encoding="utf-8") as file:
    #     json.dump(cleaned_results, file, ensure_ascii=False, indent=4)         
    # Instruct-large
    # query = "what is a finance function?"
    # query_instruction = (
    #     "Represent the user's question for retrieving supporting documents: "
    # )    
    # corpus_instruction = "Represent the BingSearch document for retrieval: "
    # query_embedding = model.encode(query, prompt=query_instruction)
    # corpus_embeddings = model.encode(cleaned_results, prompt=corpus_instruction)
    # similarities = cos_sim(query_embedding, corpus_embeddings)
    # print(similarities)
    
    # All-MiniLM-L6-v2
    start = time.time()
    query_embedding = model.encode(keywords, convert_to_tensor=True)
    scored_documents = []
    for docs in cleaned_results:
        for chunk in docs["content"]:            
            embedding = get_embedding(model, chunk)
            score = cos_sim(query_embedding, embedding)
            url = docs["url"]
            scored_documents.append((score.item(), chunk, url))

    # Sort by score in descending order
    scored_documents.sort(reverse=True, key=lambda x: x[0])
    end = time.time()
    print(f"Time score documents: {end - start} seconds")
    
    # Select the top 5 pages
    top_documents = scored_documents[:5]

    # Print top N documents and their scores
    for score, doc, url in top_documents:
        print('-'*50)
        print(f"Score: {score},\nURL: {url},\nDocument: {doc}")
        print('-'*50)

    # Save top documents as json file
    with open("top_documents.json", "w", encoding="utf-8") as file:
        json.dump(top_documents, file, ensure_ascii=False, indent=4)

if __name__ == "__main__":  
    subscription_key = os.environ['BING_SEARCH_KEY']
    keywords = "finance function"
    num_pages = 8
    main(subscription_key=subscription_key, 
         keywords = keywords, num_pages=num_pages)
   


