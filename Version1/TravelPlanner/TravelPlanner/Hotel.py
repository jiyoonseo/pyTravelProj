from Travel import Travel

class Hotel(Travel):

    def __init__(self, travel_id, datetime, hotel_info):
        super().__init__(travel_id, datetime)
        self.hotel_info = hotel_info