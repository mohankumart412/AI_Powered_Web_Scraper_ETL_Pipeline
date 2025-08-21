import traceback
import pandas as pd
from datetime import datetime
from config import open_ai_api_config
from functions import extract_internal_links, get_html_content, get_data_by_open_ai_api, get_data_by_gemni_ai_api, save_summerized_html_content, insert_into_db


def calculate_run_time(start_time):
    end_time = datetime.now()
    run_time = end_time - start_time
    formatted_run_time = str(run_time).split(".")[0]  # Remove microseconds (HH:MM:SS)
    open_ai_api_config.RUN_TIME = formatted_run_time


def read_data_from_gldb():
    """
    Reads data from the table.
    """
    connection, cursor = open_ai_api_config.Gl_Database_Connection()
    df = pd.read_sql(open_ai_api_config.GL_SELECT_QUERY, con=connection)
    print(df.columns, "number of websites")
    print(df.shape[0])
    connection.close()
    return df


def main():
    try:
        df = read_data_from_gldb()
        for index, row in df.iterrows():
            url = row["gl_website"]
            open_ai_api_config.WEBSITE_URL = ""
            open_ai_api_config.NUM_PAGES = 0
            open_ai_api_config.PARAMETER_COUNT = 0
            open_ai_api_config.SUMMARY_HTML_TOKEN = 0
            open_ai_api_config.HTTP_ERROR = 0
            open_ai_api_config.IS_MORE_THAN_THRESHOLD = 0
            open_ai_api_config.TOKEN_EXCEED = 0
            open_ai_api_config.PAGE_LINK_TOKEN = None
            open_ai_api_config.NOT_INSERTED_FLAG = 0
            open_ai_api_config.WEBSITE_SCRAPE_DONE_FLAG = 0
            open_ai_api_config.RUN_TIME = 0


            # url = "http://www.caschiro.com/"
            open_ai_api_config.WEBSITE_URL = url

            start_time = datetime.now()
            website_name, tld = get_html_content.find_website_name(url)
            main_page_path = get_html_content.save_main_page(url, website_name, tld)

            if main_page_path:
                internal_links = extract_internal_links.extract_internal_links(main_page_path, url)
                open_ai_api_config.NUM_PAGES = len(internal_links)    

                if len(internal_links) > open_ai_api_config.MAXIMUM_LINKS_NUMBER:
                    open_ai_api_config.IS_MORE_THAN_THRESHOLD = 1
                    print(f"THis website url have more than {open_ai_api_config.MAXIMUM_LINKS_NUMBER} internal links", url)
                    insert_into_db.update_flag_for_more_than_threshold()
                    calculate_run_time(start_time)
                    insert_into_db.insert_log()

                elif len(internal_links) > 1:
                    total_file_paths = get_html_content.get_html_content(internal_links, main_page_path, website_name, tld)
                    if len(total_file_paths) > 1:
                        summerized_html_list = get_data_by_gemni_ai_api.get_html_summary_by_gemini(total_file_paths)
                        if summerized_html_list:
                            summerized_html_path = save_summerized_html_content.save_summerized_html_content(summerized_html_list, website_name, tld)
                            data = get_data_by_gemni_ai_api.get_data_from_html_file_by_gemini(url, summerized_html_path)
                            if data:
                                insert_into_db.update_data(data)
                                calculate_run_time(start_time)
                                insert_into_db.insert_log()
                            else:
                                calculate_run_time(start_time)
                                insert_into_db.insert_log()
                                continue
                        else:
                            insert_into_db.update_flag_for_token_error()
                            calculate_run_time(start_time)
                            insert_into_db.insert_log()
                            continue
                    else:
                        data = get_data_by_gemni_ai_api.get_data_from_html_file_by_gemini(url, total_file_paths[0])
                        if data:
                            insert_into_db.update_data(data)
                            calculate_run_time(start_time)
                            insert_into_db.insert_log()
                        else:
                            calculate_run_time(start_time)
                            insert_into_db.insert_log()
                            continue
                else:
                    get_html_content.get_html_content(internal_links, main_page_path, website_name, tld)
                    data = get_data_by_gemni_ai_api.get_data_from_html_file_by_gemini(url, main_page_path)
                    if data:
                            insert_into_db.update_data(data)
                            calculate_run_time(start_time)
                            insert_into_db.insert_log()
                    else:
                        calculate_run_time(start_time)
                        insert_into_db.insert_log()
                        continue
            else:
                calculate_run_time(start_time)
                insert_into_db.insert_log()
                continue

    except Exception as e:
        traceback.print_exc()


if __name__ == "__main__":
    print(datetime.now(), "script start time.............")
    main()
    print(datetime.now(), "script end time.............")
