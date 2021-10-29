import time

t0 = time.time()
a = 1
for i in range(1000000):
    if a < 100000:
        a = a * (i % 2 + 1)
    else:
        a = a // (i % 2 + 1)
t1 = time.time()
total = t1-t0
print(total)