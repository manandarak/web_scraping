import requests
from bs4 import BeautifulSoup
import mysql.connector
import logging
from mysql.connector import errorcode

# Function to scrape website
def scrape_website(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        else:
            logging.error(f"Failed to fetch content from {url}. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching content from {url}: {str(e)}")
        return None

# Function to extract data
def extract_data(content):
    if content:
        soup = BeautifulSoup(content, 'html.parser')
        # Example: extracting title
        title = soup.find('title').text.strip()
        return title
    else:
        return None

# Function to save data to MySQL database
def save_to_database(data):
    try:
        cnx = mysql.connector.connect(user='root', password='Manan35635@',
                                      host='localhost', database='web_scraping')
        cursor = cnx.cursor()

        # Create table if not exists
        create_table_query = """
            CREATE TABLE IF NOT EXISTS scraped_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255)
            )
        """
        cursor.execute(create_table_query)

        # Insert data into the table
        insert_query = "INSERT INTO scraped_data (title) VALUES (%s)"
        data_values = (data,)
        cursor.execute(insert_query, data_values)

        cnx.commit()
        cursor.close()
        cnx.close()
        logging.info("Data saved to MySQL database successfully.")
        print("Task completed successfully!")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            logging.error("Access denied error. Check username or password.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            logging.error("Database does not exist.")
        else:
            logging.error("Error saving data to MySQL database: {}".format(err))

# Main function
def main():
    logging.basicConfig(filename='scraping.log', level=logging.ERROR)
    urls = ["https://www.scrapethissite.com/pages/ajax-javascript/#2015",
            "https://www.scrapethissite.com/pages/forms/",
            "https://www.scrapethissite.com/pages/advanced/"]

    for url in urls:
        content = scrape_website(url)
        if content:
            data = extract_data(content)
            if data:
                save_to_database(data)
            else:
                logging.error(f"No data extracted from {url}")
        else:
            logging.error(f"No content fetched from {url}")

if __name__ == "__main__":
    main()
