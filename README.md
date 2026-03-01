🚀 Monday.com Business Intelligence AI Agent

Production-ready AI-powered revenue intelligence agent that connects to Monday.com, cleans messy business data, performs executive-level analytics, and delivers founder-ready insights via dashboard + conversational AI.

🎯 Assignment Objective

Build a Business Intelligence AI Agent capable of:

Making LIVE Monday.com GraphQL API calls

Handling messy, inconsistent business data

Performing revenue intelligence analysis

Answering founder-level strategic queries

Delivering insights conversationally

Providing a live hosted prototype

🏗️ Architecture Overview

The system follows a clean, modular production architecture:

app/
│
├── api/                  → Monday GraphQL client + Query builder
├── services/             → Deals & Work Orders processing
├── utils/                → Data cleaning & normalization
├── agent/                → LLM orchestrator + Tool calling
├── schemas/              → Tool & response schemas
├── config/               → Settings & constants
├── main.py               → EnterpriseBIAgent core logic
│
streamlit_app.py          → Executive dashboard frontend
🧠 System Architecture Flow
User Query
     ↓
LLM (Function Calling)
     ↓
Tool Registry
     ↓
Deals / Work Orders Service
     ↓
Business Logic Layer
     ↓
Executive Summary
     ↓
Streamlit Dashboard
📊 Core Capabilities
1️⃣ Live Monday.com Integration

Uses GraphQL API

Pulls live board data

Handles API errors gracefully

Falls back to dummy dataset if API fails

2️⃣ Messy Data Handling

System automatically:

Cleans masked revenue fields

Normalizes sector names

Parses inconsistent date formats

Handles missing values

Converts probability labels → weighted scores

Example:

High → 0.8
Medium → 0.5
Low → 0.2
3️⃣ Revenue Intelligence Engine

Implements:

Total pipeline value

Probability-weighted revenue

90-day revenue forecast

Conversion rate

Pipeline velocity

Risk distribution analysis

Revenue by owner

Revenue by sector

Revenue by stage

4️⃣ AI Tooling Layer

OpenAI function-calling tools:

fetch_deals

fetch_work_orders

conversion_analysis

LLM selects tool → tool executes → business logic summarizes → executive response generated.

5️⃣ Executive Dashboard (Streamlit)

Includes:

KPI Overview Row

Conversion %

90-Day Forecast

Pipeline Velocity

Risk Distribution Chart

Revenue by Owner

Sector Contribution Pie Chart

Revenue by Stage

AI Insights Panel

Filter controls (Sector / Owner)

Live Data Source indicator

Board-meeting ready UI.

⚙️ Setup Instructions
1️⃣ Clone Repository
git clone <your-repo>
cd monday-bi-agent
2️⃣ Create Virtual Environment
python -m venv .venv
source .venv/bin/activate
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Create .env File
OPENAI_API_KEY=your_openai_key
MONDAY_API_KEY=your_monday_key
DEALS_BOARD_ID=your_deals_board_id
WORK_ORDERS_BOARD_ID=your_work_orders_board_id
5️⃣ Run Streamlit App
streamlit run streamlit_app.py
🔄 Fallback Behavior

If:

Monday API fails

Credentials missing

Network issue occurs

System automatically loads dummy dataset and continues functioning.

This ensures always-on demo capability.

📈 Design Decisions

Avoided complex GraphQL filtering → filtered in Python for reliability

Used heuristic forecasting (probability-weighted)

Modular architecture for scalability

Separation of concerns for maintainability

Clean error handling layer

Transparent trace logging
