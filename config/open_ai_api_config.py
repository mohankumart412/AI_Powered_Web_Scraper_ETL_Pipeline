import os
import mysql.connector


# Define the base directory for saving HTML files
BASE_DIR1 = os.path.join(os.getcwd(), "data/html_files_in_batch_format")
os.makedirs(BASE_DIR1, exist_ok=True)


# Define the base directory for saving HTML files
BASE_DIR2 = os.path.join(os.getcwd(), "data/summerized_html_files")
os.makedirs(BASE_DIR1, exist_ok=True)


# chat gpt-4o-mini api
# os.environ["OPENAI_API_KEY"] = "***"

# google gemini-1.5-flash api
os.environ["GOOGLE_API_KEY"] = "***"

# AWS Configuration for deepseek R1 Model
# REGION_NAME = '***'
# AWS_ACCESS_KEY_ID = '***'   # Replace with actual AWS access key
# AWS_SECRET_ACCESS_KEY = '***'  # Replace with actual AWS secret key
# MODEL_ID = '***'  # Use a valid Amazon Bedrock model ID

# api key for together ai
# API_KEY = "***"

# def Database_Connection():
 
#     db_connection = mysql.connector.connect(
        
#         host = '***',
#         user = '***',
#         password ='***',
#         database = '***',
#         # auth_plugin='***'
#     )
 
#     db_cursor = db_connection.cursor()
 
#     return db_connection,db_cursor


MAIN_PROMPT = """Objective : 
I am providing an HTML file containing the source code of multiple pages from a website. Parse the required information related to the doctor, business, and services from the HTML elements, attributes, and meta tags. The extracted data should be structured in a format that is easily convertible into a Pandas DataFrame, with two columns:
Parameter Name
Parsed Data from the HTML file
Use the most relevant HTML tags, classes, IDs, or structured data (such as JSON-LD or microdata) to retrieve accurate information. If data is not explicitly available, return "Null" instead of leaving it blank.

Parsing Instructions & Required Data Fields
1. Personal Details
Profile Image: Parse the doctor's profile image URL, check it is doctor profile image or not, if it is not doctor's image mention as NUll and don't take logo url, banner url.
Title: Parse the doctor’s title (e.g., Dr., Prof.) from relevant heading tags (h1-h6), strong tags, or structured data by default mention (Dr).
First Name: Parse the first name from structured data, labels, or text content.
Middle Name: Parse the middle name from structured data, labels, or text content.
Last Name: Parse the last name from structured data, labels, or text content.
Email ID: Parse the email address , if it is not put Null.
Contact Number: Parse the phone number from tel: links, structured data, or visible text.
Website: Parse the doctor’s website URL from anchor tags <a> or metadata.
Gender: Parse gender if explicitly mentioned in structured data or text.
Age/DOB: Parse date of birth or age if available.
NPI Number: Parse National Provider Identifier (NPI) number if mentioned.
Address: Parse the full clinic/practice address, including street, city, state, ZIP code.
About Me: Parse the doctor’s bio or professional background from the “About Me” section.
Therapist Race or Ethnicity: Parse if mentioned explicitly.

2. Media Parameters
Banner Images: Parse banner image URLs or file names.
Carousel Images: Parse carousel images URLs.
Gallery Images: Parse gallery images and their URLs.
Videos: Parse video URLs, embedded video codes (YouTube, Vimeo, etc.), or file names.
Media JSON: Combine all media-related fields (Banner Images, Carousel Images, Gallery Images, and Videos) into a single JSON object and with in double quotes, don't use backward slash "\" in the json and return it under "Media JSON" as follows:
    json
    CopyEdit Example like below

    "[{"video": [{"id": 300, "url": "https://holistictherapisthub-project.s3.amazonaws.com/visualmedia/user_77/videos/67ada4ea6ce35.mp4",
        "name": "6296290-hd_1080_1920_25fps.mp4", "size": 12693666, "type": "video/mp4", "stored_path": "visualmedia/user_77/videos/67ada4ea6ce35.mp4"}], 
        "banner_image": [{"id": 1, "url": "https://holistictherapisthub-project.s3.amazonaws.com/visualmedia/user_77/banner_images/67ada4e61ed7d.png", "name": "_64.png", "size": 683, "type": "image/png", "stored_path": "visualmedia/user_77/banner_images/67ada4e61ed7d.png"}, 
        {"id": 2, "url": "https://holistictherapisthub-project.s3.amazonaws.com/visualmedia/user_77/banner_images/67ada4e7e43fd.png", "name": "InactiveProfile.png", "size": 426, "type": "image/png", "stored_path": "visualmedia/user_77/banner_images/67ada4e7e43fd.png"}], 
        "gallery_images": [{"id": 200, "url": "https://holistictherapisthub-project.s3.amazonaws.com/visualmedia/user_77/gallery_images/67ada4e8ba502.png", "name": "user-profile-icon-vector-avatar-600nw-2247726673.png", "size": 5214, "type": "image/webp", "stored_path": "visualmedia/user_77/gallery_images/67ada4e8ba502.png"}, {"id": 201, "url": "https://holistictherapisthub-project.s3.amazonaws.com/visualmedia/user_77/gallery_images/67ada4e90f621.png", "name": "screencapture-sub-holistictherapytribe-user-profile-2025-01-24-12_39_33 (1).png", "size": 536634, "type": "image/png", "stored_path": "visualmedia/user_77/gallery_images/67ada4e90f621.png"}], 
        "carousel_images": [{"id": 100, "url": "https://holistictherapisthub-project.s3.amazonaws.com/visualmedia/user_77/carousel_images/67ada4e8362be.png", 
        "name": "Facebook.png", "size": 1925, "type": "image/png", "stored_path": "visualmedia/user_77/carousel_images/67ada4e8362be.png"}, {"id": 101, "url": "https://holistictherapisthub-project.s3.amazonaws.com/visualmedia/user_77/carousel_images/67ada4e879525.png", "name": "Google.png", "size": 2225, "type": "image/png", "stored_path": "visualmedia/user_77/carousel_images/67ada4e879525.png"}]}
    ]"



3. Professional Details
Specialty: Parse the doctor’s medical specialty from structured data or headings.
Board Certification: Parse board certification details.
Education and Training: Parse the doctor’s education, degrees, and training details.
Awards: Parse any awards received.
Credentials Attended: Parse certifications or credentials associated with the doctor.
Languages Spoken: Parse languages the doctor speaks; if not found, default to "English".
How Did You Hear About Us: Parse how the patient heard about the doctor.
Experience: Parse the doctor’s experience, if there is no experience put Null.

4. Business Information
Business Logo: Parse the business logo URL or file name.
Business Name: Parse the name of the business or practice.
Years Established: Parse how many years the business has been active, if it is not found mention as a Null.
Primary Practitioner Type: Parse the primary type of practitioner (e.g., Psychologist, Chiropractor, etc.).
Other Practitioner Types: Parse other specialties (if applicable).
Tagline: Parse the business/doctor's tagline.
Tags: Parse SEO or category tags related to the business/doctor.

5. Service Details
Practitioner: Parse name of the practitioner.
Conditions Treated: Parse health conditions treated.
Modalities: Parse treatment techniques/modalities used.
Amenities: Parse available amenities at the practice.
Cost of Sessions: Parse the pricing details of sessions.
Payment Accepted: Parse the accepted payment methods.
Types (Online - Offline, Phone, Telehealth): Parse whether the service is provided (online, offline, via phone, or telehealth), don't take in dictionary type format.
Treatment Orientations: Parse the therapeutic approaches followed.
Insurance: Parse the insurance providers accepted.

6. Location & Contact Information
Postcode/ZIP: Parse the ZIP code/postal code.
Country: Parse the country, give me full country name.
State: Parse the state, give me full state name.
State code: Parse the state code.
City: Parse the city, give me full city name.
Address: Parse the full address.
Working Hours: Working Hours JSON Format (Structured) and with in double quotes "", don't use backward slash
    If available, parse clinic/office working hours in the following JSON format:
    json
    CopyEdit
    "[
        {"id": 1, "day": "Monday", "opening_time": "9:00", "closing_time": "5:00", "opening_am_pm": "AM", "closing_am_pm": "PM"},
        {"id": 2, "day": "Tuesday", "opening_time": "9:00", "closing_time": "5:00", "opening_am_pm": "AM", "closing_am_pm": "PM"},
        {"id": 3, "day": "Wednesday", "opening_time": "Null", "closing_time": "Null", "opening_am_pm": "PM", "closing_am_pm": "AM"},
        {"id": 4, "day": "Thursday", "opening_time": "Null", "closing_time": "Null", "opening_am_pm": "PM", "closing_am_pm": "AM"},
        {"id": 5, "day": "Friday", "opening_time": "Null", "closing_time": "Null", "opening_am_pm": "PM", "closing_am_pm": "AM"},
        {"id": 6, "day": "Saturday", "opening_time": "Null", "closing_time": "Null", "opening_am_pm": "PM", "closing_am_pm": "AM"},
        {"id": 7, "day": "Sunday", "opening_time": "Null", "closing_time": "Null", "opening_am_pm": "PM", "closing_am_pm": "AM"}
    ]"
Map: Parse Google Maps embedded link or location coordinates.
FAQ: FAQ JSON Format (Structured) with double quotes "", don't use backward slash
    If available, parse FAQ in the following JSON format:
    json
    CopyEdit
    
    "[
        {"indexId": 0, "answerId": "1", "questionId": "1"},
        {"indexId": 1, "answerId": "3", "questionId": "2"},
        {"indexId": 2, "answerId": "5", "questionId": "3"}
    ]"



7. Social Media & Reviews
Facebook URL: Parse the Facebook profile/page URL.
Instagram URL: Parse the Instagram profile URL.
Yelp URL: Parse the Yelp business URL.
Twitter URL: Parse the Twitter (X) profile URL.
YouTube URL: Parse the YouTube channel URL.
Trustpilot URL: Parse the Trustpilot profile URL.
LinkedIn URL: Parse the LinkedIn profile/business page URL.
Google Business Profile URL: Parse the Google Business Profile URL.
Google Review Count: Parse the total number of Google reviews.
Facebook Rating: Parse the Facebook rating.
Google Rating: Parse the Google rating.
Yelp Rating: Parse the Yelp rating.
Yelp Review Count: Parse the total number of Yelp reviews.
Trustpilot Rating: Parse the Trustpilot rating.
Trustpilot Review Count: Parse the total number of Trustpilot reviews.

Output Format

The parsed data should be in key and value pairs,  parameter as key and that respective value as value and
don't give me python code give me extracted data and don't include any unwanted text like(import, print, create dataframe,
 variable, any words, space, json, html, python, commas, python code(if, else, condition, etx..) and unwanted text) 
in output response should be only in dictionary format and don't give a python code.:
"""

SUMMARY_PROMPT = """
Extract the essential hyper text markup language (html)) content from the provided hyper text markup language (html)) content, 
ensuring the total length does not exceed 30,000 characters. 
Only include the necessary hyper text markup language (html)) elements (such as headings, paragraphs, links, images, and other key sections). 
Exclude any non-essential or redundant content like excessive comments, scripts, and unnecessary metadata. 
The output should focus on the core content relevant to the page while staying within the character limit of 30,000.
and don't include any unwanted text only output should in hyper text markup language (html)) format.
"""


def Gl_Database_Connection():
 
    db_connection = mysql.connector.connect(
        
        host = '***',
        user = '***',
        password ='***',
        database = '***',
        # auth_plugin='***'
    )

    # db_connection = mysql.connector.connect(
        
    #     host = '***',
    #     user = '***',
    #     password ='***@1234',
    #     database = '***',
    #     # auth_plugin='***'
    # )
 
    db_cursor = db_connection.cursor()
 
    return db_connection,db_cursor
 


MAXIMUM_LINKS_NUMBER = 25

CHARACTER_LIMIT = 300000

TOKEN_LIMIT = 90000



WEBSITE_URL = ""
NUM_PAGES = 0
PARAMETER_COUNT = 0
SUMMARY_HTML_TOKEN = 0
HTTP_ERROR = 0
IS_MORE_THAN_THRESHOLD = 0
TOKEN_EXCEED = 0
PAGE_LINK_TOKEN = None
NOT_INSERTED_FLAG = 0
WEBSITE_SCRAPE_DONE_FLAG = 0
RUN_TIME = 0

LOG_TABLE_NAME = "usa_chiropractor_business_data_log"


GL_SCRAPE_TABLENAME = "usa_chiropractor_business_data"

CITY = '"Philadelphia", "Austin", "Portland", "New York"'

GL_SELECT_QUERY = f"""SELECT DISTINCT gl_website FROM {GL_SCRAPE_TABLENAME} WHERE city IN  ({CITY}) AND custom_website_flag = 1 AND http_error_code IS null AND is_more_than_threshold IS null AND token_exceed_flag IS null AND not_inserted_flag IS null AND website_scrape_done_flag IS null;"""

GL_UPDATE_QUERY = f"""UPDATE {GL_SCRAPE_TABLENAME}
                    SET 
                        w_title = %s,
                        first_name = %s,
                        middle_name = %s,
                        last_name = %s,
                        practice_speciality = %s,
                        w_phone_number = %s,
                        w_email = %s,
                        profile_pic = %s,
                        map = %s,
                        npi_number = %s,
                        gender = %s,
                        experience = %s,
                        age = %s,
                        race_ethnicity = %s,
                        professional_summary = %s,
                        board_certifications = %s,
                        education_training = %s,
                        awards = %s,
                        credentials_attended = %s,
                        languages_spoken = %s,
                        business_logo = %s,
                        year_established = %s,
                        primary_practitioner_type = %s,
                        other_practitioner_types = %s,
                        tag_line = %s,
                        tags = %s,
                        postcode = %s,
                        w_country = %s,
                        w_state = %s,
                        w_state_code = %s,
                        w_city = %s,
                        w_address = %s,
                        practitioner = %s,
                        conditions_treated = %s,
                        modalities = %s,
                        amenities = %s,
                        cost_sessions = %s,
                        payment_accepted = %s,
                        types = %s,
                        treatement_orientation = %s,
                        insurance = %s,
                        mediaJson = %s,
                        facebook_url = %s,
                        instagram_url = %s,
                        yelp_url = %s,
                        twitter_url = %s,
                        youtube_url = %s,
                        trustpilot_url = %s,
                        linkedin_url = %s,
                        w_google_url = %s,
                        google_review_count = %s,
                        yelp_review_count = %s,
                        trustpilot_review_count = %s,
                        facebook_rating = %s,
                        google_rating = %s,
                        yelp_rating = %s,
                        trustpilot_rating = %s,
                        faq = %s,
                        working_hours = %s,
                        number_of_pages = %s,
                        website_scrape_done_flag = %s
                    WHERE gl_website = %s;
                    """
