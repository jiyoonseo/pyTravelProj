﻿from flask import Flask, url_for, request, render_template
from bs4 import BeautifulSoup
import json, requests

from Travel import app
from Travel import repo
from Travel.models.Flight import Flight
from Travel.models.Hotel import Hotel
from Travel.models.Place import Place
from Travel.models.trip import Trip

import datetime
from jinja2 import Template
from bs4.builder import HTML
from flask import Markup
from datetime import datetime
import re

travel_id = "ok whatever"
user_id = "user_js_01"
user_name = "June Seo"
trip_id = "default"
trip_id_used = False

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    global trip_id_used
    global trip_id
    if request.method == 'GET':  # ------------------------------------------------------------------------------------------------ GET

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

        ### new code block for home - start

        ## Set Trip_id and User_id for data handling
        tid = str(datetime.utcnow())
        tuid= user_id
        rp = [' ', ':', '.', '-']
        for c in rp:
            tid = tid.replace(c, '')
            tuid = tuid.replace(c, '')

        tid = tuid +tid
        trip_id = tid

        ## from Database Table 'trips'
        trips_result = repo.get_trips()  # list
        trips_output = ""
        temp_trip_id = "temp trip id"
        for event in trips_result:
            turn = False
            t_add = """
                <tr>
                    <td>
                """
            trips_output += t_add
            for cell in event:
                if(turn == False):
                    temp_trip_id = cell
                    turn = True
                t_add = cell + """ </td>
                            <td>"""
                trips_output += t_add
                
            t_add = """
                    <td><button type="button" class="btn btn-success btn-sm pull-right" onclick="location.href = '/trip/"""
            trips_output += t_add
            trips_output += str(temp_trip_id)
                    
            t_add = """';">View Details</button></td>
                    </td>
                        </tr>
                  """
            trips_output += t_add
        trips_output = Markup(trips_output)



        ### new code block for home - end

        return render_template(
        'index.html',
        title='Home Page',
        user_name = user_name,
        travel_id = travel_id,
        auto_gen_trip_id = trip_id,
        sorted_result = output,
        show_trip_list = trips_output,
        year=datetime.now().year
        )

    elif request.method == 'POST':  # ------------------------------------------------------------------------------------------------ POST

        trip_name = request.form['new_trip_name']
        if( is_bad_str(trip_name) ):
            msg = "WRONG INPUT: please try again to create a trip list"
            return render_template('wrongInputTrip.html',
                                   user_name = user_name,
                                   msg = msg
                                   )
            
                
        t = Trip(trip_id, trip_name, user_id)

        repo.add_trip_name(t)

        # if already used trip_id, create a new trip_id
        tid = str(datetime.utcnow())
        tuid= user_id
        rp = [' ', ':', '.', '-']
        for c in rp:
            tid = tid.replace(c, '')
            tuid = tuid.replace(c, '')

        tid = tuid +tid
        trip_id = tid


        ## from Database Table 'trips'
        trips_result = repo.get_trips()  # list
        trips_output = ""
        temp_trip_id = "temp trip id"
        for event in trips_result:
            turn = False
            t_add = """
                <tr>
                    <td>
                """
            trips_output += t_add
            for cell in event:
                if(turn == False):
                    temp_trip_id = cell
                    turn = True
                t_add = cell + """ </td>
                            <td>"""
                trips_output += t_add
                
            t_add = """
                    <td><button type="button" class="btn btn-success btn-sm pull-right" onclick="location.href = '/trip/"""
            trips_output += t_add
            trips_output += str(temp_trip_id)
                    
            t_add = """';">View Details</button></td>
                    </td>
                        </tr>
                  """
            trips_output += t_add
        trips_output = Markup(trips_output)

        return render_template(
        'index.html',
        title='Home Page',
        user_name = user_name,
        travel_id = travel_id,
        auto_gen_trip_id = trip_id,
        show_trip_list = trips_output,
        year=datetime.now().year,
        )


@app.route('/trip/<trip_id>', methods=['GET', 'POST'])
def trip(trip_id):
    if request.method == 'GET': # ------------------------------------------------------------------------------------------------ Get
        output = ""
        travel_result = repo.get_travel_events(trip_id)  # list of tuples
        
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

        return render_template(
        'trip.html',
        title='Home Page',
        user_name = user_name,
        travel_id = travel_id,
        trip_id = trip_id,
        sorted_result = output,
        year=datetime.now().year,
        )
    elif request.method == 'POST':   # ------------------------------------------------------------------------------------------------ POST

        # retrieve lists
        flights = request.values.getlist('flight')
        print(type(flights))
        print(len(flights))
        print(flights)
        
        flights_dt = request.values.getlist('flight_datetime')
        hotels = request.values.getlist('hotel')
        hotels_dt = request.values.getlist('hotel_datetime')
        places = request.values.getlist('place')
        places_dt = request.values.getlist('place_datetime')

        f_obj_list = []
        h_obj_list = []
        p_obj_list = []        

        # save respective objs in lists
        if(len(flights)!= 0 and len(flights)==len(flights_dt)):
            for i in range(len(flights)):

                # input validation 
                if(not is_valid_datetime(flights_dt[i]) or is_bad_str(flights[i]) ):
                    msg = ""
                    if(not is_valid_datetime(flights_dt[i])):
                        msg = msg + "<p style='color:#f00'><b>INVALID INPUT:</b> please try again to create a trip 'Flight Date/Time' field</p>"
                    if(is_bad_str(flights[i])):
                        msg = msg + "<p style='color:#f00'><b>INVALID INPUT:</b> please try again to create a trip 'Flight Name' field</p>"
                    
                    return render_template('wrongInputField.html',
                                           trip_id= trip_id,
                                            user_name = user_name,
                                            msg = Markup(msg)
                                            )
            

                f_obj = Flight(trip_id, flights_dt[i], flights[i] )  # create a Flight obj
                url = 'https://flightaware.com/live/flight/' + str(f_obj.info)
                req = req = requests.get(url)
                soup = BeautifulSoup(req.text, "html.parser")
                flight_state = []  # from website https://flightware.com/live/flight/
                for each in soup.findAll("td", {"class": "smallrow1"}):
                    flight_state.append(each.text)

                
                if(len(flight_state) == 0):
                    f_obj.status="NOT AVAILABLE"
                else:  # flight information is good to go
                    print(flight_state)  # keep going  & show live flight info
                    f_obj.status = str(re.sub(r'\([^)]*\)', '', flight_state[0]))    

                f_obj_list.append(f_obj)

        if(len(hotels)!= 0 and len(hotels)==len(hotels_dt)):


            for i in range(len(hotels)):
                # input validation 
                if(not is_valid_datetime(hotels_dt[i]) or is_bad_str(hotels[i]) ):
                    msg = ""
                    if(not is_valid_datetime(hotels_dt[i])):
                        msg = msg + "<p style='color:#f00'><b>INVALID INPUT:</b> please try again to create a trip 'Hotel Date/Time' field</p>"
                    if(is_bad_str(hotels[i])):
                        msg = msg + "<p style='color:#f00'><b>INVALID INPUT:</b> please try again to create a trip 'Hotel Name' field</p>"
                    
                    return render_template('wrongInputField.html',
                                            trip_id= trip_id,
                                            user_name = user_name,
                                            msg = Markup(msg)
                                            )

                h_obj = Hotel(trip_id, hotels_dt[i], hotels[i] )
                h_obj_list.append(h_obj)

        if(len(places)!= 0 and len(places)==len(places_dt)):

            for i in range(len(places)):
                # input validation 
                if(not is_valid_datetime(places_dt[i]) or is_bad_str(places[i]) ):
                    msg = ""
                    if(not is_valid_datetime(places_dt[i])):
                        msg = msg + "<p style='color:#f00'><b>INVALID INPUT:</b> please try again to create a trip 'Place Date/Time' field</p>"
                    if(is_bad_str(places[i])):
                        msg = msg + "<p style='color:#f00'><b>INVALID INPUT:</b> please try again to create a trip 'Place Name' field</p>"
                    
                    return render_template('wrongInputField.html',
                                            trip_id= trip_id,
                                            user_name = user_name,
                                            msg = Markup(msg)
                                            )

                p_obj = Place(trip_id, places_dt[i], places[i] )
                p_obj_list.append(p_obj)
            
        # add to repo -> database
        for each_flight_obj in f_obj_list:
            repo.add_flight(each_flight_obj)
        for each_hotel_obj in h_obj_list:
            repo.add_hotel(each_hotel_obj)
        for each_place_obj in p_obj_list:
            repo.add_place(each_place_obj)

        # time to display
        output = ""
        travel_result = repo.get_travel_events(trip_id)  # list of tuples        
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

        return render_template('trip.html',
                user_name = user_name,
                travel_id = travel_id,
                trip_id = trip_id,
                sorted_result = output,
                year=datetime.now().year,
                )






def is_valid_datetime(d):
    try:
        datetime.strptime(d, '%Y-%m-%dT%H:%M')
        return True
    except ValueError:
        return False

def is_bad_str(string):
    if not string:
        return True
    else:
        return False



















### ----------------------------------------- OLD ------------------------------------------------------------------------------------------------------------------------------
### ----------------------------------------- OLD ------------------------------------------------------------------------------------------------------------------------------

@app.route('/userInput', methods=['GET', 'POST'])
def userInput():

    if request.method == 'GET':
        return render_template('UserInput.html')

    elif request.method == 'POST':         # ----------------------------------------------------------------------------------------  -------------- post

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



