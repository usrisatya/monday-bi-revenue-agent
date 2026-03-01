🚀 Revenue Intelligence Agent for Monday.com
Turn messy deal data into board-ready revenue insights.

This AI agent connects directly to Monday.com, cleans inconsistent business data, and transforms it into executive-grade revenue intelligence in minutes.

Overview

This project implements a production-ready AI-powered Business Intelligence Agent that integrates with Monday.com via live GraphQL API calls, processes inconsistent business data, and delivers executive-level revenue insights through both conversational AI and a real-time dashboard.

The system is designed to simulate founder-level decision support under real-world data constraints.

Key Capabilities

Live Monday.com GraphQL integration

Automated data cleaning and normalization

Probability-weighted revenue forecasting

Pipeline velocity and conversion analysis

Risk distribution modeling

LLM-powered tool-calling architecture

Executive dashboard (Streamlit)

Automatic fallback to demo dataset if API unavailable

System Architecture

Layered, modular design:

API Layer – Monday GraphQL client

Service Layer – Deals & Work Orders transformation

Business Logic Layer – Revenue intelligence engine

Agent Layer – LLM orchestration + tool registry

Presentation Layer – Executive Streamlit dashboard

This separation ensures scalability, maintainability, and production readiness.

Revenue Intelligence Metrics

The agent computes:

Total pipeline value

Probability-weighted revenue

90-day forecast

Conversion rate

Pipeline velocity

Revenue by owner

Revenue by sector

Revenue by stage

Risk categorization

AI Tooling

Implements OpenAI function-calling tools:

fetch_deals

fetch_work_orders

conversion_analysis

The LLM interprets founder-level queries, selects tools dynamically, and produces structured executive summaries.

Setup
1. Environment
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
2. Environment Variables

Create .env:

OPENAI_API_KEY=your_key
MONDAY_API_KEY=your_key
DEALS_BOARD_ID=board_id
WORK_ORDERS_BOARD_ID=board_id
3. Run
streamlit run streamlit_app.py
Design Principles

Clean separation of concerns

Defensive data handling

Minimal assumptions

Scalable architecture

Board-ready output

Submission Includes

Live hosted dashboard

Monday board link

Decision Log (PDF)

Source code

This README
