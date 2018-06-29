import pandas as pd  
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

from imblearn.ensemble import EasyEnsemble
from imblearn.over_sampling import ADASYN
from imblearn.under_sampling import NearMiss 

#read dataset
dataset = pd.read_csv('ecoli4.csv')

#read kolom class
X = dataset.drop(['Class'], axis=1) 
y = dataset['Class'] 

print('Original dataset shape {}'.format(Counter(y)))

ada = NearMiss()
X_res, y_res = ada.fit_sample(X, y)
print('Resampled dataset shape {}'.format(Counter(y_res)))


#menampilkan visualisasi grafik
besar = dataset.groupby(['Class']).size()
besar = list(besar)
#print('total:{}'.format(besar))

#koordinat x, koordinat y
koor_x = ['Positive','Negative']
koor_y = besar

y_res = list(y_res)
#print('total:{}'.format(y_res))

valp = y_res.count(' positive')
valn = y_res.count(' negative')

#print('total:{}'.format(valn))

new_y = []
new_y.append(valp)
new_y.append(valn)

plt.bar(koor_x,new_y, label = 'After Neramiss', color='c', width = 0.5, align = 'center')
plt.bar(koor_x,koor_y, label = 'Before Nearmiss', color='r', width = -0.3, align = 'edge')

plt.xlabel('x')
plt.ylabel('Value')

plt.title('Graph')

plt.legend()
plt.show()