####LOOP Softwarare Trigger Init
import cnbiloop
from cnbiloop import BCI, BCI_tid

bci = BCI_tid.BciInterface()

def sendTiD(Event_):
        bci.id_msg_bus.SetEvent(Event_)
        bci.iDsock_bus.sendall(str.encode(bci.id_serializer_bus.Serialize()))

def receiveTiD():
    data = None
    try:
        data = bci.iDsock_bus.recv(512).decode("utf-8")
        bci.idStreamer_bus.Append(data)
    except:
        nS = False
        dec = 0
        pass
    # deserialize ID message
    if (data):
        if (bci.idStreamer_bus.Has("<tobiid", "/>")):
            msg = bci.idStreamer_bus.Extract("<tobiid", "/>")
            bci.id_serializer_bus.Deserialize(msg)
            bci.idStreamer_bus.Clear()
            tmpmsg = int(round(float(bci.id_msg_bus.GetEvent())))
            # print("Received Message: ", tmpmsg)
            return tmpmsg
               
        elif bci.idStreamer_bus.Has("<tcstatus","/>"):
            MsgNum = bci.idStreamer_bus.Count("<tcstatus")
            for i in range(1,MsgNum-1):
                # Extract most of these messages and trash them    
                msg_useless = bci.idStreamer_bus.Extract("<tcstatus","/>")

######## End of Loop Init





##send software
sendTiD(1000)  #example