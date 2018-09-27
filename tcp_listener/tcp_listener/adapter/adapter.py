
class Adapter:
    @classmethod
    def decode(cls, datastring):
        # Given string data from a device, decode -> return standard 'Message'
        raise NotImplementedError()

    @classmethod
    def response_to(cls, datastring):
        # For this adapter, get response (Message) to one datastring
        raise NotImplementedError()

    @classmethod
    def detect(cls, datastring):
        # Given a datastring, determine adapter type it's for
        # and return this adapter's class
        from .tk102 import TK102
        if TK102.decode(datastring):
            return TK102
        # raise NotImplementedError("Unknown data".format(datastring))
