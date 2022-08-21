def my_add(x, level):
    lista = list()
    lista.append(x)

    y = x + 1
    print("start:", y, level, lista)
    level += 1
    if level > 10:
        return
    my_add(y, level)
    print("end:", y, level, lista)


for i in range(10):
    my_add(0, 0)
