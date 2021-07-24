import pandas as pd 
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from nltk.metrics.distance  import edit_distance
import re
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt


y = df['y']
df.drop(columns=['y'], inplace=True)
X = df.copy()

scaler = StandardScaler()

X[['n_caracteristicas', 'metros', 'quartos', 'banheiros', 'vagas','descricao']] = scaler.fit_transform(X[['n_caracteristicas', 'metros', 'quartos', 'banheiros', 'vagas','descricao']])

X = pd.get_dummies(X)

# X['endereco'] = LabelEncoder().fit_transform(X['endereco'])

reg = LinearRegression().fit(X, y)
reg.score(X, y)
pred_reg = reg.predict(X)

coef = reg.coef_

error = mean_squared_error(reg.predict(X), y)

clf = RandomForestClassifier(max_depth=400, random_state=0)
clf.fit(X, y)

predictions = clf.predict(X)
error2 = mean_squared_error(clf.predict(X), y)
clf.score(X, y)

plt.barh(X.columns, clf.feature_importances_)


plt.figure(figsize=(10,10))
plt.scatter(y, pred_reg, c='crimson')
plt.yscale('log')
plt.xscale('log')

p1 = max(max(pred_reg), max(y))
p2 = min(min(pred_reg), min(y))
plt.plot([p1, p2], [p1, p2], 'b-')
plt.xlabel('True Values', fontsize=15)
plt.ylabel('Predictions', fontsize=15)
plt.axis('equal')
plt.show()
