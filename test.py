import random

a = [0]

for z in range(10):

    print(a)

    b = random.randint(0,10)

    broken = False

    for i, e in enumerate(a):
        if e > b:
            a.insert(i, b)
            broken = True
            break

    if not broken:
        a.append(b)

print(a)
