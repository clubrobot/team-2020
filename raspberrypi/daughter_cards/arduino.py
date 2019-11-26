from common.serialtalks import *
from common.components import *

_MANAGE_OPCODE = 0X07
_SUBSCRIBE     = 0X0
_UNSUBSCRIBE   = 0X1

def TopicHandler(*args):
    def producedDecorator(fct):
        def cap_fct(self, data):
            if(len(args)>1):
                return fct(self, *data.read(*args))
            else :
                return fct(self,  data.read(*args))
        return cap_fct
    return producedDecorator

class Arduino(SerialTalksProxy):
    def __init__(self, server, uuid):
        SerialTalksProxy.__init__(self, server, uuid)

    def addTopic(self, topic_code, handler, name, timestep):
        name = name[0].upper() + name.lower()[1:]

        if  (not self.__dict__.get("subscribe"+name, None) is None ) or (not self.__dict__.get("unsubscribe"+name, None) is None):
            raise RuntimeError("Unable to create subscriber method")

        def sub():
            output = self.execute(
                _MANAGE_OPCODE, BYTE(_SUBSCRIBE), BYTE(topic_code), LONG(timestep))
            return bool(output.read(BYTE))

        def usub():
            output = self.execute(
                _MANAGE_OPCODE, BYTE(_UNSUBSCRIBE),  BYTE(topic_code))
            return bool(output.read(BYTE))

        self.__setattr__("subscribe"+name, sub)
        self.__setattr__("unsubscribe"+name, usub)

        self.bind(topic_code, handler)

class SecureArduino(SecureSerialTalksProxy):
    def __init__(self, server, uuid, default_result):
        SecureSerialTalksProxy.__init__(self, server, uuid, default_result)

    def addTopic(self, topic_code, handler, name, timestep):
        name = name[0].upper() + name.lower()[1:]

        if  (not self.__dict__.get("subscribe"+name, None) is None ) or (not self.__dict__.get("unsubscribe"+name, None) is None):
            raise RuntimeError("Unable to create subscriber method")

        def sub():
            output = self.execute(
                _MANAGE_OPCODE, BYTE(_SUBSCRIBE), BYTE(topic_code), LONG(timestep))
            return bool(output.read(BYTE))

        def usub():
            output = self.execute(
                _MANAGE_OPCODE, BYTE(_UNSUBSCRIBE),  BYTE(topic_code))
            return bool(output.read(BYTE))

        self.__setattr__("subscribe"+name, sub)
        self.__setattr__("unsubscribe"+name, usub)

        self.bind(topic_code, handler)

class ArduinoLocal(SerialTalks):
    def __init__(self, port):
        SerialTalks.__init__(self, port)

    def addTopic(self, topic_code, handler, name, timestep):
        name = name[0].upper() + name.lower()[1:]

        if  (not self.__dict__.get("subscribe"+name, None) is None ) or (not self.__dict__.get("unsubscribe"+name, None) is None):
            raise RuntimeError("Unable to create subscriber method")

        def sub():
            output = self.execute(
                _MANAGE_OPCODE, BYTE(_SUBSCRIBE), BYTE(topic_code), LONG(timestep))
            return bool(output.read(BYTE))

        def usub():
            output = self.execute(
                _MANAGE_OPCODE, BYTE(_UNSUBSCRIBE),  BYTE(topic_code))   
            return bool(output.read(BYTE))

        self.__setattr__("subscribe"+name, sub)
        self.__setattr__("unsubscribe"+name, usub)

        self.bind(topic_code, handler)


