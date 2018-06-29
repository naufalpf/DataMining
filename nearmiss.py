import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
from sklearn import datasets
from sklearn.datasets import make_classification
from imblearn.over_sampling import ADASYN
from imblearn.under_sampling import NearMiss 
from sklearn.decomposition import PCA as sklearnPCA
from sklearn.preprocessing import StandardScaler

#read dataset
dataset = pd.read_csv('ecoli4.csv')

#read kolom class
X = dataset.drop(['Class'], axis=1) 
y = dataset['Class'] 

#X, y = make_classification(n_classes=2, class_sep=2,weights=[0.1, 0.9], n_informative=3, n_redundant=1, flip_y=0,n_features=20, n_clusters_per_class=1, n_samples=1000,random_state=10)
print('Original dataset shape {}'.format(Counter(y)))

ada = NearMiss()
X_res, y_res = ada.fit_sample(X, y)
print('Resampled dataset shape {}'.format(Counter(y_res)))