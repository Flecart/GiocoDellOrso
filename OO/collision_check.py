# check if there are any collisions with the state strings
import numpy as np
state = "".join(['2', '1', '1', '1', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_'])

mappings = dict()  
mappings[hash(state)] = state  
times = 3 * 10 ** 7
shuffle = state 
for _ in range(times):
    shuffle = list(shuffle)
    np.random.shuffle(shuffle)
    shuffle = "".join(shuffle)   
    hash_value = hash(shuffle)
    if hash_value not in mappings:
        mappings[hash_value] = shuffle
    elif mappings[hash_value] != shuffle:
        print("collision found!")
        print(mappings[hash_value])
        print(shuffle)
        break
 
# seems OK