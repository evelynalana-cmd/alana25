import streamlit as st
import pandas as pd
from app.data.db import connect_database
from app.data.incidents import get_all_incidents

# Page setup
st.set_page_config(page_title="Cybersecurity Dashboard", page_icon="🔒", layout="wide")

# Guard: block unauthorized access
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

if not st.session_state.logged_in:
    st.error("You must be logged in to view this page.")
    if st.button("Go to login page"):
        st.switch_page("Home.py")
    st.stop()

# Welcome message
st.title("🔒 Cybersecurity Dashboard")
st.success(f"Welcome, {st.session_state.username}!")

# Connect to database
conn = connect_database("DATA/intelligence_platform.db")
incidents = get_all_incidents(conn)

# Sidebar filters
with st.sidebar:
    st.header("Filters")
    severity_filter = st.multiselect("Severity", ["Low","Medium","High","Critical"], default=["High","Critical"])
    status_filter = st.multiselect("Status", ["Open","In Progress","Resolved"], default=["Open","In Progress"])

# Apply filters
filtered = incidents[
    incidents["severity"].isin(severity_filter) &
    incidents["status"].isin(status_filter)
]

# KPIs
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Incidents", len(filtered))
with col2:
    st.metric("Open Cases", (filtered["status"]=="Open").sum())
with col3:
    st.metric("Resolved Cases", (filtered["status"]=="Resolved").sum())

# Charts
colA, colB = st.columns(2)
with colA:
    st.subheader("Incidents by Severity")
    st.bar_chart(filtered["severity"].value_counts())

with colB:
    st.subheader("Incidents Over Time")
    if "date" in filtered.columns:
        by_date = filtered.groupby("date").size().reset_index(name="count")
        st.line_chart(by_date.set_index("date")["count"])
    else:
        st.info("No 'date' column found in incidents data.")

# Raw data expander
with st.expander("See filtered data"):
    st.dataframe(filtered, use_container_width=True)

# Logout
st.divider()
if st.button("Log out"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.info("You have been logged out.")
    st.switch_page("Home.py")