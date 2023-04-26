
# coding: utf-8

# # Métodos não supervisionados - K-Means
# 
# **Contexto:** com a base de dados em mãos dados de perfis de clientes de cartão de crédito é interessante agrupálos de maneira a facilitar o desenho de estratégias focadas nesses clientes.
# 
# Para entender melhor o perfil de cada cliente, nesse projeto fiz uma clusterização com o método [K-Means](https://minerandodados.com.br/entenda-o-algoritmo-k-means/) e dizer qual é o perfil médio de dos clientes de cada cluster. 
# 
# Você pode ler informações sobre esse dataset nesse link do [Kaggle](https://www.kaggle.com/arjunbhasin2013/ccdata).
# 
# Esse trabalho passa pelas seguintes etapas:
# - Tratar os dados e observar as estatísticas descritivas e distribuições dos dados
# - Tratar outliers caso necessário
# - Fazer uma transformação para standarizar os dados
# - Fazer o KMEANS e utilizar o método do cotovelo para definir o número de clusters
# - Através de boxplots, entender quais os perfis dos clusters e tentar caracterizar os clusters
# 

# In[ ]:


#aqui tem as bibliotecas que vamos utilizar

import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
sns.set(rc={'figure.figsize':(11.7,8.27)}) # isso é pras figuras ficarem maiores


# ## 1) Importação dos dados
# 
# importantdo os dados do data set do kaggle

# In[ ]:


from google.colab import files
uploaded = files.upload()


# In[ ]:


import io
df = pd.read_csv(io.BytesIO(uploaded['CC GENERAL.csv']))


# In[ ]:


df.drop(['CUST_ID'], axis=1, inplace=True) # aqui vamos retirar essa coluna porque ela só diz o ID do usuário


# ## 2) Tratamento, estatísticas descritivas e visualização dos dados

# In[ ]:


df.describe() #estatisticas descritivas 


# In[ ]:


df.isna().sum() #aqui estamos vendo se o quanto de valores vazios temos no dataset


# In[ ]:


df.dropna(inplace=True) # como a soma dos valores vazios no dataset é de menos que 4%, só deletamos essas linhas


# ### 2.1) Histograma dos dados
# 
# 

# In[ ]:


sns.histplot(x="BALANCE", data=df)


# In[ ]:


sns.histplot(x="BALANCE_FREQUENCY", data=df)


# In[ ]:


sns.histplot(x="PURCHASES", data=df)
#purchases<2000


# In[ ]:


sns.histplot(x='ONEOFF_PURCHASES', data=df)
#ONEOFF_PURCHASES<1000


# In[ ]:


sns.histplot(x='INSTALLMENTS_PURCHASES', data=df)
#INSTALLMENTS_PURCHASES<1000


# In[ ]:


sns.histplot(x='CASH_ADVANCE', data=df)


# In[ ]:


sns.histplot(x='PURCHASES_FREQUENCY', data=df)


# In[ ]:


sns.histplot(x='ONEOFF_PURCHASES_FREQUENCY', data=df)


# In[ ]:


sns.histplot(x='PURCHASES_INSTALLMENTS_FREQUENCY', data=df)


# In[ ]:


sns.histplot(x='CASH_ADVANCE_FREQUENCY', data=df)


# In[ ]:


sns.histplot(x='CASH_ADVANCE_TRX', data=df)


# In[ ]:


sns.histplot(x='PURCHASES_TRX', data=df)


# In[ ]:


sns.histplot(x='CREDIT_LIMIT', data=df)


# In[ ]:


sns.histplot(x='PAYMENTS', data=df)


# In[ ]:


sns.histplot(x='MINIMUM_PAYMENTS', data=df)


# In[ ]:


sns.histplot(x='PRC_FULL_PAYMENT', data=df)


# In[ ]:


sns.histplot(x='TENURE', data=df)


# ### 2.2) Matriz de correlação

# In[ ]:


sns.heatmap(df.corr(), annot=True,cmap='BrBG')


# ### 2.3) Tratamento de outliers

# O critério que utilizaremos será selecionar somente até o percentil 95 dos dados de algumas colunas.

# In[ ]:


df1=df[df['BALANCE'] < df['BALANCE'].quantile(.95)]
df1=df1[df1['PURCHASES'] < df['PURCHASES'].quantile(.95)]
df1=df1[df1['ONEOFF_PURCHASES'] < df['ONEOFF_PURCHASES'].quantile(.95)]
df1=df1[df1['INSTALLMENTS_PURCHASES'] < df['INSTALLMENTS_PURCHASES'].quantile(.95)]
df1=df1[df1['CASH_ADVANCE'] < df['CASH_ADVANCE'].quantile(.95)]
df1=df1[df1['PAYMENTS'] < df['PAYMENTS'].quantile(.95)]
df1=df1[df1['CREDIT_LIMIT'] < df['CREDIT_LIMIT'].quantile(.95)]
df1=df1[df1['MINIMUM_PAYMENTS'] < df['MINIMUM_PAYMENTS'].quantile(.95)]
df1=df1[df1['PURCHASES_TRX'] < df['PURCHASES_TRX'].quantile(.95)]
df1=df1[df1['CASH_ADVANCE_TRX'] < df['CASH_ADVANCE_TRX'].quantile(.95)]


# In[ ]:


df1.describe() # aqui vemos que o dataset sem outlier ficou com 72% do tamanho original


# ### 2.4) Standarização dos dados

# In[ ]:


scaler = StandardScaler()
normalized_df = scaler.fit_transform(df1)


# ### 2.5) Método do cotovelo para seleção do número de clusters

# In[ ]:


inertias = []
K = range(1, 10)
from scipy.spatial.distance import cdist
for k in K:
    # Building and fitting the model
    kmeanModel = KMeans(n_clusters=k).fit(normalized_df)
    inertias.append(kmeanModel.inertia_)


# In[ ]:


plt.plot(K, inertias, 'bx-')
plt.xlabel('Numero de clusteres')
plt.ylabel('Inercia')
plt.title('Método da inercia')
plt.show()


# Aqui vamos escolher o numero de 4 clusters

# In[ ]:


model = KMeans(4,random_state=42) #aqui treinamos o modelo
labels = model.fit_predict(normalized_df) #lembre-se de treinar com os dados normalizados


# In[ ]:


df1['clusters']=labels # aqui vamos atribuir pra cada cliente o seu devido cluster
df1['clusters']=df1['clusters'].astype(str)


# ## 3) Análise dos clusteres
# 
# 

# In[ ]:


sns.boxplot(x="clusters", y="PAYMENTS", data=df1)


# In[ ]:


sns.boxplot(x="clusters", y="MINIMUM_PAYMENTS", data=df1)


# In[ ]:


sns.boxplot(x="clusters", y="PRC_FULL_PAYMENT", data=df1)


# In[ ]:


sns.boxplot(x="clusters", y="BALANCE", data=df1)


# In[ ]:


sns.boxplot(x="clusters", y="PURCHASES", data=df1)


# In[ ]:


sns.boxplot(x="clusters", y="INSTALLMENTS_PURCHASES", data=df1)


# In[ ]:


sns.boxplot(x="clusters", y="ONEOFF_PURCHASES", data=df1)


# In[ ]:


sns.boxplot(x="clusters", y="CASH_ADVANCE", data=df1)


# In[ ]:


sns.boxplot(x="clusters", y="CASH_ADVANCE_FREQUENCY", data=df1)


# In[ ]:


sns.boxplot(x="clusters", y="CASH_ADVANCE_TRX", data=df1)


# In[ ]:


sns.boxplot(x="clusters", y="PURCHASES_TRX", data=df1)


# In[ ]:


sns.boxplot(x="clusters", y="CREDIT_LIMIT", data=df1)


# ## 4) Conclusão

# Ao analisar os clusters e as descrições de cada variável, identificamos diferenças entre as populações em algumas variáveis, o que nos permite criar 4 perfis distintos. É importante observar que há presença de outliers quando comparamos entre os clusters.
# 
# Os 4 perfis identificados são:
# 
# Cliente Contido (Cluster 0): Não realiza compras em grandes valores, quantidades ou pagamento antecipado.
# 
# Cliente Comprador (Cluster 1): Realiza compras em grandes valores e quantidades, porém não realiza pagamento antecipado.
# 
# Cliente em Ascensão (Cluster 2): Está começando a aumentar suas compras, porém ainda realiza compras em quantidades normais e não realiza pagamento antecipado.
# 
# Cliente Não Devedor (Cluster 3): Similar ao Cliente Contido, porém realiza pagamento antecipado em todas as suas compras.
# 
# Essa descrição é útil em áreas não técnicas, como atendimento ao cliente, marketing, vendas e financeiro, pois fornece detalhes relevantes sobre a população que podem ser úteis para o negócio, sem a necessidade de analisar todas as contas individualmente