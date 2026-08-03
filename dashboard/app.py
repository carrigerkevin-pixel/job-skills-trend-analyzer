import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "pipeline"))

import streamlit as st
import pandas as pd
from analysis import top_skills_overall

st.set_page_config(page_title="Job Skills Trend Analyzer", layout="wide")

st.title("📊 Job Skills Trend Analyzer")
st.write("Discover which skills are most in-demand across tech job postings.")

st.header("Top Skills Overall")

skills_data = top_skills_overall(limit=10)

# Convert the list of dicts into a pandas DataFrame — the format charts expect
df = pd.DataFrame(skills_data)
df = df.set_index("skill")  # use skill names as the x-axis labels

st.bar_chart(df)