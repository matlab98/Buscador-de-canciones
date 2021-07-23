import numpy
import pandas as pd

def matching(fingerAi, finger_i):

    it = 0
    ta = 0
    tb = 0
    for i in range(len(fingerAi)):
     
        if fingerAi["Hash"].iloc[i]==finger_i["Hash"].iloc[i]: 

            it = it+1 
            print(it)


