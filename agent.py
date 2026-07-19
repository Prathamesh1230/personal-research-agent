import os
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch
from langgraph.prebuilt import create_react_agent

load_dotenv()

def get_api_keys():
    try:
        gemini_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))
        tavily_key = st.secrets.get("TAVILY_API_KEY", os.getenv("TAVILY_API_KEY"))
    except Exception:
        gemini_key = os.getenv("GEMINI_API_KEY")
        tavily_key = os.getenv("TAVILY_API_KEY")
    return gemini_key, tavily_key


def create_research_agent():
    gemini_key, tavily_key = get_api_keys()

    llm = ChatGoogleGenerativeAI(
        model="gemini-3-flash-preview",
        google_api_key=gemini_key,
        temperature=0.3
    )

    search_tool = TavilySearch(
        max_results=5,
        tavily_api_key=tavily_key
    )

    agent = create_react_agent(
        model=llm,
        tools=[search_tool],
        prompt="""You are an expert research assistant. 
Research the given topic thoroughly using multiple searches.
Always search at least 3 times with different queries to get comprehensive information.
Then write a detailed report with these sections:
## Overview
## Key Findings  
## Detailed Analysis
## Latest Developments
## Conclusion
Include source URLs at the end."""
    )

    return agent


def run_research(topic):
    print(f"\n Researching: {topic}")
    print("=" * 50)

    agent = create_research_agent()

    result = agent.invoke({
        "messages": [{"role": "user", "content": f"Research this topic thoroughly: {topic}"}]
    })

    content = result["messages"][-1].content

    if isinstance(content, list):
        final_message = content[0]["text"]
    else:
        final_message = content

    return final_message


if __name__ == "__main__":
    from report import create_pdf_report

    topic = input("Enter a topic to research: ")
    report = run_research(topic)

    print("\n FINAL REPORT:")
    print("=" * 50)
    print(report)

    print("\n Saving PDF...")
    pdf_file = create_pdf_report(topic, report)
    print(f" Done! Your report is saved as: {pdf_file}")