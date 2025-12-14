import streamlit as st
import pandas as pd
from app.services.dataset_service import list_datasets
  

st.set_page_config(page_title="Data Science", page_icon="🧪", layout="wide")

# Guard: block unauthorized access
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if not st.session_state.logged_in:
    st.error("You must be logged in to view this page.")
    if st.button("Go to login"):
        st.switch_page("Home.py")
    st.stop() 

st.title("🧪 Data Science Dashboard")
st.success(f"Welcome {st.session_state.username}")

# Fetch datasets directly
datasets = list_datasets()

# Sidebar filters
with st.sidebar:
    st.header("Filters")
    source_filter = st.multiselect("Source", sorted(datasets["department"].dropna().unique().tolist()) if "department" in datasets.columns else [])
    owner_filter = st.multiselect("Owner", sorted(datasets["owner"].dropna().unique().tolist()) if "owner" in datasets.columns else [])

filtered = datasets.copy()
if source_filter and "department" in datasets.columns:
    filtered = filtered[filtered["department"].isin(source_filter)]
if owner_filter and "owner" in datasets.columns:
    filtered = filtered[filtered["owner"].isin(owner_filter)]

# KPIs
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Total datasets", len(filtered))
with c2:
    st.metric("Avg size (MB)", round(filtered["size_mb"].mean() if "size_mb" in filtered.columns else 0, 2))
with c3:
    st.metric("Latest update", str(filtered["last_updated"].max()) if "last_updated" in filtered.columns and not filtered.empty else "N/A")

# Charts
colA, colB = st.columns(2)
with colA:
    st.subheader("Datasets by Department")
    if "department" in filtered.columns:
        st.bar_chart(filtered["department"].value_counts())
with colB:
    st.subheader("Dataset Growth Over Time")
    if "last_updated" in filtered.columns:
        by_date = filtered.groupby("last_updated").size().reset_index(name="count")
        st.line_chart(by_date.set_index("last_updated")["count"])
    else:
        st.info("No 'last_updated' column.")

# Raw data
with st.expander("See raw data"):
    st.dataframe(filtered, use_container_width=True)