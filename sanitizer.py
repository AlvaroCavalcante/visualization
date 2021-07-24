import pandas as pd
import ast
from unidecode import unidecode
import re
from nltk.metrics.distance  import edit_distance

df = pd.read_csv('./data/house_data.csv')

def get_similar_address():
    similar = []
    count = 0

    for add in df['endereco'].unique():
        count +=1
        print(count)
        for add2 in df['endereco'].unique():
            if add != add2:
                dist = edit_distance(add, add2)
                if dist <= 2:
                    similar.append((add, add2))

    return similar

df['iptu'] = df['iptu'].fillna('')
df['iptu'] = df['iptu'].map(lambda x: x.lstrip('R$'))

df['condominio'] = df['condominio'].fillna('')
df['condominio'] = df['condominio'].map(lambda x: x.lstrip('R$'))

df['iptu'] = df['iptu'].replace('', 0).astype(float)

df['condominio'] = df['condominio'].replace('Não informado', -1)
df['condominio'] = df['condominio'].replace('', 0).astype(float)

df['aluguel'] = df['aluguel'].fillna('-1')
df['aluguel'] = df['aluguel'].map(lambda x: x.lstrip(' R$').rstrip('/mês').replace('.', '')).astype(float)

df['endereco'] = df['endereco'].str.upper()
df['endereco'] = df['endereco'].map(lambda x: x.replace('SP', '').replace('BAURU', ''))
df['endereco'] = df['endereco'].map(lambda x: unidecode(x))

new_add = []
for add in df['endereco']:
    if 'RUA' in add.split(' ') or 'AVENIDA' in add.split(' '):
        divide_ind = add.index('-')
        add = add[divide_ind+1:]

    new_add.append(add.replace(',', '').replace('-', '').lstrip(' ').rstrip(' '))

len_features = []
m_squared = []
rooms = []
bath = []
car_space = []

for f in df['features']:
    f = ast.literal_eval(f)
    len_features.append(len(f))
    
    if ''.join(list(f[0])[len(f[0])-2:]) == 'm²':
        m_squared.append(int(f[0].split('m²')[0]))
    else:
        m_squared.append(-1)
      
    if f[1].split(' ')[-1] in ['quartos', 'quarto']:
        rooms.append(int(f[1].split(' ')[0]))
    else:
        rooms.append(-1)
        
    if f[2].split(' ')[-1] in ['banheiro', 'banheiros', 'suíte', 'suítes']:
        bath.append(int(f[2].split(' ')[0]))
    else:
        bath.append(-1)
        
    if f[3].split(' ')[-1] in ['vagas', 'vaga']:
        car_space.append(int(f[3].split(' ')[0]))
    else:
        car_space.append(-1)
        
data = {
        'n_caracteristicas': len_features,
        'metros': m_squared,
        'quartos': rooms,
        'banheiros': bath,
        'vagas': car_space,
        'descricao': df['description_len'].values,
        'endereco': new_add,
        'y': df['aluguel'].values
        }

feature_frame = pd.DataFrame(data)

feature_frame['endereco'] = feature_frame['endereco'].fillna('')
feature_frame['endereco'] = feature_frame['endereco'].map(lambda x: re.sub("[0-9]+", "", x).lstrip(' '))

feature_frame['endereco'] = feature_frame['endereco'].replace('VILA CORALINA', 'VILA CAROLINA')

feature_frame.to_csv('data/feature_frame.csv', index=False)