import json
from config import open_ai_api_config


def commit_mysql_query_executer(query, values, fun_name):
    db_connection, db_cursor = open_ai_api_config.Gl_Database_Connection()
    try:
        db_cursor.execute(query, values)
        db_connection.commit()
        db_cursor.close()
        print(f"✅ Data Inserted Successfully for {fun_name}")
        if fun_name == "update_output_data":
            open_ai_api_config.WEBSITE_SCRAPE_DONE_FLAG = 1
    except Exception as e:
        print(f"❌ Database Commit Exception for {fun_name}: {e}")
        if fun_name == "update_output_data":
            update_flag_for_not_inserted()
            open_ai_api_config.NOT_INSERTED_FLAG = 1


def insert_log():
    query = f"""INSERT INTO {open_ai_api_config.LOG_TABLE_NAME} 
                (website, number_of_pages, parameter_count, summary_html_token, http_error, is_more_than_threshold, token_exceed, pages_links_tokens, not_inserted_flag, website_scrape_done_flag, run_time)
                VALUES (%(website)s, %(number_of_pages)s, %(parameter_count)s, %(summary_html_token)s, %(http_error)s, %(is_more_than_threshold)s, %(token_exceed)s, %(pages_links_tokens)s,  %(not_inserted_flag)s, %(website_scrape_done_flag)s, %(run_time)s)
            """
    values = {
        'website': open_ai_api_config.WEBSITE_URL,
        'number_of_pages': open_ai_api_config.NUM_PAGES if open_ai_api_config.NUM_PAGES else None,
        'parameter_count': open_ai_api_config.PARAMETER_COUNT if open_ai_api_config.PARAMETER_COUNT else None,
        'summary_html_token': open_ai_api_config.SUMMARY_HTML_TOKEN if open_ai_api_config.SUMMARY_HTML_TOKEN else None,
        'http_error': open_ai_api_config.HTTP_ERROR if open_ai_api_config.HTTP_ERROR else None,
        'is_more_than_threshold': open_ai_api_config.IS_MORE_THAN_THRESHOLD if open_ai_api_config.IS_MORE_THAN_THRESHOLD else None,
        'token_exceed': open_ai_api_config.TOKEN_EXCEED if open_ai_api_config.TOKEN_EXCEED else None,
        'pages_links_tokens': json.dumps(open_ai_api_config.PAGE_LINK_TOKEN) if open_ai_api_config.PAGE_LINK_TOKEN else None,
        'not_inserted_flag': open_ai_api_config.NOT_INSERTED_FLAG if open_ai_api_config.NOT_INSERTED_FLAG else None,
        'website_scrape_done_flag': open_ai_api_config.WEBSITE_SCRAPE_DONE_FLAG if open_ai_api_config.WEBSITE_SCRAPE_DONE_FLAG else None,
        'run_time': open_ai_api_config.RUN_TIME if open_ai_api_config.RUN_TIME else None
    }
    commit_mysql_query_executer(query, values, "insert log")


def update_flag_for_not_inserted():
    query = f"""
        UPDATE {open_ai_api_config.GL_SCRAPE_TABLENAME}
        SET not_inserted_flag = %s
        WHERE gl_website = %s;
    """
    values = (1, open_ai_api_config.WEBSITE_URL)
    commit_mysql_query_executer(query, values, "insert not_inserted_flag")


def update_flag_for_token_error():
    query = f"""
        UPDATE {open_ai_api_config.GL_SCRAPE_TABLENAME}
        SET token_exceed_flag = %s
        WHERE gl_website = %s;
    """
    values = (1,open_ai_api_config.WEBSITE_URL)
    commit_mysql_query_executer(query, values, "insert error token")


def update_flag_for_http_error():
    query = f"""
        UPDATE {open_ai_api_config.GL_SCRAPE_TABLENAME}
        SET http_error_code = %s
        WHERE gl_website = %s;
    """
    values = (1,open_ai_api_config.WEBSITE_URL)
    commit_mysql_query_executer(query, values, "insert error code")


def update_flag_for_more_than_threshold():
    query = f"""
        UPDATE {open_ai_api_config.GL_SCRAPE_TABLENAME}
        SET number_of_pages = %s, is_more_than_threshold = %s
        WHERE gl_website = %s;
    """
    values = (open_ai_api_config.NUM_PAGES, 1, open_ai_api_config.WEBSITE_URL)
    commit_mysql_query_executer(query, values, f"more than {open_ai_api_config.MAXIMUM_LINKS_NUMBER}")


def update_data(data):

    # # Function to handle missing values gracefully
    # def safe_get_website(key, default=None):
    #     value = data.get(key, default)
    #     return url if value == "Null" else value  # Convert "Null" strings to None

    # Function to handle missing values gracefully
    def safe_get(key, default=None):
        value = data.get(key, default)
        return None if value == "Null" else value  # Convert "Null" strings to None

    # Function to convert lists to comma-separated strings
    def list_to_string(key):
        value = safe_get(key)
        if isinstance(value, list):
            return ', '.join(str(v) for v in value)  # Convert all items to strings before joining
        return value

    # Function to remove backslashes from strings
    def remove_backslashes(value):
        if isinstance(value, str):
            return value.replace("\\", "")  # Remove all backslashes from the string
        return value

    values = (
        safe_get("Title"),
        safe_get("First Name"),
        safe_get("Middle Name"), 
        safe_get("Last Name"),  
        list_to_string("Specialty"), 
        safe_get("Contact Number"), 
        safe_get("Email ID"),
        list_to_string("Profile Image"), 
        safe_get("Map"), 
        safe_get("NPI Number"),
        safe_get("Gender"), 
        safe_get("Experience"), 
        safe_get("Age/DOB"), 
        safe_get("Therapist Race or Ethnicity"), 
        safe_get("About Me"), 
        list_to_string("Board Certification"), 
        list_to_string("Education and Training"), 
        list_to_string("Awards"), 
        safe_get("Credentials Attended"), 
        list_to_string("Languages Spoken"), 
        safe_get("Business Logo"), 
        safe_get("Years Established"), 
        list_to_string("Primary Practitioner Type"), 
        list_to_string("Other Practitioner Types"), 
        safe_get("Tagline"), 
        list_to_string("Tags"), 
        safe_get("Postcode/ZIP"), 
        safe_get("Country"), 
        safe_get("State"),
        safe_get("State code"), 
        safe_get("City"), 
        safe_get("Address"), 
        list_to_string("Practitioner"), 
        list_to_string("Conditions Treated"), 
        list_to_string("Modalities"), 
        safe_get("Amenities"), 
        list_to_string("Cost of Sessions"), 
        list_to_string("Payment Accepted"), 
        safe_get("Types (Online - Offline, Phone, Telehealth)"), 
        safe_get("Treatment Orientations", ""),
        list_to_string("Insurance"), 
        remove_backslashes(list_to_string("Media JSON")), 
        safe_get("Facebook URL"), 
        safe_get("Instagram URL"), 
        safe_get("Yelp URL"), 
        safe_get("Twitter URL"), 
        safe_get("YouTube URL"), 
        safe_get("Trustpilot URL"), 
        safe_get("LinkedIn URL"), 
        safe_get("Google Business Profile URL"), 
        safe_get("Google Review Count"), 
        safe_get("Yelp Review Count"), 
        safe_get("Trustpilot Review Count"), 
        safe_get("Facebook Rating"), 
        safe_get("Google Rating"), 
        safe_get("Yelp Rating"), 
        safe_get("Trustpilot Rating"), 
        remove_backslashes(list_to_string("FAQ")), 
        remove_backslashes(list_to_string("Working Hours")),
        open_ai_api_config.NUM_PAGES,
        1,
        open_ai_api_config.WEBSITE_URL
    )

    # 🛠️ Debugging Step: Print values before inserting
    print("🛠️ DEBUG: Data being inserted:", values)

    # ✅ Execute the query safely
    try:
        commit_mysql_query_executer(open_ai_api_config.GL_UPDATE_QUERY, values, "update_output_data")
    except Exception as e:
        print(f"❌ Error inserting data: {e}")
