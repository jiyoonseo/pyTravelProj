from Travel  import Travel

class Flight(Travel):
    def __init__(self, travel_id, datetime, flight_info):
        super().__init__(travel_id, datetime)
        self.flight_info = flight_info

    def set_status(status):
        self.status = status

    def get_status():
        return self.status