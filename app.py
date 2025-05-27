# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pynsee.download import download_file
from utils.llm_utils import parse_prompt

st.set_page_config(page_title="INSEE Data Plotter", layout="wide")
st.title("📈 INSEE Data Plot from Natural Language Prompt")

prompt = st.text_input("Enter your question:", "Show inflation trend in France since 2000")

if st.button("Generate Plot"):
    with st.spinner("Interpreting your prompt..."):
        parsed = parse_prompt(prompt)

    if "error" in parsed:
        st.error(f"LLM parsing failed: {parsed['error']}")
    else:
        st.json(parsed)
        indicator = parsed.get("indicator", "").upper()
        region = parsed.get("region", "France")
        start_year = int(parsed.get("start_year", 2000))

        try:
            st.info(f"Fetching INSEE data for {indicator} in {region} since {start_year}...")

            # This example assumes indicator is CPI for simplicity
            df = download_file("IPC-2015")
            df = df[df['DATE'] >= f"{start_year}-01"]

            # Optional filter depending on structure
            # df = df[df['INDICATOR'].str.contains(indicator)]

            st.success("Data loaded. Generating plot...")

            fig, ax = plt.subplots()
            df.plot(x='DATE', y='VALUE', ax=ax)
            ax.set_title(f"{indicator} in {region} since {start_year}")
            st.pyplot(fig)

        except Exception as e:
            st.error(f"Error fetching or plotting data: {e}")
