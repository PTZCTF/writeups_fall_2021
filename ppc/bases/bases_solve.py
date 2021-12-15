import socket
import base64

# Функция для получения и обработки информации от сервера
def recv_until(s, end=b"\n"):
    ba = bytearray()

    while True:
        data = s.recv(1)
        # if not data:
        #     raise RuntimeError('Server closed socket prematurely')
        ba += data
        if ba.endswith(end):
            break
    return ba.decode("utf-8")


# Функция для обработки кодировок
def detect_encoding(s):
    def check_bytes(s):
        if isinstance(s, str):
            s = s.encode()
        elif not isinstance(s, bytes):
            raise Exception(f'\"s\" is of type \"{type(s)}\" but need \"str\" or \"bytes\"')

        return s

    def is_base64(s):
        s = check_bytes(s)
        try:
            return base64.b64encode(base64.b64decode(s)) == s
        except Exception as error:
            return False

    def is_base32(s):
        s = check_bytes(s)
        try:
            return base64.b32encode(base64.b32decode(s)) == s
        except Exception as error:
            return False

    def is_base16(s):
        s = check_bytes(s)
        try:
            return base64.b16encode(base64.b16decode(s)) == s
        except Exception as error:
            return False

    def is_ascii85(s):
        s = check_bytes(s)
        try:
            return base64.a85encode(base64.a85decode(s)) == s
        except Exception as error:
            return False

    if is_base16(s):
        decans = base64.b16decode(s.encode()).decode('utf-8')
        return str(decans)

    if is_base32(s):
        decans = base64.b32decode(s.encode()).decode('utf-8')
        return str(decans)

    if is_base64(s):
        decans = base64.b64decode(s.encode()).decode('utf-8')
        return str(decans)

    if is_ascii85(s):
        decans = base64.a85decode(s.encode()).decode('utf-8')
        return str(decans)



HOST = "195.209.248.208"
PORT = 33331
s = socket.socket()
s.connect((HOST, PORT))
print('connected: ', HOST)

res = str(recv_until(s, end=b" >> ")) 
print(res) # Введи токен >>
s.sendall("тут персональный токен\n".encode())

res = str(recv_until(s))
print(res) # Тест на знание кодировок. Для того, чтобы получить флаг...

while True:
    res = str(recv_until(s, end=b" >> "))
    print(res, end = "") # выводит ответ от сервера

    # Обрабатываем последнюю строку
    if "Молодец" in res:
        res = str(recv_until(s))
        print(res, end="")
        break

    # декодирует ответ и добавляет "\n" 
    ans = detect_encoding(res[:-4]) + '\n' 

    print(ans, end="") # выводим что мы отправляем серверу
    s.sendall(ans.encode()) # отправляем серверу ответ