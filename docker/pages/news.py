import streamlit as st
import plotly.express as px
from utils import *
from configuration import *
import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import numpy as np

st.title("Data Analytics")

# Read from the bucket
bucket = get_bucket()
df = get_df(bucket, "news")

# Authors Plot
fig = px.bar(df, x='author')
st.subheader('Authors Plot')
st.plotly_chart(fig)

# Most Cited Symbols/Companies Plot
st.subheader('Most Cited Symbols')
join_df = np.array([i for i in df['symbols']])
join_df = np.concatenate(join_df).ravel()
fig = px.bar(join_df)
fig.update_layout(showlegend=False)
st.plotly_chart(fig)

# Most Frequent Words Plot
st.subheader('Most Frequent Words')
text = " ".join(i for i in df['summary'])
STOPWORDS = ["S"] + list(STOPWORDS)
stopwords = set(STOPWORDS)
wordcloud = WordCloud(stopwords=stopwords, background_color="black").generate(text)
print(text)
plt.figure(figsize=(15,10))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
st.set_option('deprecation.showPyplotGlobalUse', False)
st.pyplot()
