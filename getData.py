import requests

Url = "http://127.0.0.1:5000/get_data/"

criteria = {"user": "",  # Specific User
            "search_term": "",  # Word or Phrase that is being searched for
            "until": "",  # End date
            "since": "",  # Start Date
            "count": 1}  # Number of tweets requested

r = requests.post(url=Url, json=criteria)

print(r.json()["data"])