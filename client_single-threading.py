import json, socket
HOST='172.16.11.34'
PORT=65323
rows, columns = 10, 10
my_map = [[0 for x in range(rows)] for y in range(columns)]
my_shoots=[[0 for x in range(rows)] for y in range(columns)]
print(my_map)
def print_map(m):
    for row in m:
        for column in row:
            print(str(column) + " ", end="")
        print("")
def check_out(boat):
    for i in range(boat[1]):
        for j in range(boat[0]):
            x,y=[int(i) for i in input("Введите координату: ").split(" ")]
            my_map[x-1][y-1]=1
        print_map(my_map)
def game(boat):
    for i in range(boat[1]):
        for j in range(boat[0]):
            x,y=[int(i) for i in input("Введите координату для выстрела: ").split(" ")]
            my_map[x-1][y-1]=1
#коннект сервера
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock: #создание сокета tcp
    sock.connect((HOST, PORT))
    sock.sendall(bytes("Hello", encoding="utf-8"))
    for ship in [[4, 1]]:
        check_out(ship)
    # for ship in [[4, 1], [3, 2], [2, 3], [1, 4]]:
    # check_out(ship)
    data = json.dumps(my_map)  # преобразование данных в json строку
    sock.sendall(bytes(data, encoding="utf-8")) #передача карты
    print("Карта отправлена на сервер")
    while True:
        received=sock.recv(1024) #считывание входящих данных
        if not received:
            print("Сервер завершил соединение")
            break
        received = received.decode("utf-8")
        if received.find("finish") == 0:
            print(received.split(":")[1])
            break
        else:
            shoot = input(received)  # координата
            n, m = shoot.split(" ")
            sock.sendall(bytes(shoot, encoding="utf-8"))
            received = sock.recv(1024)  # считывание входящих данных
            if int(received):
                my_shoots[int(n)-1][int(m)-1] = 1
            else:
                my_shoots[int(n)-1][int(m)-1] = "*"
            print_map(my_shoots)
