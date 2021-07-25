import pandas as pd 
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt

df = pd.read_csv('/home/alvaro/Área de Trabalho/data visualization/data/feature_frame.csv')

y = df['y']
df.drop(columns=['y'], inplace=True)
X = df.copy()

scaler = StandardScaler()

X[['n_caracteristicas', 'metros', 'quartos', 'banheiros', 'vagas','descricao']] = scaler.fit_transform(X[['n_caracteristicas', 'metros', 'quartos', 'banheiros', 'vagas','descricao']])

# X = pd.get_dummies(X)

X['endereco'] = LabelEncoder().fit_transform(X['endereco'])

reg = LinearRegression().fit(X, y)
reg.score(X, y)
pred_reg = reg.predict(X)

coef = reg.coef_

error = mean_squared_error(reg.predict(X), y, squared=False)

clf = RandomForestClassifier(max_depth=400, random_state=0)
clf.fit(X, y)

predictions = clf.predict(X)
error2 = mean_squared_error(clf.predict(X), y, squared=False)
clf.score(X, y)


def plot_cost_by_district():
    top_district = list(df['endereco'].value_counts()[0:10].index)  
    mean_cost = []
    
    for add in top_district:
        y_values = df[df['endereco'] == add]['y']
        mean_cost.append(sum(y_values) / len(y_values))
        
    plt.bar(top_district, mean_cost)
            
plot_cost_by_district()
      
def plot_feature_imp():
    result_dict = {}    
    
    for i, col in enumerate(X.columns):
        result_dict[col] = clf.feature_importances_[i]
    
    order_dict = {k: v for k, v in sorted(result_dict.items(), key=lambda item: item[1], reverse=False)}
    
    plt.barh(list(order_dict.keys()), order_dict.values())


def get_reg_plot(predictions, y):
    plt.figure(figsize=(10,10))
    plt.scatter(y, predictions, c='crimson')
    plt.yscale('log')
    plt.xscale('log')

    p1 = max(max(predictions), max(y))
    p2 = min(min(predictions), min(y))
    plt.plot([p1, p2], [p1, p2], 'b-')
    plt.xlabel('Valor real', fontsize=15)
    plt.ylabel('Valor previsto', fontsize=15)
    plt.axis('equal')
    plt.show()

get_reg_plot(predictions, y)
get_reg_plot(pred_reg, y)
