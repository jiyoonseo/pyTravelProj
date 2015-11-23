from flask import Flask, url_for, request, render_template
from bs4 import BeautifulSoup
import json, requests
from Travel.models.Flight import Flight
from Travel.models.Hotel import Hotel
from Travel.models.Place import Place

from Travel import app
from Travel import repo


# from Travel.models.Place import Place
import datetime
from jinja2 import Template
from bs4.builder import HTML
from flask import Markup
import re

travel_id = 'travel_01'


@app.route('/')
def hello():
    return render_template('home.html')
        

@app.route('/userInput', methods=['GET', 'POST'])
def userInput():

    if request.method == 'GET':
        return render_template('UserInput.html')

    elif request.method == 'POST':        
        flight = Flight(travel_id, request.form['flight_datetime'], request.form['flight'] )  # request.form['flight_datetime']
        hotel = Hotel(travel_id, request.form['hotel_datetime'], request.form['hotel'] )  # request.form['hotel_datetime']
        place  = Place(travel_id, request.form['place_datetime'], request.form['place'] )  # request.form['place_datetime']

        # return incorrect flight info page when result is not available
        # retrieve live flight information from website (no free api I found so far..)
        url = 'https://flightaware.com/live/flight/' + str(flight.info)
        req = requests.get(url)
        soup = BeautifulSoup(req.text, "html.parser")
        flight_state = []  # from website https://flightware.com/live/flight/
        for each in soup.findAll("td", {"class": "smallrow1"}):
            flight_state.append(each.text)

        output = """
                <tr>
                    <th>Event</th>
                    <th>Detail</th>
                    <th>Date/Time</th>
                    <th>Status</th>
                </tr>
        """

        if(len(flight_state) == 0):
            flight.status="NOT AVAILABLE"
            tl = [flight, hotel, place]
            tl.sort(key= lambda obj: obj.datetime)            

            for obj in tl:            
                add =  """
                            <tr>
                                <td>""" + obj.title + """</td>
                                <td>""" + obj.info + """</td>
                                <td>""" + obj.datetime + """</td>
                                <td style='color:#f00'>""" + obj.status + """</td>
                            </tr>
                        """
                output += add
            
            output = Markup(output)
            return render_template('IncorrectFlightInfo.html', 
                            travel_id = travel_id, sorted_result= output
                            )
        else:  # flight information is good to go
            print(flight_state)  # keep going  & show live flight info
            flight.status = str(re.sub(r'\([^)]*\)', '', flight_state[0]))


        repo.add_travel_info(flight, hotel, place)

        # return result information when flight info is availalble 
        # dt = datetime.datetime.strptime(flight.datetime, "%Y-%m-%dT%H:%M")  # conversion
        
        tl = [flight, hotel, place]
        tl.sort(key= lambda obj: obj.datetime)
                
        for obj in tl:
            
            add =  """
                        <tr>
                            <td>""" + obj.title + """</td>
                            <td>""" + obj.info + """</td>
                            <td>""" + obj.datetime + """</td>
                            <td style='color:#00bde4'>""" + obj.status + """</td>
                        </tr>
                    """
            output += add
            
        output = Markup(output)
        return render_template('ShowTravelInfo.html', 
                               travel_id = travel_id, sorted_result= output)

    return   # end of userInput()


@app.route('/travel', methods=['GET', 'POST'])
def travel():
    if request.method == 'GET':
        return render_template('ShowTravelInfo.html', travel_id = travel_id)
    elif request.method == 'POST':
        travel_result = repo.get_travel_events(travel_id)  # list of tuples
        output = ""
        for event in travel_result:
            add = """
                <tr>  
                    <td>              
            """
            output += add
            for cell in event:
                add =  cell + """</td>
                                <td>"""
                output += add

            add = """</td>
                            </tr>
                        """
            output += add
            
        output = Markup(output)
        return render_template('ShowTravelInfo.html', 
                               travel_id = travel_id, sorted_result= output)
        # return str(result_flight)

    return

