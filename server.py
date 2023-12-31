from flask import Flask, request, jsonify
from flask_cors import CORS
# send a get request to /
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)
load_dotenv()

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api', methods = ['POST', 'GET'])
def api():
    def scrape_website(url):
    
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
            print(cleaned_text)
        else:
            return "3/5"

    # Example usage:
    
    from apify_client import ApifyClient
    client = ApifyClient(token='API_KEY')

    from test2 import summarize
    from scraper import scraper

    url = request.json['url1']

    run_input = {
        "queries": summarize(scraper(url)),
        "maxPagesPerQuery": 1,
        
    }

    # Run the Actor and wait for it to finish
    # .call method waits infinitely long using smart polling
    # Get back the run API object
    run = client.actor("apify/google-search-scraper").call(run_input=run_input)
    website_url2 = ""
    # Fetch and print Actor results from the run's dataset (if there are any)
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        print(item['organicResults'][5]['url'])
        website_url2 = item['organicResults'][5]['url']
    
    # this should work try running the server
    website_url1 = request.json['url1']
    print(website_url1)
    print(website_url2)
    
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    body1 = scrape_website(website_url1)
    body2 = scrape_website(website_url2)
    
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are an AI CRAAP tester assistant for research projects."},
        {"role": "user", "content": f"Website body 1: {body1} \n Website body 2: {body2} \n compare the content and give me a score of 1-5 on how similar the content is to provide a CRAAP score accuracy. MAKE SURE THAT YOU ONLY GIVE ME A RATING OF 1-5 WITH NOTHING ELSE IN THE TEXT. For example: 1/5. Not: this is the summary of the website. The website is 1/5. The first website is the og website and the second one is what you are comparing to. ONLY RETURN A NUMBER / Something over 5. THIS IMPORTANT. eg. 2/5 or eg. 3/5"}
    ]
    )

    print(completion.choices[0].message.content)
    return jsonify(completion.choices[0].message.content)
    
if __name__ == '__main__':
    app.run()

# send it to /api