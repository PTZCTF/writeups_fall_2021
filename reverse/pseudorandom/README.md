# Разбор таска (by keepontalkingtoyourself)

Категория:&nbsp;&nbsp;`Reverse`    
Стоимость:&nbsp;`350`  
First blood:&nbsp;&nbsp;`wingiu`

---

## Что нам дано?

Нам дан [небольшой скрипт](src/task.py), использующий встроенный в Python модуль [`random`](https://www.programiz.com/python-programming/modules/random) для работы со случайными числами. Флаг в нем заменен на `"ptzctf{REDACTED}"`, а конце кода есть [байтовая строка](https://www.programiz.com/python-programming/methods/built-in/bytes), которую этот алгоритм вернул:

```python
#b'o\x7fxUEz~p~Odni:3cn.lYOKqzwDX~G'
```

---

## Как начать решать?

Для начала надо понять, что делают описанные в коде функции:

1. В `encrypt()` сразу же вызывается `set_seed()`, а ее результат записывается в `key`. 

    ```python
    key = set_seed()
    ```

1. В `set_seed()` генерируется случайное целое число в диапазоне от 0 до 100, это число задается в качестве зерна для генерации псевдослучайных чисел.

    Подробнее про "Генератор псевдослучайных чисел" можно почитать [здесь](https://habr.com/ru/post/151187/). 
    
    Главное, что нужно понимать — фиксированный `seed()` гарантирует то, что генератор будет работать каждый раз по одной и той же схеме (т. е. "случайность" будет воспроизводиться при каждом запуске программы).

    ```python
    def set_seed():
        seed = random.randint(0, 100)
        random.seed(seed)
        return seed
    ```

1. Снова возвращаемся в функцию `encrypt()`. Строка превращается в список, состоящий из ее символов. Этот список перемешивается при помощи `shuffle()`.

    ```python
    flag_arr = list(flag)
    # 'abc' → ['a', 'b', 'c']
    random.shuffle(flag_arr)
    # ['a', 'b', 'c'] → ['b', 'c', 'a']
    ```

1. Каждый символ [шифруется при помощи XOR](https://en.wikipedia.org/wiki/XOR_cipher) с ключом, сгенерированным выше (тоже самое значение, что было передано в `seed()`).

    ```python
    for i in range(len(flag_arr)):
    enc += chr(ord(flag_arr[i]) ^ key)
    ```

    Сначала [функция `ord()`](https://www.programiz.com/python-programming/methods/built-in/ord) возвращает код символа в Unicode, к полученному числу применяется XOR (операция `^`), а потом [функция `chr()`](https://www.programiz.com/python-programming/methods/built-in/chr) возвращает символ, соответствующий новому числовому коду.

---

## Решение

Для решения этого таска придется писать код ([вот такой](src/solution.py)). Разберем его построчно:

1. Импортируем модуль для работы со случайными числами:

    ```python
    import random
    ```

1. Это наш зашифрованный флаг:

    ```python
    enc_flag = b"o\x7fxUEz~p~Odni:3cn.lYOKqzwDX~G"
    ```

1. Попробуем подобрать ключ, который использовался при шифровании и в качестве зерна генерации. Мы знаем, что `key` принимал значения от 0 до 100, поэтому диапазон выберем [`range(1, 101)`](https://www.programiz.com/python-programming/methods/built-in/range):

    ```python
    for key in range(0, 101):
    ```

1. Шифруем XOR-ом всю строку:

    ```python
    shuf_flag = "".join(list(map(lambda x: chr(x ^ key), list(enc_flag))))
    ```

    Разберем пошагово:

    - Превращаем байтовую строку в список чисел ([`list()`](https://www.programiz.com/python-programming/methods/built-in/list)):
    
        ```python
        list(enc_flag)
        # b'abc' → [97, 98, 99]
        ```
    
    - Применяем XOR к коду символа и превращаем полученный код в символ:

        ```python
        map(lambda x: chr(x ^ key), ...)
        ```

        [`lambda()`](https://www.programiz.com/python-programming/anonymous-function) — это способ записать функцию в одну строку.

        [`map()`](https://www.programiz.com/python-programming/methods/built-in/map) применяет функцию, переданную в качестве первого аргумента, к каждому элементу списка (второй агрумент).

    - Превращаем "map object" в список и соединяем все элементы в одну строку конструкцией [`"".join()`](https://www.programiz.com/python-programming/methods/string/join):

        ```python
        "".join(list(...))
        ```

    Более развернуто ~~и менее изящно~~ это можно записать так:

    ```python
    shuf_flag = ""
    for s in enc_flag:
        shuf_flag += chr(s ^ key)
    ```

1. Теперь проверяем, подходит ли нам расшифрованная этим ключом строка. Для этого узнаем, есть ли в ней символы `"ptzctf{}"`, ведь они гарантированно должны быть в нашем флаге:

    ```python
    if all(s in shuf_flag for s in "ptzctf{}"):
        print(shuf_flag, key)
        break
    # eur_OptztEndc09id$fSEA{p}NRtM 10
    ```

    > Здесь в условии используется [`all()`](https://www.programiz.com/python-programming/methods/built-in/all) и цикл [`for()`](https://www.programiz.com/python-programming/for-loop), записанный в одну строку.
    > 
    > То же самое можно записать так:
    > 
    > ```python
    > if "p" in shuf_flag and "t" in shuf_flag and "z" in ...
    > ```

    Если такая строка найдена, печатаем ее и подобранный ключ для проверки и останавливаем ([`break`](https://www.programiz.com/python-programming/break-continue)) перебор ключа.  

1. Теперь, зная какое число было сгенерировано в `set_seed()`, установим его в качестве нашего зерна генерации. Одинаковый `seed()` означает, что `shuffle()` будет проходить по одной и той же схеме, поэтому мы сможем обратить его действие.

    ```python
    random.seed(key)
    ```

1. `res` обозначим список состоящий из нулей, длиной как наш флаг. Нам нужно добавлять символы не в конец, а в разные места списка, поэтому такой формат будет удобнее:

    ```python
    res = [0] * len(shuf_flag)
    # [0] * 4 → [0, 0, 0, 0]
    ```

1. Теперь обратим перемешивание флага, применив `shuffle()` на список, чей правильный порядок мы будем знать точно:

    ```python
    perm = list(range(len(shuf_flag)))
    # list(range(5)) → [0, 1, 2, 3, 4]
    ```

1. Перемешаем:

    ```python
    random.shuffle(perm)
    # [0, 1, 2, 3, 4] → [3, 0, 2, 4, 1]
    ```

1. Теперь, расставим cимволы нашего флага в нужном порядке:

    ```python
    for i, j in enumerate(perm):
    res[j] = shuf_flag[i]
    ```

    [`enumerate()`](https://www.programiz.com/python-programming/methods/built-in/enumerate) нумерует каждый элементы списка. За номер отвечает переменная `i`, когда `j` — это сам элемент списка.

    ```python
    list(enumerate(['a', 'b', 'c', 'd']))
    # [(0, 'a'), (1, 'b'), (2, 'c'), (3, 'd')]
    ```

    Например:
    
    Мы смотрим, какое число стоит на 3 месте в перемешанном `perm` (`i = 2`, нумерация с нуля). Допустим, там оказалось число 7 (`j = 7`). Значит, 3 элемент из перемешанного флага будет помещен на 8 место в `res`.

1. Соединяем список `res` в строку известным способом и печатаем результат:
    ```python
    print("".join(res))
    ```

1. Запусим [скрипт](src/solution.py).


---

## Результат

Флаг: `ptzctf{pSeudORANd0M_intE9Er$}`