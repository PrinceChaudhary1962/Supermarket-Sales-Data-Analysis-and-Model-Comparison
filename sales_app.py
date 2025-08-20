import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("📊 Supermarket Sales Data Analysis")

# Load data
df = pd.read_csv("SuperMarket Analysis.csv")

# Clean column names
df.columns = df.columns.str.strip()

# Debug: show column names
st.write("Columns in dataset:", df.columns.tolist())

# Sidebar filters
city = st.sidebar.selectbox("Select City", df["City"].unique())
branch = st.sidebar.selectbox("Select Branch", df["Branch"].unique())

filtered = df[(df["City"] == city) & (df["Branch"] == branch)]

if filtered.empty:
    st.warning("⚠️ No data available for this filter. Try different options.")
else:
    # Plot sales by Product line
    fig, ax = plt.subplots()
    sns.barplot(x="Product line", y="Total", data=filtered, estimator=sum, ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)
