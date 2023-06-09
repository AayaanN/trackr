import torch
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import torch.nn as nn

data = pd.read_csv('AMZN.csv')

data = data['open','close']

print(data)
