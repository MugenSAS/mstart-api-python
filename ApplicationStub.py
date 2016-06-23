from OSC import OSCMessage
from DataManagement import DataManagement
import time

""" This class is an application stub using the content of this API
    to dialog with an M-START Server
"""
class ApplicationStub(DataManagement) :

    def __init__(self, anActivity, IP, port) :
        super(ApplicationStub, self).__init__(anActivity, IP, port)
        # Initialize anything more you need here

    def messageReceived(self, aMessage) :

        address = aMessage[0]

        if address.startswith("/client-send/...") :
            """ Start processing the address 
                Access values in the message (value = aMessage[2])
            """        
        else :
            """ Complete your process 
            """
         
      
ap = ApplicationStub("Activity","192.168.0.1", 59900) #Replace here Activity    

while True :
    # Main loop





