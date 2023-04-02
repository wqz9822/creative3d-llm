import requests
import json


def summarize(summaryurl):

    url = "https://kagi.com/api/v0/summarize?url="+summaryurl;
    response = requests.get(url, headers={'Authorization': 'Bot [and then replace this with api key i guess]'})

    # Parse the response as JSON
    data = json.loads(response.text)

    # Print the JSON data
    print(data)

summarize("http://bbc.co.uk")