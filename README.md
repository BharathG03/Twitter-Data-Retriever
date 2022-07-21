# Twitter-data-Retriever
An API that returns a user specified number of tweets based on criteria such as account, word/phrase, and time-period without any limitations on the number of tweets or timeframe of when a tweet was issued.

# app.py
Creates a Flask API that provides users with a easy way to outline the search criteria and the number of tweets they want to retrieve. The API returns a JSON object with the tweets.

# getData.py
Sends a POST request to the Flask API and recives the JSON Data that is returned. The JSON Data can then be parsed into a more readable format.