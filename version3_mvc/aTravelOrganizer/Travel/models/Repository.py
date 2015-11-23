import sqlite3


class Repository(object):

    def __init__(self, connectionString):
        self.__conn = sqlite3.connect(connectionString, check_same_thread=False)
        # self.__conn = sqlite3.connect(r'C:\Users\junes\OneDrive\Documents\Visual Studio 2015\Projects\pythonProject\TravelPlanner\TravelPlanner\data.sqlite')

    def __del__(self):
        self.__conn.close()

    def add_travel_info(self, flight_obj, hotel_obj, place_obj):
        try:
            with self.__conn:
                cursor = self.__conn.cursor()
                cursor.execute("insert into Flight (travel_id, title, datetime, flight_info, live_status) values(?, ?, ?, ?, ?)", (flight_obj.travel_id, flight_obj.title, flight_obj.datetime, flight_obj.info, flight_obj.status))
                cursor.execute("insert into Hotel (travel_id, title, datetime, hotel_info) values(?, ?, ?, ?)", (hotel_obj.travel_id, hotel_obj.title, hotel_obj.datetime, hotel_obj.info))
                cursor.execute("insert into Place (travel_id, title, datetime, place_info) values(?, ?, ?, ?)", (place_obj.travel_id, place_obj.title, place_obj.datetime, place_obj.info))
        except Exception as e:
            print("ERROR OCCURED in Repository.add_travel_info: "+ e)
            # Do something here
            raise

    def get_travel_events(self, travel_id):
        try:
            cursor = self.__conn.cursor()
            list_all = []

            for each in ["Flight","Hotel","Place"]:
                exe = cursor.execute("select * from " + each + " where travel_id = ?", (travel_id,))
                result = exe.fetchall()
                list_all.extend(result)


            # fetchone() --> get only the first line

            print(list_all)  # print tuple here

            
            return list_all
        except Exception as e:
            # Do something here
            print("ERROR OCCURED in Repository.get_travel_events:" + e)
            raise
        return