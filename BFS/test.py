#
from collections import Counter
for i in range(10000000):
    s = str(7*i)
    if len(s) == Counter(s)[s[0]]:
        print(7*i)