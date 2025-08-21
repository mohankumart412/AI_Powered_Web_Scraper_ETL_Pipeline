import os
import re
import time
import requests
from functions import insert_into_db
from bs4 import BeautifulSoup
from config import open_ai_api_config
from urllib.parse import urljoin, urlparse


def find_website_name(website_url):
    """Extract website name and domain extension."""
    domain = urlparse(website_url).netloc.replace("www.", "")
    parts = domain.split(".")
    return parts[0], ".".join(parts[1:])


def clean_html(body):
    """Remove unwanted elements like <script>, <style>, and other non-body tags."""
    # Remove all <script> and <style> elements
    for script_or_style in body(['script', 'style', 'noscript']):
        script_or_style.decompose()
    return body


def count_tokens(text):
    """Count tokens in text, accounting for contractions and hyphenated words."""
    # Regex to capture words and punctuation, handling cases like "I'm" or "don't"
    tokens = re.findall(r"\b\w+('\w+)?\b|[^\w\s]", text)
    return len(tokens)


# def get_html_content(links, file_path, website_name, tld):
#     """Fetch and save the body content of internal links, splitting files based on token count."""
#     file_index = 1
#     current_file_path = file_path
#     file_paths = [current_file_path]
    
#     with open(current_file_path, "w", encoding="utf-8") as file:
#         with open(file_path, "r", encoding="utf-8") as main_file:
#             main_content = main_file.read()
#             file.write(main_content)
    
#     current_tokens = count_tokens(main_content)
    
#     for link in links:
#         print(f"Fetching content from: {link}")
#         try:
#             response = requests.get(link, timeout=10)
#             response.raise_for_status()
            
#             soup = BeautifulSoup(response.text, 'html.parser')
#             body_content = soup.find('body')
            
#             if body_content:
#                 clean_content = clean_html(body_content)
#                 content_str = f"\n<!-- URL: {link} -->\n{clean_content}\n\n{'=' * 80}\n"
                
#                 content_tokens = count_tokens(content_str)
                
#                 # Check if adding this content exceeds the token limit
#                 if current_tokens + content_tokens > open_ai_api_config.TOKEN_LIMIT:
#                     file_index += 1
#                     current_file_path = os.path.join(open_ai_api_config.BASE_DIR1, f"{website_name}_{tld}_{file_index}.html")
#                     file_paths.append(current_file_path)
#                     current_tokens = 0
                    
#                 with open(current_file_path, "a", encoding="utf-8") as file:
#                     file.write(content_str)
#                     current_tokens += content_tokens
#             else:
#                 print(f"Body content not found for {link}")
        
#             time.sleep(1)
#         except Exception as e:
#             print(f"Error fetching content from {link}: {e}")
#     return file_paths


def get_html_content(links, file_path, website_name, tld):
    """Fetch and save the body content of internal links, splitting files based on token count and character count."""
    file_index = 1
    current_file_path = file_path
    file_paths = [current_file_path]
    
    with open(current_file_path, "w", encoding="utf-8") as file:
        with open(file_path, "r", encoding="utf-8") as main_file:
            main_content = main_file.read()
            file.write(main_content)
    
    current_tokens = count_tokens(main_content)

    open_ai_api_config.PAGE_LINK_TOKEN = {}
    
    for link in links:
        print(f"Fetching content from: {link}")
        try:
            response = requests.get(link, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            body_content = soup.find('body')
            
            if body_content:
                clean_content = clean_html(body_content)
                content_str = f"\n<!-- URL: {link} -->\n{clean_content}\n\n{'=' * 80}\n"
                
                content_tokens = count_tokens(content_str)
                open_ai_api_config.PAGE_LINK_TOKEN[link] = content_tokens
                # Check if adding this content exceeds the token limit or character limit (300,000)
                if current_tokens + content_tokens > open_ai_api_config.TOKEN_LIMIT or len(content_str) > open_ai_api_config.CHARACTER_LIMIT:
                    file_index += 1
                    current_file_path = os.path.join(open_ai_api_config.BASE_DIR1, f"{website_name}_{tld}_{file_index}.html")
                    file_paths.append(current_file_path)
                    current_tokens = 0
                    
                with open(current_file_path, "a", encoding="utf-8") as file:
                    file.write(content_str)
                    current_tokens += content_tokens
                    
                # Check if the total characters exceed the limit after writing the content
                if len(content_str) > open_ai_api_config.CHARACTER_LIMIT:
                    print(f"Content for {link} exceeds {open_ai_api_config.CHARACTER_LIMIT} characters.")
        
            else:
                print(f"Body content not found for {link}")
        
            time.sleep(1)
        except Exception as e:
            print(f"Error fetching content from {link}: {e}")
    return file_paths



def save_main_page(url, website_name, extension):
    """Fetch and save the body content of the main page HTML to a file, excluding scripts and styles."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract only the body content
        body_content = soup.find('body')

        if body_content:
            # Clean the body content to remove scripts and styles
            clean_content = clean_html(body_content)

            # Save the cleaned body content to a file
            file_path = os.path.join(open_ai_api_config.BASE_DIR1, f"{website_name}_{extension}_1.html")
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(str(clean_content))  # Write only the cleaned body content

            print(f"Main page body content saved to: {file_path}")
            return file_path
        else:
            print(f"Body content not found for {url}")
            open_ai_api_config.HTTP_ERROR = 1
            insert_into_db.update_flag_for_http_error()
            return None

    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        open_ai_api_config.HTTP_ERROR = 1
        insert_into_db.update_flag_for_http_error()
        return None
