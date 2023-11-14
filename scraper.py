import requests
from bs4 import BeautifulSoup


def scraper(url):
    
    # Make a GET request to the website
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract all the text from the page
        all_text = soup.get_text()

        # Remove newline characters from the text
        all_text_without_newlines = all_text.replace('\n', '')

        # Remove extra spaces and ensure only one space between words
        cleaned_text = ' '.join(all_text_without_newlines.split())

        # Print or do something with the cleaned text
        return cleaned_text
    else:
        print(f"Error: Unable to fetch the website. Status code: {response.status_code}")

