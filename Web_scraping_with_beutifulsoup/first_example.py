import requests

url = "http://www.webscrapingfordatascience.com/paramhttp/?query=test"
r = requests.get(url)
print(r.text)