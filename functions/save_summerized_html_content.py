import os
from config import open_ai_api_config


def save_summerized_html_content(html_list, website_name, extension):
    filename = f"summerized_{website_name}_{extension}.html"
    summerized_file_path = os.path.join(open_ai_api_config.BASE_DIR2, filename)
    with open(summerized_file_path, "w", encoding="utf-8") as file:
        for html in html_list:
            file.write(html + "\n")

    return  summerized_file_path
