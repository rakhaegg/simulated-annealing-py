
from bdb import Breakpoint


data = [1 , 2 , 32, 4]
data_banya = [
    [1 , 2 , 32, 4],
    [1 ,3 ,3 ,4],
    [2 ,2 ,3, 4, ],
]
data_asal = [2 , 3,1,1]

for x in data_banya:
    if x == data_asal:
        print("Ada")
        break