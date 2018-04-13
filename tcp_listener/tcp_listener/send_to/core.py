
from .request import Request





def Send_to(tracker, agent):
    if tracker['request_type'] == 'Data':

        response = Request(tracker, agent)
        return response

    return tracker['request_type']








