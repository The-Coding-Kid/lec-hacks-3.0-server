from apify_client import ApifyClient
client = ApifyClient(token='apify_api_jCU3xbbBbEjAIGe4Kbmmmt1eZgC0kZ2RAmAi')

run_input = {
    "queries": "Best brawlers brawl stars",
    "maxPagesPerQuery": 1,
    
}

# Run the Actor and wait for it to finish
# .call method waits infinitely long using smart polling
# Get back the run API object
run = client.actor("apify/google-search-scraper").call(run_input=run_input)

# Fetch and print Actor results from the run's dataset (if there are any)
ctr = 0
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item['organicResults'][0]['url'])
