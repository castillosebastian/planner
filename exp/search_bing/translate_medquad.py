import os 
import pandas as pd
import time
import sys
import json
import inspect
import asyncio
import textwrap
import google.generativeai as genai
# Get the root directory of your project (the directory containing 'src' and 'plugins')
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
pluginDirectory = "plugins"
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
model = genai.GenerativeModel('gemini-pro')
medquad = pd.read_csv('data/medquad.csv')
medquad = medquad.head(3)

def save_to_file(data, file_path='data/translated_qa_pairs.json'):
    try:
        with open(file_path, 'a') as f:
            f.write(json.dumps(data) + '\n')
    except Exception as e:
        print(f"Failed to save data: {e}")

async def main() -> None:

    max_retries = 3
    for index, row in medquad.iterrows():
        question = row['question']
        answer = row['answer']
        focus_area = row['focus_area']
        
        qa_pair = json.dumps({'question': question, 'answer': answer, 'focus_area': focus_area})

        for attempt in range(max_retries):
            try:
                response = model.generate_content(textwrap.dedent("""\
                "Please translate the provided 'question', 'answer' and 'focus_area' into Spanish, and format the response as a JSON object using the schema below:

                {
                    "question": "[QUESTION]",
                    "answer": "[ANSWER]",
                    "focus_area": "[FOCUS_AREA]"
                }
                
                Important: Ensure you return a single, valid JSON text.

                Question, answer and focus area to translate:"
                """) + qa_pair)

                json_text = response.text.strip('`\r\n ').removeprefix('json')

                qa_pair_dict = json.loads(json_text)
                qa_pair_dict['source'] = row['source']
                
                # If successful:
                save_to_file(qa_pair_dict)
                break
            except Exception as e:
                print(f"Attempt {attempt+1} failed: {e}")
                time.sleep(2)  # Adjust retry wait time as needed
        else:
            print(f"Failed to process row {index}. Continuing with next.")
        
        time.sleep(1)  # Adjust based on rate limit

        progress = (index + 1) / medquad.shape[0] * 100
        print(f"Progress: {progress:.2f}%")
        

if __name__ == "__main__":   
    asyncio.run(main())
