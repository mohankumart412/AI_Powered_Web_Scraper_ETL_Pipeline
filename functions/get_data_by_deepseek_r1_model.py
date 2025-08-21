import re
import os
import json
import boto3
import traceback
from bs4 import BeautifulSoup
from datetime import datetime
from botocore.config import Config
from config import open_ai_api_config
from functions import get_html_content

config = Config(
    retries={
        'total_max_attempts': 10, 
        'mode': 'standard'
    }
)

session = boto3.session.Session()
br_runtime = session.client(
    service_name='bedrock-runtime', 
    region_name=open_ai_api_config.REGION_NAME, 
    config=config
)


br_runtime = boto3.client(
    service_name='bedrock-runtime', 
    region_name=open_ai_api_config.REGION_NAME, 
    aws_access_key_id=open_ai_api_config.AWS_ACCESS_KEY_ID, 
    aws_secret_access_key=open_ai_api_config.AWS_SECRET_ACCESS_KEY,
    config=config
)


def save_summerized_html_content(html_list, website_name, extension):
    filename = f"summerized_{website_name}_{extension}.html"
    summerized_file_path = os.path.join(open_ai_api_config.BASE_DIR2, filename)
    with open(summerized_file_path, "w", encoding="utf-8") as file:
        for html in html_list:
            file.write(html + "\n")

    return  summerized_file_path


def get_html_summary_by_bedrock(html_file_paths):
    summarized_data_list = []
    for html_file_path in html_file_paths:
        print(datetime.now(), "start time for summarize the html content .............")
        with open(html_file_path, "r", encoding="utf-8") as html_file:
            html_content = html_file.read()

        soup = BeautifulSoup(html_content, 'html.parser')
        try:
            # Truncate the HTML content to avoid exceeding the model's token limit
            max_length = 10000  # Adjust based on the model's token limit
            truncated_html = str(soup)[:max_length]

            # Prepare the request body
            body = json.dumps({
                'prompt': f"{open_ai_api_config.SUMMARY_PROMPT}\n\n{truncated_html}",
                'max_gen_len': 2048  # Adjust based on the model's limit
            })

            # Debug: Print the request body
            # print("Request body:", body)

            # Invoke the model
            response = br_runtime.invoke_model(
                modelId=open_ai_api_config.MODEL_ID, 
                body=body, 
                accept="application/json", 
                contentType="application/json"
            )

            # Read the response body
            invoke_response = json.loads(response["body"].read().decode("utf-8"))
            
            # Extract the summarized HTML content directly
            summarized_html = invoke_response.get("generation", "")  # Use the correct key if known
            if not summarized_html:
                print("No summarized HTML content found in the response.")
                continue  # Skip this file if no content is found

            # Append the summarized HTML to the list
            summarized_data_list.append(summarized_html)
            print(summarized_html)
        except Exception as e:
            traceback.print_exc()
            continue
        print(datetime.now(), "end time for summarize the html content .............")
    return summarized_data_list


def get_data_from_html_file_by_bedrock(url, html_file_path):
    print(datetime.now(), "start time for get final output data by chat api.............")
    with open(html_file_path, "r", encoding="utf-8") as html_file:
        html_content = html_file.read()

    structured_data = None

    soup = BeautifulSoup(html_content, 'html.parser')
    content_str = f"\n<!-- summary file  -->\n{soup}\n\n{'=' * 80}\n"
                
    open_ai_api_config.SUMMARY_HTML_TOKEN = get_html_content.count_tokens(content_str)
    try:
        response = br_runtime.invoke_model(
            modelId=open_ai_api_config.MODEL_ID, 
            body=json.dumps({
                'prompt': f"{open_ai_api_config.MAIN_PROMPT}\n\n{soup}",
                'max_gen_len': 4100
            }), 
            accept="application/json", 
            contentType="application/json"
        )

        invoke_response = json.loads(response["body"].read().decode("utf-8"))
        # extracted_data = invoke_response["generated_text"]
        print(invoke_response)
    except Exception as e:
        traceback.print_exc()
        TOKEN_EXCEED = 1
        # insert_into_db.insert_flag_for_token_error(url)
        return None

    # # Extract JSON dictionary using regex
    # match = re.search(r"\{.*\}", extracted_data, re.DOTALL)
    # if match:
    #     json_str = match.group(0)  # Extract the dictionary
    #     try:
    #         structured_data = json.loads(json_str)  # Convert to dictionary
    #         print(structured_data)  # Output the dictionary
    #     except json.JSONDecodeError as e:
    #         print("Error decoding JSON:", e)
    #         structured_data = None
    # else:
    #     print("No dictionary found")

    # if structured_data:
    #     open_ai_api_config.PARAMETER_COUNT = sum(
    #         1 if (v and v != "Null" and v != "[]") else 0 for v in structured_data.values()
    #     )
    #     print(open_ai_api_config.PARAMETER_COUNT, "parameters collected")
    
    # return structured_data    
