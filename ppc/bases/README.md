# Разбор таска Bases

Категория:&nbsp;&nbsp;`PPC`    
Стоимость:&nbsp;`300`  
First blood:&nbsp;&nbsp;`DMA.ORG`

---

## Что нам дано?

Тест на знание кодировок. Для того, чтобы получить флаг, необходимо правильно и быстро определить кодировку и отправить исходную строку. Для решения тебе понадобится токен: *тут был персональный токен*.

`nc 195.209.248.208 33331`

---

## Как начать решать?

Для того, чтобы решить этот таск нужно понимать/ нагуглить кодировки. На [четвертой лекции](https://youtu.be/xoABXnwjWNU?t=2326) были разобраны кодировки [Base16](https://en.wikipedia.org/wiki/Hexadecimal), [Base32](https://en.wikipedia.org/wiki/Base32), [Base64](https://en.wikipedia.org/wiki/Base64) и [Base85 (Ascii85)](https://en.wikipedia.org/wiki/Ascii85).

Так как категория таска **PPC** и нам сказано, что **необходимо правильно и быстро определить кодировку**, значит, надо будет писать код, который 
1. Обращается к серверу; 
2. Принимает какие-то данные;
3. Обрабатывает эти данные;
4. Отправляет обработанные данные.

---

## Решение

### 1. Определяем, что нужно серверу
Подсоединяемся к серверу через netcat `nc 195.209.248.208 33331` (именно та команда, которая была указана в описании).  

Он спрашивает у нас персональный токен:
```bash
Введи токен >>
```
Появляется описание таска и условия, для получения флага:
```bash
Введи токен >> REDACTED
Тест на знание кодировок. Для того, чтобы получить флаг, необходимо правильно и быстро определить кодировку и отправить мне исходную строку. Удачи :)
...
```
И затем сервер начинает отправлять строчки с различными кодировками:

```
...
ONSG2YLCKJDGYUTM >>
```

### 2. Пишем код

На первых занятиях мы прошли ([тут начало](https://youtu.be/jVe-_-L2Q4s)) основы языка программирования Python. Реализуем соединение с сервером:

Импортируем модуль [socket](https://docs.python.org/3/library/socket.html) для соединения серверу и [base64](https://docs.python.org/3/library/base64.html) для обработки строк
```python
import socket
import base64
```

Следующим этапом будет реализация функции получения данных от сервера
```python
# Функция для получения и обработки информации от сервера
def recv_until(s, end=b"\n"):
    ba = bytearray()

    while True:
        data = s.recv(1)
        ba += data
        if ba.endswith(end):
            break
    return ba.decode("utf-8")
```

Теперь можем подключаться к серверу

```python
HOST = "195.209.248.208"
PORT = 33331
s = socket.socket()
s.connect((HOST, PORT))
print('connected: ', HOST)
```

Вводим наш токен и получаем условия для таска:
```python
res = str(recv_until(s, end=b" >> ")) 
print(res) # Введи токен >>
s.sendall("тут персональный токен\n".encode())

res = str(recv_until(s))
print(res) # Тест на знание кодировок. Для того, чтобы получить флаг...
```

---

Дальше идёт наша основная задача -- обработка кодировок. Самое важное -- правильный порядок определения кодировок: Base16 -> Base32 -> Base64 -> Ascii85. Простой разбор `is_base?`: проверяем, если мы переведём строку в UTF-8, затем переведём в base?, будет ли она совпадать с нашей исходной строкой? Если да, то мы нашли *ту самую кодировку*, иначе ищем дальше.

```python
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
```

Теперь запрашиваем строки у сервера и декодируем строки 
```python
while True:
    res = str(recv_until(s, end=b" >> "))
    print(res, end = "") # выводит ответ от сервера

    # декодирует ответ и добавляет "\n" 
    ans = detect_encoding(res[:-4]) + '\n' 

    print(ans, end="") # выводим что мы отправляем серверу
    s.sendall(ans.encode()) # отправляем серверу ответ
```

И после запуска программы и прохождения теста мы видим, что ответ от сервера изменился: `Молодец >> `. Значит, мы дошли до конца! Обработаем последнюю строчку:

```python
while True:
    res = str(recv_until(s, end=b" >> "))
    print(res, end = "")

    # Обрабатываем последнюю строку
    if "Молодец" in res:
        res = str(recv_until(s))
        print(res, end="")
        break

    ans = detect_encoding(res[:-4]) + '\n'
    print(ans, end="")
    s.sendall(ans.encode())    
```

Последняя строчка: `Молодец >> Держи свой флаг: ptzctf{5ucH_MuCH_84$3S_mgimO_fINishED}`

---

## Результат

Итоговый код вы можете найти [здесь](./bases_solve.py)

Флаг: `ptzctf{5ucH_MuCH_84$3S_mgimO_fINishED}`
