from typing import Union
import socket
import threading
from fastapi import FastAPI
from fetchdata import bancard, check_cards, fetchStatistic, get_cards, increase_fail, increase_suc, unbancard
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('192.168.1.251', 8888)
sock.sendto(b"0LDRg9GE", server_address)

# Store data globally
received_data = ""

def getdata():
    global received_data
    print(received_data)
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
from fastapi import HTTPException
from datetime import datetime

@app.get("/api/statistics")
def get_statistics(start_date: str, end_date: str):
    # try:
    #     # Convert dates to datetime objects
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    # except ValueError:
    #     raise HTTPException(status_code=400, detail="Invalid date format. Use 'YYYY-MM-DD'")

    stats = fetchStatistic(start_date,end_date)
    
    res = []
    for card in stats:
        res.append({
            "id": card[0],
            "registered": card[1],
            "att_suc": card[2],
            "timestamp": card[3],
            "name": card[4]
        })
    return res
@app.post("/api/banuser/{name}")
def banuser(name:int):
    
    res = bancard(name)
    return {"id": res[0], "registered": res[1], "att_suc": res[2], "att_fail": res[3], "number": res[4], "id_number": res[5]}
@app.get("/api/getcards")
def getcards():
    res = get_cards()
    resа = []
    for card in res:
        resа.append({
            "id": card[0],
            "registered": card[1],
            "att_suc": card[2],
            "att_fail": card[3],
            "number": card[4],
            "id_number": card[5],
            "name": card[6]
        })
    
    return resа    
@app.post("/api/unbanuser/{name}")
def unbanuser(name:int):
    
    res = unbancard(name)
    return {"id": res[0], "registered": res[1], "att_suc": res[2], "att_fail": res[3], "number": res[4], "id_number": res[5]}
    

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    global received_data
    return {"item_id": item_id, "q": q, "Data": received_data}
