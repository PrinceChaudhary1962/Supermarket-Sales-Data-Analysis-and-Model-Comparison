import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import re
import difflib
import traceback

st.set_page_config(layout="wide")
st.title("📊 Supermarket Sales Data Analysis — Robust Plotting")

# -----------------------
# Helper functions
# -----------------------
def normalize_colname(col):
    # strip BOM, whitespace, newlines, lower-case for matching but keep original for display
    col = col.replace('\ufeff', '')
    col = col.strip()
    col = re.sub(r'\s+', ' ', col)   # collapse multi-space/newline
    return col

def find_best_match(col_candidates, cols):
    """Return the first exact (case-insensitive) match, or close fuzzy match, else None."""
    cols_lower = {c.lower(): c for c in cols}
    for cand in col_candidates:
        if cand.lower() in cols_lower:
            return cols_lower[cand.lower()]
    # fuzzy: find best single match using difflib
    all_cols = list(cols)
    all_cols_lower = [c.lower() for c in all_cols]
    for cand in col_candidates:
        matches = difflib.get_close_matches(cand.lower(), all_cols_lower, n=1, cutoff=0.7)
        if matches:
            # return original cased column name
            matched_lower = matches[0]
            idx = all_cols_lower.index(matched_lower)
            return all_cols[idx]
    return None

# -----------------------
# Load data
# -----------------------
@st.cache_data
def load_and_prepare(path="SuperMarket Analysis.csv"):
    df = pd.read_csv(path)
    # Normalize column names in-place but keep original mapping
    orig_cols = list(df.columns)
    cleaned_cols = [normalize_colname(c) for c in orig_cols]
    # apply cleaned names to dataframe
    df.columns = cleaned_cols

    # Some common column name candidates:
    product_candidates = [
        "product line", "product", "product_line", "productline", "product category",
        "product type", "product category name"
    ]
    total_candidates = [
        "total", "total sales", "total_sales", "amount", "total_price", "total amount",
        "grand total", "total sale", "total_bill"
    ]
    city_candidates = ["city", "branch city", "store city"]
    branch_candidates = ["branch", "store", "branch name", "store name"]

    prod_col = find_best_match(product_candidates, df.columns)
    total_col = find_best_match(total_candidates, df.columns)
    city_col = find_best_match(city_candidates, df.columns)
    branch_col = find_best_match(branch_candidates, df.columns)

    return df, {"prod_col": prod_col, "total_col": total_col, "city_col": city_col, "branch_col": branch_col}

try:
    df, cols_map = load_and_prepare("SuperMarket Analysis.csv")
except FileNotFoundError:
    st.error("File 'SuperMarket Analysis.csv' not found in repo root. Make sure the CSV is uploaded at the repo root.")
    st.stop()
except Exception as e:
    st.error(f"Error reading CSV: {e}")
    st.text(traceback.format_exc())
    st.stop()

# -----------------------
# Debug info: show columns & auto-detected columns
# -----------------------
st.subheader("Dataset columns & automatic mapping")
st.write("Detected columns (cleaned):", df.columns.tolist())
st.write("Auto-detected mapping:", cols_map)

# If essential columns not found, show guidance and stop
if cols_map["prod_col"] is None or cols_map["total_col"] is None:
    st.error("Could not automatically find 'Product line' or 'Total' columns in your dataset.")
    st.info("Try renaming your CSV headers to include columns like 'Product line' and 'Total' (or 'Total Sales').")
    st.stop()

# -----------------------
# Clean Total column to numeric
# -----------------------
total_col = cols_map["total_col"]
prod_col = cols_map["prod_col"]

# Convert total column to numeric safely
df[total_col] = df[total_col].astype(str).str.replace(r'[^\d.\-]', '', regex=True)  # remove $ , etc.
df[total_col] = pd.to_numeric(df[total_col], errors='coerce')

# Show type info
st.write("Column dtypes (after cleaning):")
st.write(df[[prod_col, total_col]].dtypes)

# -----------------------
# Sidebar filters (uses detected city/branch if available)
# -----------------------
city_col = cols_map["city_col"]
branch_col = cols_map["branch_col"]

if city_col and city_col in df.columns:
    df[city_col] = df[city_col].astype(str).str.strip()
    city = st.sidebar.selectbox("Select City", options=["All"] + sorted(df[city_col].dropna().unique().tolist()))
else:
    city = "All"

if branch_col and branch_col in df.columns:
    df[branch_col] = df[branch_col].astype(str).str.strip()
    branch = st.sidebar.selectbox("Select Branch", options=["All"] + sorted(df[branch_col].dropna().unique().tolist()))
else:
    branch = "All"

# -----------------------
# Apply filters
# -----------------------
filtered = df.copy()
if city != "All" and city_col:
    filtered = filtered[filtered[city_col] == city]
if branch != "All" and branch_col:
    filtered = filtered[filtered[branch_col] == branch]

st.write(f"Filtered data shape: {filtered.shape}")

# Guard: empty filtered
if filtered.empty:
    st.warning("No rows match the chosen filters. Try selecting 'All' or different filter values.")
    st.dataframe(df.head(10))
    st.stop()

# -----------------------
# Aggregation and plotting
# -----------------------
try:
    # Aggregate to ensure seaborn sees tidy data with numeric y-values
    agg = filtered.groupby(prod_col, as_index=False)[total_col].sum().sort_values(by=total_col, ascending=False)
    st.write("Aggregated values (top 10):")
    st.dataframe(agg.head(10))

    if agg.empty:
        st.warning("Aggregated data is empty after grouping. Check the Total column for numeric conversion issues.")
        st.stop()

    # Plot
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=agg, x=prod_col, y=total_col, ax=ax)
    ax.set_xlabel(prod_col)
    ax.set_ylabel("Sum of " + total_col)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig)

except Exception as e:
    st.error("Plotting failed. See debug info below.")
    st.text(f"Error: {e}")
    st.text(traceback.format_exc())
    st.write("Filtered sample (first 10 rows):")
    st.dataframe(filtered.head(10))
    st.write("Filtered dtypes:")
    st.write(filtered.dtypes)
    st.stop()
