from OSC import OSCStreamingClient, OSCMessage
import math, re, socket, select, string, struct, sys, threading, time, types, array, errno, inspect
from SocketServer import UDPServer, DatagramRequestHandler, ForkingMixIn, ThreadingMixIn, StreamRequestHandler, TCPServer
from contextlib import closing

"""This class manages connection to an M-START Server and sending and receiving OSC messages 
   from an M-START Server.
"""
class ClientSocket(OSCStreamingClient):


        """ Class constructor specifying the connection information de an M-START Server
            - observer(DataManagment) the class to notify when an OSC message from the server is received
            - IP(String): the M-START Server IP address
            - port(int): the M-Start Server port
            - anActivity(String): the Activity name as it is set in the M-START Server database
        """
	def __init__(self, observer, IP, port, anActivity):
		OSCStreamingClient.__init__(self)
                self._observer = observer
                self.address = (IP, port)
                self.activity = anActivity
                self.connecting = False
                self.connected = False
                self._txMutex2 = threading.Lock()
                self._txMutex3 = threading.Lock()

                
                
        """ Receive data from the M-START Server 
            - count (int) the size of the data to receive
        """
        def _receiveWithTimeout(self, count):
		chunk = str()
		while len(chunk) < count:
			try:
				tmp = self.socket.recv(count - len(chunk))
			except socket.timeout:
				if not self._running:
					print "CLIENT: Socket timed out and termination requested."
					return None
				else:
					continue
			except socket.error, e:

				if e[0] == errno.ECONNRESET:
                                        if e[0] == errno.ECONNRESET:
					        print "CLIENT: Connection reset by peer."
				                return False
                                      
				else:
				        raise e
			if not tmp or len(tmp) == 0: # The socket has been closed

                                if self.connecting :
                                        while not self.connected :
                                                time.sleep(10)
                                else :
                                        # Loop to try to reconnect the server
                                        self.connecting = True
                                        self.connected = False
                                        self._txMutex2.acquire()
                                        while not self.connected :
                                                try :
					                time.sleep(10) # Sleep for 10s before trying to reconnect the server
                                                        print("Trying to reconnect...")
                                                        self.reconnect(self.address)
                                                except socket.error, exc :
                                                        continue
                                        self.connecting = False
                                        self._txMutex2.release()
			chunk = chunk + tmp
		return chunk
        

        
        """ Loops to receive OSC messages from an M-START Server and notify the data management class 
            when one is fully received.

	    This method does not handle OSC bundles as raw messages are dispatched as OSC messages. To do so, 
	    extend or modify this method.
	"""
	def _receiving_thread_entry(self):
		print "CLIENT: Entered receiving thread."
		self._running = True
		while self._running:
			decoded = self._receiveMsgWithTimeout()
			if not decoded:
				continue
			elif len(decoded) <= 0:
				continue
                        else :
                                self._observer.messageReceived(decoded)
                
		print "CLIENT: Receiving thread terminated."

                
                
	"""Connects to the M-START Server and sets up the activity.
           - address ((String,int)) the address (IP and port) of the M-START Server
        """
        def connect(self, address):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, self.sndbuf_size)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.rcvbuf_size)
		self.socket.settimeout(1.0)
		self.socket.connect(address)
                self.connected = True 
                
                m2 = OSCMessage()
                m2.setAddress("/set-link-with-activity")
                m2.append(self.activity) 
                self.sendOSC(m2)
       
		self.receiving_thread = threading.Thread(target=self._receiving_thread_entry)
		self.receiving_thread.start()

                

        """Reconnects to the M-START Server and sets up the activity.
           - address ((String,int)) the address (IP and port) of the M-START Server
        """
        def reconnect(self, address):
	        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, self.sndbuf_size)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.rcvbuf_size)
		self.socket.settimeout(1.0)
		self.socket.connect(address)
                self.connected = True
                
                m2 = OSCMessage()
                m2.setAddress("/set-link-with-activity")
                m2.append(self.activity) 
                self.sendOSC(m2)
		


        """ Transmit data to the M-START Server 
            - data (String) binary representation of the message
        """
        def _transmitWithTimeout(self, data):
		sent = 0
		while sent < len(data):
		        try:
				tmp = self.socket.send(data[sent:])
                                if tmp == 0:
				        return False
			        sent += tmp
			except socket.timeout:
				if not self._running:
					print "CLIENT: Socket timed out and termination requested."
					return False
				else:
					continue
                                
			except socket.error, e:
				if e[0] == errno.EPIPE:

                                        if self.connecting :
                                                while not self.connected :
                                                        time.sleep(10)
                                        else :
                                                # Loop to try to reconnect the server
                                                self.connecting = True
                                                self.connected = False
                                                self._txMutex3.acquire()
                                                while not self.connected :
                                                        try :
					                        time.sleep(10) # Sleep for 10s before trying to reconnect the server
                                                                print("Trying to reconnect...")
                                                                self.reconnect(self.address)
                                                        except socket.error, exc :
                                                                continue
                                                self.connecting = False
                                                self._txMutex3.release()
				else:
					raise e
			
		return True
		

