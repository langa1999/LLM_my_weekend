from nredarwin.webservice import DarwinLdbSession
from langchain_core.tools import tool

from auth import get_railway_api_key


@tool
def get_departures_board():
    """
    A function that gets the train station boards and returns a string with all the next departures
    :return: str
    """
    api_key = get_railway_api_key()
    darwin_session = DarwinLdbSession(wsdl="https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx", api_key=api_key)

    departure_stations = ['WAT', 'VIC', 'LBG']
    result = ''
    for station in departure_stations:
        board = darwin_session.get_station_board(crs=station, rows=100, destination_crs = 'HAV', )
        for s in board.train_services:
            a = darwin_session.get_service_details(s.service_id)
            for c in a.subsequent_calling_points:
                if c.crs=='HAV':
                    result = f"Train to {c.location_name} arrives at {c.st} from {a.location_name} departing at {a.std}\n" # change to full station name
    return result if result else "No more trains today."
