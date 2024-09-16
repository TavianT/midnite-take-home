# midnite-take-home
Take home technical exercise for Midnite

## how to run server

 - Ensure Python 3.10+ is installed
 - (Optional) create venv
 - execute the line `pip install -r requirements.txt`
 - execute the line `fastapi dev src/main.py` from the top level of the repo
 - Use the URI `http://127.0.0.1:8000/event` to send requests

## Challenges and considerations
During development, I had a few things to consider. One thing was how to store data. The simplest method would’ve been to use a JSON file for storage to keep the scope small or I could’ve used a NoSQL database like MongoDB however I chose a SQL database (SQLite) due to it being easy to use, easy to keep in scope and the ease of querying data for checking alert codes. Another consideration I had was during the development of the logic for alert code 123, I wasn’t sure if the alert should calculate for all deposits within 30 seconds of the given timestamp or for just when the request contained a deposit. I went with the latter as that made the most sense with the other information provided. A challenge I had was keeping within the scope, I mostly stayed within scope however I did add some request validation. A change I would make when doing this again is changing the response of the alert code checking functions from tuples to dicts to improve readability.
