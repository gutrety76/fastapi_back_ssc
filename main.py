from typing import Union
import socket
import threading
from fastapi import FastAPI
from fetchdata import bancard, check_cards, increase_fail, increase_suc, unbancard

app = FastAPI()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('192.168.1.251', 8888)
sock.sendto(b"0LDRg9GE", server_address)

# Store data globally
received_data = ""

def getdata():
    global received_data
    while True:
        data, address = sock.recvfrom(1024)
        received_data = data.decode()
        
        res = check_cards(int(received_data))
        
        if res[1] != False:
            
            sock.sendto(b"open", server_address)  
            print(increase_suc(res[4]))
        elif res[1] == False:
            print(increase_fail(res[4]))
# Start the data fetching in a new thread
fetch_thread = threading.Thread(target=getdata)
fetch_thread.start()

@app.post("/api/banuser/{name}")
def banuser(name:int):
    
    res = bancard(name)
    return res

@app.post("/api/unbanuser/{name}")
def unbanuser(name:int):
    
    res = unbancard(name)
    return res

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    global received_data
    return {"item_id": item_id, "q": q, "Data": received_data}
