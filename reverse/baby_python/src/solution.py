def hot(flag):
    enc = ""
    for i in range(len(flag)):
        enc += chr(42 ^ flag[i])
    return enc


def warm(flag):
    odd = ""
    even = ""
    for i in range(len(flag)):
        if i % 2 == 0:
            odd += flag[i]
        else:
            even += flag[i]

    even = even[::-1]
    enc = ""

    for i in range(len(odd)):
        enc += odd[i] + even[i]
    return enc


def cold(flag):
    enc = flag[::-1]
    return enc


flag = b"WZ\x19Px^|QXjDsbZS~ueHu\x1c\x19LOIY^\x0b"
decrypted_flag = cold(warm(hot(flag)))
print(decrypted_flag)
# ptzctf{6@bY_pyTHOn_r3VeRs3!}
