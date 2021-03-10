import json
import urllib.request

import pandas as pd
import streamlit as st
import plotly.express as px


@st.cache(allow_output_mutation=True)
def get_data_from_api():
    api_url = 'https://api.sne.space/catalog?ra=21:23:32.16&dec=-53:01:36.08&radius=300'

    response = urllib.request.urlopen(api_url)
    response_content = json.loads(response.read())
    data = pd.DataFrame.from_dict(response_content, orient='index').reset_index(drop=True)
    data = data[['name', 'catalog', 'ra', 'dec', 'discoverdate', 'lumdist', 'redshift']]
    data['name'] = data.name.apply(lambda x: x[0])
    data['catalog'] = data.catalog.apply(lambda x: x[0])
    data['ra'] = data.ra.apply(lambda x: x[0].get('value'))
    data['dec'] = data.dec.apply(lambda x: x[0].get('value'))
    return data


st.title('超新星資料')

data_load_state = st.text('正在讀取API資料...')
data = get_data_from_api()

if not data.empty:
    data_load_state.text('資料讀取完成(使用快取)!')

    if st.checkbox('顯示事件原始資料欄位'):
        st.dataframe(data)

    st.sidebar.subheader('單一超新星選擇')
    selected_name = st.sidebar.selectbox('請選擇超新星名稱:', data.name)
    data[data.name == selected_name].iloc[0]
