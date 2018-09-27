
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
        from .tk103 import TK103
        if TK102.decode(datastring):
            return TK102
        elif TK103.decode(datastring):
            return TK103
        # raise NotImplementedError("Unknown data".format(datastring))
