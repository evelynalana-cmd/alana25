import streamlit as st
import pandas as pd
from app.services.incident_service import (
    get_all_incidents, insert_incident, update_incident_status, delete_incident
)

st.set_page_config(page_title="Cyber Incidents", page_icon="⚠️", layout="wide")

# Guard: only logged-in users
if not st.session_state.get("logged_in", False):
    st.error("You must be logged in to view this page.")
    if st.button("Go to login page"):
        st.switch_page("Home.py")
    st.stop()

st.title("⚠️ Cyber Incidents Dashboard")
st.caption(f"Logged in as {st.session_state.username} ({st.session_state.role})")

with st.sidebar:
    st.header("Filters")
    severity_filter = st.selectbox("Severity", ["All", "Low", "Medium", "High"])
    status_filter  = st.selectbox("Status", ["All", "Open", "Resolved", "Closed"])

    df = pd.DataFrame(get_all_incidents(),
    columns=["id","date","incident_type","severity","status","description","reported_by"]
)

if severity_filter != "All":
    df = df[df["severity"] == severity_filter]
if status_filter != "All":
    df = df[df["status"] == status_filter]

st.caption(f"Showing {len(df)} incidents")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Incidents by Severity")
    if not df.empty:
        st.bar_chart(df["severity"].value_counts())
    else:
        st.info("No data for selected filters.")

with col2:
    st.subheader("Incidents by Status")
    if not df.empty:
        st.bar_chart(df["status"].value_counts())
    else:
        st.info("No data for selected filters.")

with st.expander("See raw data"):
    st.dataframe(df, use_container_width=True)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download filtered CSV", csv, file_name="incidents_filtered.csv", mime="text/csv")

    st.divider()
st.header("Manage Incidents")

# Add incident
with st.form("add_incident"):
    st.subheader("Add Incident")
    date = st.date_input("Date")
    incident_type = st.text_input("Incident Type")
    severity = st.selectbox("Severity", ["Low", "Medium", "High"])
    status = st.selectbox("Status", ["Open", "Resolved", "Closed"])
    description = st.text_area("Description")
    reported_by = st.text_input("Reported By")
    submitted = st.form_submit_button("Add Incident")
    if submitted:
        insert_incident(date, incident_type, severity, status, description, reported_by)
        st.success("Incident added. Refresh filters if needed.")

# Admin-only actions
if st.session_state.get("role") == "admin":
    st.subheader("Admin actions")
    incident_id = st.number_input("Incident ID", min_value=1, step=1)
    new_status = st.selectbox("New Status", ["Open","Resolved","Closed"])
    colA, colB = st.columns(2)
    with colA:
        if st.button("Update Status"):
            update_incident_status(incident_id, new_status)
            st.success("Incident updated.")
    with colB:
        if st.button("Delete Incident"):
            delete_incident(incident_id)
            st.warning("Incident deleted.")
else:
    st.info("Admin-only actions are hidden for your role.")