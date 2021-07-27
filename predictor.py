import pandas as pd 
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

df = pd.read_csv('/home/alvaro/Área de Trabalho/data visualization/data/feature_frame.csv')

y = df['y']
X = df.iloc[:, 0:7]

scaler = StandardScaler()

X[['n_caracteristicas', 'metros', 'quartos', 'banheiros', 'vagas','descricao']] = scaler.fit_transform(X[['n_caracteristicas', 'metros', 'quartos', 'banheiros', 'vagas','descricao']])

# X = pd.get_dummies(X)

X['endereco'] = LabelEncoder().fit_transform(X['endereco'])

reg = LinearRegression().fit(X, y)
reg.score(X, y)
pred_reg = reg.predict(X)

error = mean_squared_error(pred_reg, y, squared=False)

clf = RandomForestClassifier(max_depth=400, random_state=0)
clf.fit(X, y)

predictions = clf.predict(X)
error2 = mean_squared_error(clf.predict(X), y, squared=False)
clf.score(X, y)


def plot_cost_by_district():
    top_district = list(df['endereco'].value_counts()[0:10].index)  
    result = {}
    
    for add in top_district:
        y_values = df[df['endereco'] == add]['y']
        result[add] = sum(y_values) / len(y_values)
    
    order_dict = {k: v for k, v in sorted(result.items(), key=lambda item: item[1], reverse=True)}
    fig = px.bar(x=order_dict.values(), y=list(order_dict.keys()), orientation='h', labels=dict(x="Valor médio do aluguel", y="Bairro"))
    html = fig.to_html('test.html')
    
    return html

def plot_house_pricing():
    fig = px.scatter(
        df, x="metros", y="y", log_x=True, log_y=True, color='promocao', color_discrete_sequence=['#adadad', '#3b6be3'])
    return fig.to_html()

def plot_house_status():
    fig = px.scatter(
        df, x="predictions", y="y", log_x=True, log_y=True, color='status', color_discrete_sequence=['#bcc0cc', '#e32b3e', '#04c943'])
    return fig.to_html()

def plot_feature_imp():
    result_dict = {}    
    
    for i, col in enumerate(X.columns):
        result_dict[col] = clf.feature_importances_[i]
    
    order_dict = {k: v for k, v in sorted(result_dict.items(), key=lambda item: item[1], reverse=True)}
    
    fig = px.bar(x=list(order_dict.keys()), y=order_dict.values(), labels=dict(x="Característica", y="Importância"))
    html = fig.to_html('test.html')
    return html
    
# df = df.drop([df.index[324] , df.index[1095], df.index[1481]])

df['promocao'] = ['Falso'] * len(df)

sum(df['metros']) / len(df['metros'])
sum(df['y']) / len(df['y'])

best_offer = df[(df['metros'] > (130*110) / 100) & (df['y'] < 2466)]

df.loc[(df['metros'] > (130*110) / 100 ) & (df['y'] < 2466), 'promocao'] = 'Verdadeiro'

status = []

for i, value in enumerate(df['y'].values):
    inc_value = (value*110) / 100
    if value == predictions[i]:
        status.append('Normal')
    elif inc_value < predictions[i]:
        status.append('Barato')
    else:
        print(value, predictions[i])
        status.append('Caro')
        
df['status'] = status
df['predictions'] = predictions

fig2 = go.Figure(go.Indicator(
    mode = "number",
    value = len(df),
    title = {"text": "Casas encontradas<br><span style='font-size:0.8em;color:gray'>Bauru - SP</span><br>"},
    # number = {'prefix': "CASAS ENCONTRADAS: "},
    domain = {'x': [0, 1], 'y': [0, 1]}))


# fig = go.Figure()

fig = make_subplots(rows=1, cols=2)

fig.add_trace(go.Indicator(
    mode = "number+delta",
    value = 200,
    domain = {'x': [0, 0.5], 'y': [0, 0.5]},
    delta = {'position' : "top"}))

fig.add_trace(go.Indicator(
    mode = "number+delta",
    value = 350,
    delta = {},
    domain = {'x': [0, 0.5], 'y': [0.5, 1]}))

fig.add_trace(go.Indicator(
    mode = "number+delta",
    value = len(df),
    title = {"text": "Casas encontradas<br><span style='font-size:0.8em;color:gray'>Bauru - SP</span><br>"},
    # number = {'prefix': "CASAS ENCONTRADAS: "},
    domain = {'x': [0, 1], 'y': [0, 1]}))

fig.update_layout(paper_bgcolor = "lightgray")

html_fig = fig.to_html()
html_fig1 = plot_feature_imp()
html_fig2 = plot_cost_by_district()
html_fig3 = plot_house_pricing()
html_fig4 = plot_house_status()

f = open('report.html','w')
f.write(html_fig)
f.write(html_fig1)
f.write(html_fig2)
f.write(html_fig3)
f.write(html_fig4)
f.close()

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
