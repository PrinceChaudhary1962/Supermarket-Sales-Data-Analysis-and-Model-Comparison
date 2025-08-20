import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("📊 Supermarket Sales Data Analysis")

# Load data
df = pd.read_csv("SuperMarket Analysis.csv")

# Clean column names
df.columns = df.columns.str.strip()

# Debug: show available columns
st.write("Columns:", df.columns.tolist())

# Sidebar filters
city = st.sidebar.selectbox("Select City", df["City"].unique())
branch = st.sidebar.selectbox("Select Branch", df["Branch"].unique())

filtered = df[(df["City"] == city) & (df["Branch"] == branch)]

# Plot
fig, ax = plt.subplots()
sns.barplot(x="Product line", y="Total", data=filtered, estimator=sum, ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)
