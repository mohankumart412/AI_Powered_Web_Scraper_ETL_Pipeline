import re
import os
import json
import google.generativeai as genai
import traceback
from bs4 import BeautifulSoup
from datetime import datetime
from config import open_ai_api_config  # Assuming you have a similar config for Gemini
from functions import insert_into_db, get_html_content

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))  # Replace with your Gemini API key

model = genai.GenerativeModel('gemini-1.5-flash')  # Or 'gemini-pro-vision' if you need image support

def get_html_summary_by_gemini(html_file_paths):
    summarized_data_list = []
    for html_file_path in html_file_paths:
        print(datetime.now(), "start time for summarize the html content .............")
        with open(html_file_path, "r", encoding="utf-8") as html_file:
            html_content = html_file.read()

        soup = BeautifulSoup(html_content, 'html.parser')
        try:
            response = model.generate_content(
                f"{open_ai_api_config.SUMMARY_PROMPT}\n\n{soup}"  # Assuming you adapt your prompt for Gemini
            )

            data = response.text
            summarized_data_list.append(data)
            print(data)
        except Exception as e:
            traceback.print_exc()
            # open_ai_api_config.TOKEN_EXCEED = 1 #handle token exceed as needed
            continue
        print(datetime.now(), "end time for summarize the html content .............")
    return summarized_data_list

def get_data_from_html_file_by_gemini(url, html_file_path):
    print(datetime.now(), "start time for get final output data by chat api.............")
    with open(html_file_path, "r", encoding="utf-8") as html_file:
        html_content = html_file.read()

    structured_data = None

    soup = BeautifulSoup(html_content, 'html.parser')
    content_str = f"\n\n{soup}\n\n{'=' * 80}\n"
                
    open_ai_api_config.SUMMARY_HTML_TOKEN = get_html_content.count_tokens(content_str) # You might need to adapt token counting for Gemini
    try:
        response = model.generate_content(
            f"{open_ai_api_config.MAIN_PROMPT}\n\n{soup}" #Adapt prompt
        )

        extracted_data = response.text
        print(extracted_data)
    except Exception as e:
        traceback.print_exc()
        open_ai_api_config.TOKEN_EXCEED = 1 #Handle token exceed
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