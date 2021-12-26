# Разбор таска Baby Python Reverse (by keepontalkingtoyourself)

Категория:&nbsp;&nbsp;`Reverse`    
Стоимость:&nbsp;`50`  
First blood:&nbsp;&nbsp;`ded_preded1997`

---

## Что нам дано?

В этом таске нам дан [небольшой код](src/task.py) на Python. В нем искомый флаг по очевидным причинам убран, зато в самом конце есть [байтовая строка](https://www.programiz.com/python-programming/methods/built-in/bytes), которую этот алгоритм вернет:

```python
#b'WZ\x19Px^|QXjDsbZS~ueHu\x1c\x19LOIY^\x0b'
```

В коде есть три функции: `cold()`, `warm()` и `hot()`, которые последовательно применяются к строке `flag`:

```python
encrypted_flag = hot(warm(cold(flag)))
print(encrypted_flag.encode())
```

---

## Как начать решать?

Для начала попытаемся понять, что эти функции делают.

### `cold()`

```python
def cold(flag):
    enc = flag[::-1]
    return enc
```

В функции `cold()` используется срез ([slice](https://www.programiz.com/python-programming/methods/built-in/slice)). Аргументы `start` и `end` пустые, значит строка будет возвращена полностью, а `step` равен `-1`, поэтому строка будет прочитана с конца (развернута).

### `warm()`

```python
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
```

Сперва в функции `warm()` объявляются две фустые строки: `odd` и `even`. Цикл `for` проходит по всей длине строки `flag`: если индекс четный (`i % 2 == 0`), то символ с этим индексом добавляется к строке `odd`, в противном случае, к строке `even`. Потом строка из нечетных символов переворачивается, и все символы последовательно соединяются в итоговую строку `enc`.

Например, таким образом из `abcdefgh` получится `ahcfedgb`.

### `hot()`

```python
def hot(flag):
    enc = ""
    for i in range(len(flag)):
        enc += chr(42 ^ ord(flag[i]))
    return enc
```

И наконец, в функции `hot` каждый символ [шифруется при помощи XOR](https://en.wikipedia.org/wiki/XOR_cipher) с ключом 42.

Сначала [функция `ord()`](https://www.programiz.com/python-programming/methods/built-in/ord) возвращает код символа в Unicode, к полученному числу применяется XOR (операция `^`), а [функция `chr()`](https://www.programiz.com/python-programming/methods/built-in/chr) возвращает символ, соответствующий новому числовому коду.

### Output

Итоговая строка печатается в кодировке `UTF-8` ([`encode()`](https://www.programiz.com/python-programming/methods/string/encode)).

---

## Решение

Заметим, что все функции симметричны, то есть если их применить дважды, то получится исходное значение:

- `cold()` разворачивает строку полностью;
- `warm()` выбирает разворачивает только нечетные символы;
- `hot()` использует XOR, для которого применяется [симметричный ключ](https://en.wikipedia.org/wiki/Symmetric-key_algorithm).

Получается, нам нужно просто вызвать их в обратном порядке. Для этого заменим наш флаг на зашифрованный:

```python
flag = b'WZ\x19Px^|QXjDsbZS~ueHu\x1c\x19LOIY^\x0b'
```

Поменяем функции местами:

```python
decrypted_flag = cold(warm(hot(flag)))
print(decrypted_flag)
```

В функции `hot()` уберем `ord()`, потому что теперь она будет на вход сразу получать байты:

```python
enc += chr(42 ^ flag[i])
```

Можно запускать [скрипт](src/solution.py).

---

## Результат

*Voilà!*

Флаг: `ptzctf{6@bY_pyTHOn_r3VeRs3!}`