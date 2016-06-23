# mstart-api-java
This is the JAVA API to easily connect, send and receive messages from an M-START Server.

### The classes
**ClientSocket** is the class which manages connection, sending and receiving messages from an M-START Server.

**DataManagement** is the class which handles the OSC messages and provides and notification mechanism for any newly received messages as well as some convinient methods to send OSC messages to the M-START Server.

**ApplicationStub** is the skeleton of class which can be used to create an application which will process received OSC messages and send OSC messages regarding the status and data of connected system that can be useful to users.

### Processing a message
This can be done by re-implementing the methode `messageReceived` directly in `DataManagement` or class extending from it, as in ApplicationStub.
All the message sent from the M-START Server will have in their address `/client-send/`. From this you can parse the rest of the address to determine what action to perform.

```python
  """ Get the address of the message : "address = aMessage[0]"
      Now parse it. In the following example, we have received a message after the user pressed a button on its HMI
  """
  if address.startswith("/client-send/startButton") :
    print("The start button was pressed.") # Or any other operation you want to perform
  elif ... :
    # And so on
```

### Sending a message
There are to ways to send a message:

* using the convinience method `sendMessageTo`
```python
  dm.sendMessageTo("/robot/object/axis/1/intprop/rotation", 356)
```
* using `sendMessage` in `DataManagement`. In this case, you will need to compose the OSC message.
```python
  msg = OSCMessage()
  msg.setAddress("/robot/object/axis/1/intprop/rotation")
  msg.append(356)
  dm.sendMessage(msg)
```

Remember that the messages sent must have the same address as the one provided in the M-START Designer so the data source can receive them.

### Tests
No tests are bundled with this (yet).

### Support
You can send any request or ask any question to our support: support@mugen-sas.com
