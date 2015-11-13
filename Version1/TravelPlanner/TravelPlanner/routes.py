from flask import Flask, url_for, request, render_template
from bs4 import BeautifulSoup
import json, requests
from app import app
from Repository import Repository
from Flight import Flight
from Hotel import Hotel
from Place import Place



repo = Repository()

@app.route('/', methods=['GET', 'POST'])
def hello():
    """Renders a sample page."""
    # Travel Planner
    url = url_for('userInput')
    input_link = '<a href='+url+'>Go to Enter Travel Input</a>'
    return input_link

    

@app.route('/userInput', methods=['GET', 'POST'])
def userInput():
    if request.method == 'GET':
        return render_template('UserInput.html')
    elif request.method == 'POST':
        
        testid= 'testid_01'
        flight = Flight(testid, request.form['flight_datetime'], request.form['flight'] )  # request.form['flight_datetime']
        hotel = Hotel(testid, request.form['hotel_datetime'], request.form['hotel'] )  # request.form['hotel_datetime']
        place  = Place(testid, request.form['place_datetime'], request.form['place'] )  # request.form['place_datetime']

        # return incorrect flight info page when result is not available
        # return incorrect flight info page when result is not available
        # retrieve live flight information from website (no free api I found so far..)
        url = 'https://flightaware.com/live/flight/' + str(flight.flight_info)
        req = requests.get(url)
        soup = BeautifulSoup(req.text, "html.parser")
        flight_state = []
        for each in soup.findAll("td", {"class": "smallrow1"}):
            flight_state.append(each.text)

        if(len(flight_state) == 0):
            print("OOPS Error")  # return incorrect page
            return render_template('IncorrectFlightInfo.html', 
                            travel_id = testid, flight_info = flight.flight_info, hotel_info = hotel.hotel_info, loc_info = place.place_info,
                            flight_datetime = flight.datetime, hotel_datetime = hotel.datetime , loc_datetime = hotel.datetime
                            )
        else:
            print(flight_state)  # keep going  & show live flight info
        
            '''
        if(soup.findAll("td", {"class": "smallrow1"}) == None):
            print("OOPS Error")  # return incorrect page
            return render_template('IncorrectFlightInfo.html', 
                            travel_id = testid, flight_info = flight.flight_info, hotel_info = hotel.hotel_info, loc_info = place.place_info,
                            flight_datetime = flight.datetime, hotel_datetime = hotel.datetime , loc_datetime = hotel.datetime
                            )
        else:
            for each in soup.findAll("td", {"class": "smallrow1"}):
                flight_state.append(each.text)
            print(flight_state)  # keep going  & show live flight info

            '''

        repo.add_travel_info(flight, hotel, place)

        # return result information when flight info is availalble
        return render_template('ShowTravelInfo.html', 
                               travel_id = testid, flight_info = flight.flight_info, hotel_info = hotel.hotel_info, loc_info = place.place_info,
                               flight_datetime = flight.datetime, hotel_datetime = hotel.datetime , loc_datetime = hotel.datetime,
                               flight_state = flight_state[0]
                               )
    return
