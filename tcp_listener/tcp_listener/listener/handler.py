from tcp_listener.tk103_parser import Parse
from tcp_listener.send_to import Send_to


def handle_tracker(data, agent):
    tracker = Parse(data)
    respone = Send_to(tracker, agent)
    return respone






