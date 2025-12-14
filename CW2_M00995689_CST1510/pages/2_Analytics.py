import streamlit as st
import pandas as pd

st.set_page_config(page_title="Analytics", page_icon="📈", layout="wide")
st.title("📈 Analytics Page")

st.write("This is where you can add deeper analysis.")

# Example chart
df = pd.DataFrame({"x": [1,2,3,4], "y": [10,20,30,40]})
st.line_chart(df.set_index("x"))