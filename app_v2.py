from click import option
import streamlit as st
import pandas as pd
import random
import math
import os.path
import numpy as np
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

if 'next' not in st.session_state:
  st.session_state['next'] = False
  
if 'predict' not in st.session_state:
  st.session_state['predict'] = False

def collect_game():
  res = st.multiselect("Choose your favorite game ", (st.session_state['games']))

  Select = st.button("Select")
  if Select:
    st.session_state['ans'] = res
    st.session_state['suggest'] = similiar[similiar['Ori_game'] == st.session_state['ans'][-1]]['Name']

  st.write("Similiar")
  st.write(st.session_state['suggest'])
  if len(st.session_state['ans']) >0:
    Next = st.button("Next")
    if Next: 
      st.session_state['ans'] = res
      st.session_state['next'] = Next
    
def collect_time():
  with st.form("my_form"):
    time = [None] * len(st.session_state['ans'])
    for i in range(len(st.session_state['ans'])):
      st.write(st.session_state['ans'][i])
      time[i] = st.slider("How much time you use to play in scores", max_value = 10.0, value = 5.0, step = 0.5, key = i)
      time[i] = random.uniform(time[i] -0.5, time[i] +0.5)
      
    submitted = st.form_submit_button("Submit")
    if submitted:
      st.session_state['time'] = time
      df = pd.read_csv("./Name_id.csv")
      for i in range(len(st.session_state['ans'])):
        st.session_state['ans'][i] = df[df['item_name'] == st.session_state['ans'][i]]['item_id'].unique()[0]
      st.session_state['predict'] = True

def predict():
  df_1 = pd.read_csv("./Df_1.csv")
  df_2 = pd.read_csv("./Df_2.csv")
  df = pd.concat([df_1, df_2])
  name = pd.read_csv("./Name_id.csv")
  ansAll = pd.read_csv('./ans0_51135.csv', index_col=0)
        
  new = pd.DataFrame()
  new['user_id'] = 'New player GG123'
  new['item_id'] = st.session_state['ans']
  new['playtime_scaled'] = st.session_state['time']
  new['user_id'] = 'New player GG123'
  
  ch = new
  
  for i in range(new.shape[0]):
    ch = pd.concat([ch, df[df['item_id'] == new.iloc[i]['item_id']]])
    
  encoded_df=ch.groupby(['user_id','item_id'])['playtime_scaled'].sum().unstack().reset_index().fillna(0).set_index('user_id')
    
  keep = pd.DataFrame(columns = {'Name', 'Val'})
  keep = keep[['Name', 'Val']]
  gn = list(ch['user_id'].unique())
  gn.remove('New player GG123')
  
  for i in gn:
    point1 = np.array(encoded_df[encoded_df.index == 'New player GG123'])
    point2 = np.array(encoded_df[encoded_df.index == i])
    keep.loc[keep.shape[0]] = [i,np.linalg.norm(point1 - point2)]
    
  similar = keep.sort_values(by ='Val', ascending = True).reset_index(drop =True).loc[0]['Name']
  
  ans_name = []
  
  for i in ansAll[ansAll['user_id'] == similar]['item_id'].unique():
    ans_name.append(name[name['item_id'] == i]['item_name'].unique()[0])
    
  st.write(ans_name)
    
if st.session_state['predict'] == False:
  if st.session_state['next'] == False:
    collect_game()
  else:
    collect_time()
else:
  predict()