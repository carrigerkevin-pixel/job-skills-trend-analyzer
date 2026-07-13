import os
import requests
from dotenv import load_dotenv

# Load the .env file so we can access our API keys
load_dotenv()

app_id = os.getenv("ADZUNA_APP_ID")
app_key = os.getenv("ADZUNA_APP_KEY")

# Basic test: search for "software engineer" jobs in the US
url = "https://api.adzuna.com/v1/api/jobs/us/search/1"
params = {
    "app_id": app_id,
    "app_key": app_key,
    "results_per_page": 5,
    "what": "software engineer"
}

response = requests.get(url, params=params)

print("Status code:", response.status_code)

if response.status_code == 200:
    data = response.json()
    print(f"Found {data['count']} total jobs")
    for job in data["results"]:
        print("-", job["title"], "at", job["company"]["display_name"])
else:
    print("Error:", response.text)