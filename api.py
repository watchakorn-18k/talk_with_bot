import requests
from dotenv import load_dotenv

load_dotenv()
import os

api = os.environ.get("API_URL")
response = requests.post(api + "generate", json={"text": "สวัสดีจ้า"})
response = requests.get(api + "generate-text")
print(response.json())
