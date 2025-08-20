import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Title
st.title("📊 Supermarket Sales Data Analysis")

# Upload CSV or load local file
df = pd.read_csv("SuperMarket Analysis.csv")
st.write("### Dataset Preview", df.head())

# Sidebar filters
city = st.sidebar.selectbox("Select City", df["City"].unique())
branch = st.sidebar.selectbox("Select Branch", df["Branch"].unique())

filtered = df[(df["City"] == city) & (df["Branch"] == branch)]
st.write("### Filtered Data", filtered.head())

# Example plot
fig, ax = plt.subplots()
sns.barplot(x="Product line", y="Total", data=filtered, estimator=sum, ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

# KPIs
st.metric("Average Total Sales", f"${filtered['Total'].mean():.2f}")
st.metric("Max Sales", f"${filtered['Total'].max():.2f}")
