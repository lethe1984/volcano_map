import streamlit as st
import pandas as pd
import numpy as np
import requests
import json

st.set_page_config(page_title="Volcano map",layout="wide")

url = "https://volcanoes.usgs.gov/hans-public/api/volcano/getElevatedVolcanoes"
response = requests.get(url)

vol_map_index = []

#Progess Bar
progress_text = "Getting volcano data..."
my_bar = st.progress(0, text=progress_text)

if response.status_code == 200:
    data = response.json()
    bar_step = int(100/len(data))
    progress = 0
    for volcano in data:
        progress=progress+bar_step
        my_bar.progress(progress, text=progress_text)
        resp_data = requests.get("https://volcanoes.usgs.gov/hans-public/api/volcano/getVolcano/"+volcano["vnum"])
        vol_data = resp_data.json()
        print(vol_data)
        vol_map_index.append(vol_data)
else:
    print(f"Error: {response.status_code}")

my_bar.empty()

#print(vol_map_index)

df = pd.DataFrame.from_dict(vol_map_index)

st.title("Active Volcano Map")

st.map(df, size=60000, zoom=1)

for vol in vol_map_index:
    with st.expander(vol["volcano_name"]):
        st.write("Region: " + vol["region"])
        st.write("Elevation [m]: " + str(vol["elevation_meters"]))
        st.write("Thread: " + vol["nvews_threat"])
        if vol["volcano_image_url"]:
            st.image(vol["volcano_image_url"])
