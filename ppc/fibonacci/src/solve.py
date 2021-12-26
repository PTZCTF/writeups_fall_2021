enc_flag = open("fibonacci.txt", "rb").read()

flag = ""

def next_fib(n):
    # Первоначальные значения для последовательности
    a = 0
    b = 1
    for _ in range(n):
        yield a
        c = a
        a = b
        b += c

fibonacci_for_flag = list(next_fib(100))

# Идём по элементам массива fibonacci_for_flag
for fib in fibonacci_for_flag:
    # Если значение числа Фибоначчи больше длины файла, 
    # то выходим из цикла
    if fib >= len(enc_flag):
        break

    # Иначе записываем во флаг
    else:
        flag += chr(enc_flag[fib])

print(flag)