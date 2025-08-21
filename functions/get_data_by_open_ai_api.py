import re
import os
import json
import openai
import traceback
from bs4 import BeautifulSoup
from datetime import datetime
from config import open_ai_api_config
from functions import insert_into_db, get_html_content


openai.api_key = os.getenv("OPENAI_API_KEY")


def get_html_summary_by_open_api(html_file_paths):
    summarized_data_list = []
    for html_file_path in html_file_paths:
        print(datetime.now(), "start time for summaerize the html content .............")
        with open(html_file_path, "r", encoding="utf-8") as html_file:
            html_content = html_file.read()

        soup = BeautifulSoup(html_content, 'html.parser')
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", "content": f"{open_ai_api_config.SUMMARY_PROMPT}\n\n{soup}"}
                ]
            )

            data = response["choices"][0]["message"]["content"]
            summarized_data_list.append(data)
            print(data)
        except Exception as e:
            traceback.print_exc()
            # open_ai_api_config.TOKEN_EXCEED = 1
            continue
        print(datetime.now(), "end time for summaerize the html content .............")
    return summarized_data_list


def get_data_from_html_file_by_open_api(url, html_file_path):
    print(datetime.now(), "start time for get final output data by chat api.............")
    with open(html_file_path, "r", encoding="utf-8") as html_file:
        html_content = html_file.read()

    structured_data = None

    soup = BeautifulSoup(html_content, 'html.parser')
    content_str = f"\n<!-- summary file  -->\n{soup}\n\n{'=' * 80}\n"
                
    open_ai_api_config.SUMMARY_HTML_TOKEN = get_html_content.count_tokens(content_str)
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": f"{open_ai_api_config.MAIN_PROMPT}\n\n{soup}"}
            ]
        )

        extracted_data = response["choices"][0]["message"]["content"]
        print(extracted_data)
    except Exception as e:
        traceback.print_exc()
        open_ai_api_config.TOKEN_EXCEED = 1
        insert_into_db.update_flag_for_token_error()
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
