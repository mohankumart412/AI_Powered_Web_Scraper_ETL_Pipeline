import re
import os
import json
import traceback
from datetime import datetime
from bs4 import BeautifulSoup
from together import Together
from config import open_ai_api_config
from functions import insert_into_db, get_html_content


# client = Together()  # Initialize Together client

client = Together(api_key=open_ai_api_config.API_KEY)

def get_html_summary_by_together_api(html_file_paths):
    summarized_data_list = []
    for html_file_path in html_file_paths:
        print(datetime.now(), "start time for summarize the html content .............")
        with open(html_file_path, "r", encoding="utf-8") as html_file:
            html_content = html_file.read()

        soup = BeautifulSoup(html_content, 'html.parser')
        try:
            stream = client.chat.completions.create(
                model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
                messages=[
                    {
                        "role": "user",
                        "content": f"{open_ai_api_config.SUMMARY_PROMPT}\n\n{soup}",
                    }
                ],
                stream=True,
            )

            for chunk in stream:
                summary = chunk.choices[0].delta.content or ""
                print(summary)
            
            summarized_data_list.append(summary)
            print(summary)
        except Exception as e:
            traceback.print_exc()
            continue
        print(datetime.now(), "end time for summarize the html content .............")
    return summarized_data_list


def get_data_from_html_file_by_together_api(url, html_file_path):
    print(datetime.now(), "start time for get final output data by chat api.............")
    with open(html_file_path, "r", encoding="utf-8") as html_file:
        html_content = html_file.read()

    structured_data = None

    soup = BeautifulSoup(html_content, 'html.parser')
    content_str = f"\n<!-- summary file  -->\n{soup}\n\n{'=' * 80}\n"

    open_ai_api_config.SUMMARY_HTML_TOKEN = get_html_content.count_tokens(content_str)
    try:
        stream = client.chat.completions.create(
            model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
            messages=[
                {
                    "role": "user",
                    "content": f"{open_ai_api_config.MAIN_PROMPT}\n\n{content_str}",
                }
            ],
            stream=True,
        )

        for chunk in stream:
            extracted_data = chunk.choices[0].delta.content or ""
            print(chunk.choices[0].delta.content or "", end="", flush=True)
        
        print(extracted_data)
    except Exception as e:
        traceback.print_exc()
        open_ai_api_config.TOKEN_EXCEED = 1
        insert_into_db.update_flag_for_token_error(url)
        return None

    # Extract JSON dictionary using regex
    match = re.search(r"\{.*\}", extracted_data, re.DOTALL)
    if match:
        json_str = match.group(0)  # Extract the dictionary
        try:
            structured_data = json.loads(json_str)  # Convert to dictionary
            print(structured_data)  # Output the dictionary
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
            structured_data = None
    else:
        print("No dictionary found")

    if structured_data:
        open_ai_api_config.PARAMETER_COUNT = sum(
            1 if (v and v != "Null" and v != "[]") else 0 for v in structured_data.values()
        )
    
    return structured_data
