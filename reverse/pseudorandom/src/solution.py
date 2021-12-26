import random

enc_flag = b"o\x7fxUEz~p~Odni:3cn.lYOKqzwDX~G"

for key in range(0, 101):
    shuf_flag = "".join(list(map(lambda x: chr(x ^ key), list(enc_flag))))
    if all(s in shuf_flag for s in "ptzctf{}"):
        print(shuf_flag, key)
        break

random.seed(key)
res = [0] * len(shuf_flag)
perm = list(range(len(shuf_flag)))
random.shuffle(perm)
for i, j in enumerate(perm):
    res[j] = shuf_flag[i]

print("".join(res))
# ptzctf{pSeudORANd0M_intE9Er$}