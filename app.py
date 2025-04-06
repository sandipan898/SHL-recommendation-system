import streamlit as st
from utils.search import SemanticSearch
import pandas as pd

import shutil
# shutil.rmtree('~/.cache/torch')
# shutil.rmtree('~/.cache/huggingface')

# Setup
st.set_page_config(page_title="SHL Assessment Search", layout="wide")
st.title("🔍 SHL Assessment Semantic Search")

# Load search engine
search_engine = SemanticSearch()
search_engine.load_data("data/shl_assessments.csv")

# Input
query = st.text_input("Enter your search query:", placeholder="e.g. logical reasoning test for recruitment")

# Display results
if query:
    results = search_engine.query(query, top_k=10)
    
    print(results.columns)

    st.subheader("Top Matches")
    for i, row in results.iterrows():
        st.markdown(f"### [{row['Title']}]({row['Link']})")
        st.write(row['Description'])
        st.markdown(f"Score: `{row['score']:.2f}`")
        st.markdown("---")
