from OSC import OSCMessage
from ClientSocket import ClientSocket
import threading


""" This class helps connecting to an M-START Server, managing received OSC messages from an
    M-START Server and facilitates sending OSC messages to an M-START Server.
"""
class DataManagement(object):
	
        """ Class constructor which provides connection to an M-START Server
            - anActivity(String): the Activity name as it is set in the M-START Server database
            - IP(String): the M-START Server IP address
            - port(int): the M-Start Server port
        """
	def __init__(self, anActivity, IP, port) :
                self.socket = ClientSocket(self, IP, port, anActivity)
                self.socket.connect((IP, port))
                self.lock = threading.Lock()

        
	""" This method is called when a message from the M-START Server is received.
            It has to be implemented in an other class extending from DataManagement
            in order to treat the messages received.
            Note: you can re-implement this method if you want to handle the 
            messages here.
        """
	def  messageReceived(self,aMessage) :
                print("No treatment defined for messages received")
	

        """ Send a message to the M-START Server.
            - aMessage(OSCMessage): the message to send
        """
	def sendMessage(self,aMessage) :
		self.socket.sendOSC(aMessage)

                
        """ Send a message to the M-START Server.
            - aMessage(address): the address of the OSC message
            - value: the value of the OSCMessage 
        """
        def sendMessageTo(self, address, value) :
                oscmsg = OSCMessage()
                oscmsg.setAddress(address)
                oscmsg.append(value)
                self.socket.sendOSC(oscmsg)
                
	
	
