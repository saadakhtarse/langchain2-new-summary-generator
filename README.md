# 📰 News Research Tool

A Streamlit app that lets you ask questions about news articles using AI.

## What it does
- Enter news article URLs
- App scrapes and processes the articles
- Ask any question about the articles
- Get answers with source URLs

## Test URLs used
- https://www.moneycontrol.com/news/business/banks/hdfc-bank-re-appoints-sanmoy-chakrabarti-as-chief-risk-officer-11259771.html
- https://www.moneycontrol.com/news/business/markets/market-corrects-post-rbi-ups-inflation-forecast-icrr-bet-on-these-top-10-rate-sensitive-stocks-ideas-11142611.html

## Sample Questions to ask
- Who is Sanmoy Chakrabarti?
- What are the top rate sensitive stocks?
- What did RBI do with inflation forecast?

## Setup
1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Add your Anthropic API key in `secret_key.py`
4. Run: `streamlit run main.py`

## Tech Stack
- LangChain
- Anthropic Claude
- Streamlit
- FAISS
- RecursiveCharacterTextSplitter