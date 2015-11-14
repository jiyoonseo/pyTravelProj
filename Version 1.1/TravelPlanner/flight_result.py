from bs4 import BeautifulSoup
import json, requests, xmltodict, re, traceback, sys

from Flight import Flight

# return incorrect flight info page when result is not available
# retrieve live flight information from website (no free api I found so far..)
url = 'https://flightaware.com/live/flight/' + str(flight.flight_info)
req = requests.get(url)
soup = BeautifulSoup(req.text, "html.parser")
print(soup.findAll("div", { "class" : "stylelistrow" }))

