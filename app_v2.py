from click import option
import streamlit as st
import pandas as pd
import random
import math
import os.path
import numpy as np
from scipy.spatial import distance
from traitlets import default

similiar = pd.read_csv('./Sim_game.csv')

st.header("Game Recommendation")

if 'suggest' not in st.session_state:
  st.session_state['suggest'] = pd.DataFrame()

if 'ans' not in st.session_state:
  st.session_state['ans'] = []
  
if 'games' not in st.session_state:
  df = pd.read_csv("./Name_id.csv")
  st.session_state['games'] = list(df['item_name'].sort_values().unique())
  
if 'time' not in st.session_state:
  st.session_state['time'] = []
  
if 'predict' not in st.session_state:
  st.session_state['predict'] = False

def collect_data():
  res = st.multiselect("Choose your favorite game ", (st.session_state['games']))

  time = st.slider("How much time you use to play in scores", max_value = 10.0, value = 5.0, step = 0.5)

  Next = st.button("Next")
  if Next:
    st.session_state['ans'] = res
    st.session_state['time'].append(random.uniform(time-0.5, time+0.5))
    st.session_state['suggest'] = similiar[similiar['Ori_game'] == st.session_state['ans'][-1]]['Name']

  st.write("Similiar")
  st.write(st.session_state['suggest'])
  Submit = st.button("Submit")
  if Submit:
    st.session_state['predict'] = True
    st.button("Go !!!")

# def predict():
#   df = pd.read_csv("./Scaled_data_without_0.csv")
#   table = pd.read_csv('./Encoded_df_with_newplay.csv', index_col = 0)
#   ansAll = pd.read_csv('./ans0_51135.csv', index_col=0)

#   for i in range(len(st.session_state['ans'])):
#     st.session_state['ans'][i] = df[df['item_name'] == st.session_state['ans'][i]]['item_id'].unique()[0]
        
#   new = pd.DataFrame()
#   new['user_id'] = 'New player GG123'
#   new['item_id'] = st.session_state['ans']
#   new['playtime_scaled'] = st.session_state['time']
#   new['user_id'] = 'New player" GG123'
  

#   keep = pd.DataFrame(columns=['A', 'B'])
#   ch = pd.DataFrame()

#   for i in range(new.shape[0]):
#       table.loc['New player GG123',new.iloc[i]['item_id']] = new.iloc[i]['playtime_scaled']
#       ch = pd.concat([ch, df[df['item_id'] == new.iloc[i]['item_id']]])
#   table = table.fillna(0)

#   for i in ch['user_id'].unique():
#     if (table[table.index == i].empty == False):
#       keep.loc[keep.shape[0]] = [i,distance.euclidean(table[table.index == 'New player GG123'], table[table.index == i])]

#   similiar_user = keep.sort_values(by ='B', ascending = False).iloc[0]['A']
    
#   ans_name = []
  
#   for i in ansAll[ansAll['user_id'] == similiar_user]['item_id'].unique():
#     ans_name.append(df[df['item_id'] == i]['item_name'].unique()[0])
    
#   st.write(ans_name)
    
if st.session_state['predict'] == False:
  collect_data()
else:
  predict()