# 🤖🧠 AI-Powered Web Scraping & Data Extraction Pipeline

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![AI](https://img.shields.io/badge/AI-Gemini%20|%20GPT%20|%20Llama%20|%20DeepSeek-successgreen)](https://ai.google/discover/gemini/)
[![Database](https://img.shields.io/badge/Database-MySQL-orange)](https://www.mysql.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](https://opensource.org/licenses/MIT)

A high-performance, modular web scraping pipeline designed to extract structured data from millions of websites. It leverages large language models (LLMs) to intelligently parse and summarize complex HTML content, transforming it into clean, structured data ready for database insertion.

## 📖 Detailed Project Description

This project is a comprehensive AI-powered web scraping and ETL (Extract, Transform, Load) pipeline, designed to automate large-scale data collection, transformation, and storage from websites.

In today’s world, businesses and researchers need structured insights from unstructured web content. Traditional scraping tools are effective for small-scale projects, but they fail when:
- The volume is extremely large (millions of websites).
- The parameters are diverse (dozens of attributes per website).
- The content is unstructured (HTML, mixed text, noisy data).
- There is a need for automation + AI understanding.

This project solves that challenge by combining classical scraping techniques with AI models (Gemini API, DeepSeek, Together AI) to extract 60+ structured parameters from more than 6 million websites.

## 🚀 Features

*   **Multi-LLM Support**: Integrates with various AI providers for robustness and flexibility (Google Gemini, OpenAI GPT, Together AI, AWS Bedrock/DeepSeek).
*   **Intelligent Parsing**: Uses advanced LLM prompts to accurately extract over 60 structured data points from raw HTML.
*   **Scalable Architecture**: Handles large-scale scraping jobs by processing HTML in batched files based on token and character limits.
*   **Database Integration**: Automatically inserts cleaned and structured data into a MySQL database with comprehensive logging and error handling.
*   **Resilient Design**: Built-in error handling for HTTP requests, token limits, and database connectivity.

## 🔍 Key Highlights

- **Massive Scale** – Built to scrape and analyze lakhs (millions) of websites efficiently.
- **AI-Driven Parsing** – Unlike traditional scrapers that rely on fixed HTML rules, this project uses LLMs to read, understand, and extract semantic insights.
- **Extensible Design** – Each major function is modularized under `/functions`, making it easy to upgrade or replace parts.
- **End-to-End Pipeline** – Covers the full ETL flow: Extract, Transform, and Load.
- **Error-Resilient** – Handles broken links, timeouts, invalid responses, and API failures gracefully.

## 🧠 Core Extraction Logic

The intelligence of this pipeline is driven by a meticulously engineered **system prompt** located in `config/open_ai_api_config.py`. This prompt acts as the instruction manual for the LLM, precisely guiding it on what to find, where to look, and how to format the output.

The `MAIN_PROMPT` is designed to:
*   **Instruct the Model:** It clearly defines the objective: to parse HTML and extract specific information related to healthcare practitioners and businesses.
*   **Handle Ambiguity:** It provides explicit rules for dealing with missing data (return "Null"), ensuring consistent output structure.
*   **Enforce Formatting:** It demands a clean, JSON-like dictionary output without any extraneous text, code, or explanations, making it ready for database insertion.
*   **Leverage Semantics:** Instead of relying on brittle HTML selectors, the prompt instructs the AI to understand the *meaning* of the content, making the scraper resilient to website design changes.

The prompt is structured to extract information across **seven key categories**:

1.  **Personal & Professional Details:** Names, titles, contact information, credentials, and biographies.
2.  **Business Information:** Practice names, logos, years established, and operational tags.
3.  **Service Details:** Treatment specialities, modalities, accepted insurance, and session costs.
4.  **Location Data:** Full addresses, coordinates, and structured working hours.
5.  **Media Assets:** URLs for profile images, banners, galleries, and videos, formatted into a clean JSON object.
6.  **Social Proof:** Links to social profiles, review site URLs, and aggregate ratings & counts.
7.  **Structured Content:** FAQ and working hours information extracted into structured JSON formats.

This prompt-based approach is what transforms a simple web scraper into a powerful AI-powered data extraction engine.

## 📋 Extracted Data Points

The pipeline is configured to extract a comprehensive set of parameters, including:

*   **Personal Details:** Name, Title, Contact Info, NPI Number, Profile Image, Bio.
*   **Professional Details:** Specialty, Education, Certifications, Experience, Languages.
*   **Business Information:** Business Name, Logo, Years Established, Tags, Tagline.
*   **Service Details:** Conditions Treated, Treatment Modalities, Insurance Accepted, Pricing.
*   **Location & Media:** Full Address, Working Hours, FAQ, Gallery Images, Videos, Social Media Links.
*   **Reviews & Ratings:** Ratings and review counts from Google, Yelp, Facebook, and Trustpilot.

## 🏗️ Project Structure

    AI_Powered_Web_Scraper_ETL_Pipeline
    ├── main.py # Main script orchestrating the pipeline
    ├── config/
    │ └── open_ai_api_config.py # Configuration & prompts (API keys, DB credentials)
    └── functions/ # Core modular functions
    ├── extract_internal_links.py # Discovers all internal links from a base URL
    ├── get_html_content.py # Fetches & cleans HTML, batches content for processing
    ├── get_data_by_gemini_ai_api.py # Data extraction module using Google Gemini
    ├── get_data_by_open_ai_api.py # Data extraction module using OpenAI API
    ├── get_data_by_together_ai.py # Data extraction module using Together AI
    ├── get_data_by_deepseek_r1_model.py # Data extraction module using AWS Bedrock
    ├── save_summerized_html_content.py # Summarizes HTML content to reduce token usage
    └── insert_into_db.py # Handles all database operations (inserts, updates, logs)


## ⚙️ Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/mohankumart412/AI_Powered_Web_Scraper_ETL_Pipeline.git
    cd AI_Powered_Web_Scraper_ETL_Pipeline
    ```

2.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *`requirements.txt`:*
    ```txt
    beautifulsoup4==4.12.2
    requests==2.31.0
    openai==1.3.0
    google-generativeai==0.3.0
    together==0.2.10
    boto3==1.28.62
    mysql-connector-python==8.1.0
    ```

3.  **Configuration:**
    *   Edit `config/open_ai_api_config.py` to set your API keys and database connection parameters.
    *   **Important:** Securely manage your secrets using environment variables or a secrets manager before deploying.

4.  **Database Setup:**
    *   Ensure your MySQL database and table schema match the structure defined in `insert_into_db.py` and the config file.

## 🚦 Usage

1.  **Add target website URLs** to your database table specified in `GL_SCRAPE_TABLENAME`.
2.  Run the main script:
    ```bash
    python main.py
    ```
3.  The pipeline will:
    *   Fetch a website URL from the DB.
    *   Scrape the main page and discover internal links.
    *   Download and clean HTML content from all pages.
    *   Use the configured LLM (default: Gemini) to analyze the HTML and extract structured data.
    *   Insert the resulting data into the database and log the process.

## 🔧 Configuration

Key settings in `config/open_ai_api_config.py`:

*   `API KEYS`: Set for Gemini, OpenAI, Together, AWS.
*   `MAIN_PROMPT`: The detailed instruction prompt for the LLM to extract data.
*   `SUMMARY_PROMPT`: The instruction for summarizing HTML to save tokens.
*   `DATABASE CONNECTION`: Host, user, password, and database name.
*   `TOKEN_LIMIT`, `CHARACTER_LIMIT`: Control how HTML is batched for processing.
*   `TABLE NAMES`: Configure the source and destination tables.

## 📈 Logging

The pipeline logs extensive metadata for each scrape job, including:
*   Number of pages processed
*   Token counts per page
*   Number of parameters successfully extracted
*   Error flags (HTTP errors, token exceedance, insertion failures)
*   Total run time

## 🏗️ Real-World Applications

- **Business Intelligence:** Automatically track competitor websites and extract product, service, or compliance details.
- **SEO & Digital Marketing:** Monitor millions of pages for keywords, metadata, backlinks, and on-page content.
- **Data Engineering:** Serve as a data ingestion pipeline for ML/AI projects.
- **Research:** Collect web data for academic, policy, or trend analysis.

## ⚡ Why It’s Unique

Unlike most scraping projects that stop at extracting raw HTML, this pipeline goes further:
- Uses AI to summarize and clean raw content.
- Extracts rich parameters (60+), not just page titles or links.
- Scales across millions of websites with efficiency.
- Stores results in a queryable database, enabling dashboards, analytics, or integration with BI tools.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/mohankumart412/AI_Powered_Web_Scraper_ETL_Pipeline/issues).

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is intended for ethical web scraping purposes. Always:
*   Check a website's `robots.txt` file and `Terms of Service` before scraping.
*   Respect `rate limits` and implement delays to avoid overwhelming servers.
*   Use scraped data responsibly and in accordance with relevant data protection laws (like GDPR, CCPA).
*   
