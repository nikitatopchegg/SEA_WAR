import json, socket
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
def step(i, j):
    connections[i].sendall(bytes("Игра началась! Введите координату: ", encoding="utf-8"))
    shoot=connections[i].recv(1024)
    shoot = shoot.decode("utf-8")
    n,m=shoot.split(" ")
    broken=maps[j][int(n)-1][int(m)-1]
    if broken>0:
        connections[i].sendall(bytes("1", encoding="utf-8"))
        brokens[j] += 1
        if brokens[j] >= NUM_TO_FINISH:
            return 0
    else:
        connections[i].sendall(bytes("0", encoding="utf-8"))
    return 1
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    addr = (HOST, PORT)      # кортеж из ip-адреса и порта
    s.bind(addr)                 # связываем ip-адрес и порт
    s.listen()               # слушаем траффик входящий на сокет
    while True:
        conn, addr = s.accept() # ждём и даём разрешение на подключение любого первого клиента
        if conn not in connections:
            connections.append(conn)
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)  # считываем входящие данные по 1 килобайту
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
    while step(0,1) and step(1,0):
        pass
    else:
        if brokens[0]==NUM_TO_FINISH:
            connections[0].sendall(bytes("finish:Ты проиграл!", encoding="utf-8"))
            connections[1].sendall(bytes("finish:Ты выйграл!!", encoding="utf-8"))
        else:
            connections[1].sendall(bytes("finish:Ты проиграл!", encoding="utf-8"))
            connections[0].sendall(bytes("finish:Ты выйграл!!", encoding="utf-8"))
