import scipy
from sklearn.preprocessing import Imputer
from sklearn.decomposition import PCA
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
import random
from sklearn import svm
from sklearn import decomposition
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import StandardScaler
#import knn_impute as ki
# from sklearn.cross_validation import train_test_split

# input edited csv adult
data = pd.read_csv("adult.csv")
row, col = data.shape

for part in data:
    data[part] = data[part].replace('?', np.NaN)


stringcol = ['workclass', 'education', 'marital-status', 'occupation', 'relationship', 'race', 'sex', 'native-country']
numericcol = [1, 3, 5, 6, 7, 8, 9, 13]
_class = data.iloc[:, col - 1].values

#colum <=50k / >50k tidak bisa di binary kan. dihapus
del data['wage']


#handling categorical values into binary values

temp = []

for part in range(0, len(numericcol)):
    if part == 0:
        cat_string = data.iloc[:, [numericcol[part]]].values
        cat_string = pd.DataFrame(cat_string, columns=list('x'))
        temp.append(cat_string)
    else:
        cat_string1 = data.iloc[:, [numericcol[part]]].values
        cat_string1 = pd.DataFrame(cat_string1, columns=list('x'))
        temp.append(cat_string1)

temp_new = []
for part in range(0, len(temp)):
    temp_new.append(pd.get_dummies(temp[part]))

for part in range(0, len(temp)):
    temp_new[part].loc[temp[part].x.isnull(), temp_new[part].columns.str.startswith('x_')] = np.nan

for part in range(0, len(numericcol)):
    if part == 0:
        del data[stringcol[part]]
    else:
        del data[stringcol[part]]

for part in range(0, len(temp_new)):
    if part == 0:
        binary = temp_new[part]
    else:
        binary = pd.concat([binary, temp_new[part]], axis=1)

data = pd.concat([data, binary], axis=1)
row, col = data.shape
x = data.values

#appending columns
index_col = []
for part in range(0, col):
    index_col.append(part + 1)

#imputer knn
#new_data = ki.knn_impute(target=df['age'], attributes=df.drop(['age', 'fnlwgt'], 1),
#                                    aggregation_method="mean", k_neighbors=2, numeric_distance='euclidean',
#                                    categorical_distance='hamming', missing_neighbors_threshold=0.8)
#df = df.assign(age = new_data)
#print(df)
#
#new_data = ki.knn_impute(target=df['workclass'], attributes=df.drop(['Age', 'fnlwgt'], 1),
#                                    aggregation_method="mean", k_neighbors=1, numeric_distance='euclidean',
#                                    categorical_distance='hamming', missing_neighbors_threshold=0.8)
#
#df = df.assign(workclass = new_data)
#print(df)

#imputer median
imputer = Imputer(missing_values="NaN", strategy='median', axis=0)
imputer = imputer.fit(x[:, :col])
x[:, :col] = imputer.transform(x[:, :col])
df = pd.DataFrame(x, columns=index_col)
print df

#PCA time!!
temp_pca = PCA(n_components=3)
pc = temp_pca.fit_transform(df.values)
datapca = pd.DataFrame(data=pc, columns=['age', 'workclass', 'fnlwgt'])
print datapca

#classification
new_df = datapca.values
X_train, X_test, y_train, y_test = train_test_split(datapca, _class, test_size=0.33)
neigh = KNeighborsClassifier(n_neighbors=3)
neigh.fit(X_train, y_train)
pred = neigh.predict(X_test)
print accuracy_score(y_test, pred)

new_df = datapca.values
X_train, X_test, y_train, y_test = train_test_split(datapca, _class, test_size=0.33)
clf = GaussianNB()
clf.fit(X_train, y_train)
target_pred = clf.predict(X_test)
print accuracy_score(y_test, pred)
#
plt.scatter(pc[:, 0], pc[:, 1],pc[:, 2], marker='o')
plt.show()