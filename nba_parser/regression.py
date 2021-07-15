from sklearn.datasets import make_regression
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import BayesianRidge
from sklearn import svm
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
import matplotlib.pyplot as plt
from sklearn.linear_model import RidgeCV


import pandas as pd
import numpy as np
from sklearn.metrics import r2_score
# create datasets

df = pd.read_csv("RAPM.csv")
p1 = df.iloc[:, 5:6]
p2 = df.iloc[:, 8:9]

tot = df[['rapm1', 'rapm2', 'rapm_pair']]
off = df[['orapm1', 'orapm2', 'orapm_pair']]
defe = df[['drapm1', 'drapm2', 'drapm_pair']]

tot2 = df[['rapm1', 'rapm2']]
off2 = df[['orapm1', 'orapm2']]
defe2 = df[['drapm1', 'drapm2']]


X = df.iloc[:, 5:14]
Z = df.iloc[:, 5:11]
y = df.iloc[:,-3:]

rapm_test = df.iloc[:, 14:15]
orapm_test = df.iloc[:, 15:16]
drapm_test = df.iloc[:, 16:17]

plt.scatter(df[['rapm_pair']], df[['rapm_pair_test']])
plt.xlabel('2016-17 pairs')
plt.ylabel('2017-18 pairs')

#plt.show()

#X, y = make_regression(n_samples=1000, n_features=10, n_informative=5, n_targets=2, random_state=1, noise=0.5)


model = svm.SVR(kernel='linear')
model2 = svm.SVR(kernel='linear')
model3 = svm.SVR(kernel='linear')
model_master = svm.SVR()
model_master_weak = svm.SVR()

# model = LinearRegression()
# model2 = LinearRegression()
# model3 = LinearRegression()
# model_master = LinearRegression()
# model_master_weak = LinearRegression()

clf = RidgeCV(alphas=[1e-3, 1e-2, 1e-1, 1]).fit(X, rapm_test)
print(clf.score(X, rapm_test))
print(clf.coef_)


# model = RandomForestRegressor()
# model2 = RandomForestRegressor()
# model3 = RandomForestRegressor()
#model_master = RandomForestRegressor()
#model_master_weak = RandomForestRegressor()


# fit model
result = model.fit(tot, rapm_test)
result_off = model2.fit(off, orapm_test)
result_def = model3.fit(defe, drapm_test)
result_master = model_master.fit(X, rapm_test)
result_master_weak = model_master_weak.fit(Z, rapm_test)

print(result.score(tot, rapm_test))
print("ORAPM")
print(result_off.score(off, orapm_test))
print("DRAPM")
print(result_def.score(defe, drapm_test))
print(result_master.score(X, rapm_test))
print(result_master_weak.score(Z, rapm_test))

result = model.fit(tot2, rapm_test)
result2 = model2.fit(off2, orapm_test)
result3 = model3.fit(defe2, drapm_test)

print()
print(result.score(tot2, rapm_test))
print("ORAPM")
print(result2.score(off2, orapm_test))
print("DRAPM")
print(result3.score(defe2, drapm_test))


