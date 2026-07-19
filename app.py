import streamlit as st
import os
from agent import run_research
from report import create_pdf_report

st.set_page_config(
    page_title="Personal Research Agent",
    layout="centered"
)

st.title("Personal Research Agent")
st.caption("Enter any topic — get a full research report + downloadable PDF")

st.divider()

topic = st.text_input(
    "What do you want to research?",
    placeholder="e.g. IT jobs in 2026"
)

depth = st.selectbox(
    "Report Depth",
    ["Quick Summary", "Detailed Report"],
    index=1
)

if st.button("Start Research", type="primary", use_container_width=True):
    if not topic.strip():
        st.warning("Please enter a topic before starting.")
    else:
        with st.spinner("Searching the web and generating your report..."):
            if depth == "Quick Summary":
                full_topic = f"Give a quick 3-paragraph summary about: {topic}"
            else:
                full_topic = f"Research this topic thoroughly with detailed analysis: {topic}"
            report = run_research(full_topic)

        st.success("Research complete!")
        st.divider()

        st.subheader("Your Report")
        st.markdown(report)

        st.divider()

        with st.spinner("Generating PDF..."):
            pdf_file = create_pdf_report(topic, report)

        with open(pdf_file, "rb") as f:
            st.download_button(
                label="Download PDF Report",
                data=f,
                file_name=pdf_file,
                mime="application/pdf",
                use_container_width=True
            )

        os.remove(pdf_file)

st.divider()
st.caption("Built with LangChain · Gemini · Tavily · Streamlit")