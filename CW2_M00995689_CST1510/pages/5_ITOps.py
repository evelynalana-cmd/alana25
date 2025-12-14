import streamlit as st
import pandas as pd
from app.data.tickets import list_tickets   

st.set_page_config(page_title="IT Operations", page_icon="🛠️", layout="wide")

# Guard
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if not st.session_state.logged_in:
    st.error("You must be logged in to view this page.")
    if st.button("Go to login"):
        st.switch_page("Home.py")
    st.stop()

st.title("🛠️ IT Operations Dashboard")
st.success(f"Welcome {st.session_state.username}")

# Fetch tickets directly
tickets = list_tickets()

# Sidebar filters
with st.sidebar:
    st.header("Filters")
    status_filter = st.multiselect("Status", sorted(tickets["status"].dropna().unique().tolist()) if "status" in tickets.columns else [])
    priority_filter = st.multiselect("Priority", sorted(tickets["priority"].dropna().unique().tolist()) if "priority" in tickets.columns else [])

filtered = tickets.copy()
if status_filter and "status" in tickets.columns:
    filtered = filtered[filtered["status"].isin(status_filter)]
if priority_filter and "priority" in tickets.columns:
    filtered = filtered[filtered["priority"].isin(priority_filter)]

# KPIs
k1, k2, k3 = st.columns(3)
with k1:
    st.metric("Total tickets", len(filtered))
with k2:
    st.metric("Open", (filtered["status"] == "Open").sum() if "status" in filtered.columns else 0)
with k3:
    st.metric("Resolved", (filtered["status"] == "Resolved").sum() if "status" in filtered.columns else 0)

# Charts
cA, cB = st.columns(2)
with cA:
    st.subheader("Tickets by Priority")
    if "priority" in filtered.columns:
        st.bar_chart(filtered["priority"].value_counts())
    else:
        st.info("No 'priority' column.")
with cB:
    st.subheader("Tickets Created Over Time")
    if "created_date" in filtered.columns:
        by_created = filtered.groupby("created_date").size().reset_index(name="count")
        st.line_chart(by_created.set_index("created_date")["count"])
    else:
        st.info("No 'created_date' column.")

# Raw data
with st.expander("See raw data"):
    st.dataframe(filtered, use_container_width=True)