
import sqlite3


class Repository(object):

    def __init__(self):
        self.__conn = sqlite3.connect(r'C:\Users\junes\OneDrive\Documents\Visual Studio 2015\Projects\pythonProject\TravelPlanner\TravelPlanner\data.sqlite')

    def __del__(self):
        self.__conn.close()

    def add_travel_info(self, flight_obj, hotel_obj, place_obj):
        try:
            with self.__conn:
                cursor = self.__conn.cursor()
                
                
                cursor.execute("insert into Flight (travel_id, datetime, flight_info) values(?, ?, ?)", (flight_obj.travel_id, flight_obj.datetime, flight_obj.flight_info))
                cursor.execute("insert into Hotel (travel_id, datetime, hotel_info) values(?, ?, ?)", (hotel_obj.travel_id, hotel_obj.datetime, hotel_obj.hotel_info))
                cursor.execute("insert into Place (travel_id, datetime, place_info) values(?, ?, ?)", (place_obj.travel_id, place_obj.datetime, place_obj.place_info))
        except Exception as e:
            print("ERROR OCCURED: "+e)
            # Do something here
            raise