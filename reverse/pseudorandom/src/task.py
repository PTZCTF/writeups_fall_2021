import random


def set_seed():
    seed = random.randint(0, 100)
    random.seed(seed)
    return seed


def encrypt(flag):
    key = set_seed()

    flag_arr = list(flag)
    random.shuffle(flag_arr)
    enc = ""
    for i in range(len(flag_arr)):
        enc += chr(ord(flag_arr[i]) ^ key)
    return enc


flag = "ptzctf{REDACTED}"
enc = encrypt(flag)
print(enc.encode())
# b'o\x7fxUEz~p~Odni:3cn.lYOKqzwDX~G'
