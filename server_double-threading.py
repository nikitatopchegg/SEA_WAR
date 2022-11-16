import json, socket
from threading import Thread

HOST='0.0.0.0'
PORT=65323
NUM_TO_FINISH=4
connections=[]
maps=[]
brokens=[0,0]

def print_map(m):
    for row in m:
        for column in row:
            print(str(column) + " ", end="")
        print("")

def reading_map():
    d = conn.recv(1024)
    return d

def step(i, j):
    while brokens[j] < NUM_TO_FINISH:
        if brokens[i] >= NUM_TO_FINISH:
            return
        connections[i].sendall(bytes("Введите координату: ", encoding="utf-8"))
        shoot=connections[i].recv(1024)
        shoot = shoot.decode("utf-8")
        n,m=shoot.split(" ")
        broken=maps[j][int(n)-1][int(m)-1]
        if broken>0:
            connections[i].sendall(bytes("1", encoding="utf-8"))
            brokens[j] += 1
        else:
            connections[i].sendall(bytes("0", encoding="utf-8"))
    else:
        connections[j].sendall(bytes("finish:Ты проиграл!", encoding="utf-8"))
        connections[i].sendall(bytes("finish:Ты выйграл!!", encoding="utf-8"))



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    addr = (HOST, PORT)      # кортеж из ip-адреса и порта
    s.bind(addr)                 # связываем ip-адрес и порт
    s.listen()   # слушаем траффик входящий на cервер
    while True:
        conn, addr = s.accept() # ждём и даём разрешение на подключение любого первого клиента
        if conn not in connections:
            connections.append(conn)
        print('Connected by', addr)
        while True:
            data = reading_map() # считываем входящие данные по 1 килобайту
            if not data:
                break
            try:
                data=json.loads(data)
                maps.append(data)
                print_map(data)
                break
            except:
                print(data)
        print(maps)
        print(connections)

        if len(maps)==2 and len(connections)==2:
            break

    thread1 = Thread(target=step, args=(0, 1,))
    thread2 = Thread(target=step, args=(1, 0,))
    thread1.start()
    thread2.start()
