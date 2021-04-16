from socketIO_client import SocketIO, LoggingNamespace

socketIO = SocketIO('localhost', 8002, LoggingNamespace)
print("Connected")

self_id = "a2"

states = {
    "l1" : 1,
    "l2" : 1,
    "l3" : 1,
    "l4" : 1,
    "temp1" : 20,
    "temp2" : 20,
    "heat1" : 15,
    "heat2" : 15,
}

def take(args):
	print(args)
     
def change_state(args):
    global states
    if str(self_id) == str(args["id"]):
        print("DATA CHANGE")
        states["l" + args["switch"]] = int(args["state"])
        print(states)


def heating_state(args):
    global states
    if str(self_id) == str(args["id"]):
        print("TEMP Change")
        states["heat" + args["heat"]] = float(args["temp"])
        print(states)

# socketIO.emit('hello')
# socketIO.on('st', take)
#socketIO.emit('hello')
socketIO.on('thank', take)
socketIO.on('switch', change_state)
socketIO.on('heating', heating_state)
while True:
    socketIO.emit('state', {"id" : self_id, "states" : states})
    socketIO.wait(seconds=2)