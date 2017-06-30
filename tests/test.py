# -*- coding: utf-8 -*-

#import context
#assuming installed
import ews
from random import random
import pandas as pd



#x =[random.randint(0,20) for i in range(1000)]

data = pd.read_csv("./sample_emerging.csv", sep = "\t", header=None)
x = data[2].tolist()

ews_data = pd.DataFrame(ews.get_ews(x, 100, 1))

ews_data.to_csv("./ews_data.csv")