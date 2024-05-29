import requests
import mysql.connector
from bs4 import BeautifulSoup

# Function to spoof headers
def spoof_headers():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    return headers

# Function to handle logins & session data
def handle_login_session():
    session = requests.Session()
    login_url = 'https://example.com/login'
    payload = {'username': 'your_username', 'password': 'your_password'}
    session.post(login_url, data=payload)
    return session

# Function to handle CSRF & hidden values
def handle_csrf_hidden_values(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrf_token'}).get('value')
    hidden_values = {}
    hidden_inputs = soup.find_all('input', type='hidden')
    for input_tag in hidden_inputs:
        hidden_values[input_tag.get('name')] = input_tag.get('value')
    return csrf_token, hidden_values

# Function to scrape and store hockey team stats
def scrape_hockey_stats():
    url = 'https://www.scrapethissite.com/pages/advanced/'
    headers = spoof_headers()
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    data = soup.find_all('tr')[1:]  # Skip header row
    for row in data:
        columns = row.find_all('td')
        team_name = columns[0].text.strip()
        year = int(columns[1].text.strip())
        wins = int(columns[2].text.strip())
        losses = int(columns[3].text.strip())
        ot_losses = int(columns[4].text.strip())
        win_percentage = float(columns[5].text.strip())
        goals_for = int(columns[6].text.strip())
        goals_against = int(columns[7].text.strip())
        plus_minus = int(columns[8].text.strip())
        cursor.execute("INSERT INTO HockeyTeamStats VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                       (team_name, year, wins, losses, ot_losses, win_percentage, goals_for, goals_against, plus_minus))
    conn.commit()

# Function to scrape and store movie awards data
def scrape_movie_awards():
    url = 'https://www.scrapethissite.com/pages/ajax-javascript/#2015'
    headers = spoof_headers()
    response = requests.get(url, headers=headers)
    data = response.json()
    for movie in data:
        cursor.execute("INSERT INTO MovieAwards VALUES (%s, %s, %s, %s)",
                       (movie['Title'], movie['Nominations'], movie['Awards'], movie['Best Picture']))
    conn.commit()

# Establish connection to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Manan35635@",
    database="assignment"
)
cursor = conn.cursor()

# Scrape and store hockey team stats
scrape_hockey_stats()

# Scrape and store movie awards data
scrape_movie_awards()

# Close cursor and connection
cursor.close()
conn.close()
