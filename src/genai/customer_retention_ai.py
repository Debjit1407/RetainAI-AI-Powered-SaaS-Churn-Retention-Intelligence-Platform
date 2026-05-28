import ollama
import pandas as pd
import sqlite3

# -----------------------------------
# CONNECT DATABASE
# -----------------------------------

conn = sqlite3.connect(
    "data/warehouse/saas.db"
)

# -----------------------------------
# LOAD CUSTOMER DATA
# -----------------------------------

df = pd.read_sql_query(
    """
    SELECT *
    FROM customer_360
    LIMIT 5
    """,
    conn
)

# -----------------------------------
# SELECT ONE CUSTOMER
# -----------------------------------

customer = df.iloc[0]

# -----------------------------------
# CREATE AI PROMPT
# -----------------------------------

prompt = f"""
You are a SaaS retention strategist.

Analyze this customer:

Country: {customer['country']}
Industry: {customer['industry']}
Plan Type: {customer['plan_type']}

Usage Events: {customer['total_usage_events']}
Session Duration: {customer['avg_session_duration']}

Support Tickets: {customer['total_tickets']}
Satisfaction Score: {customer['avg_satisfaction']}

Email Open Rate: {customer['email_open_rate']}
Click Rate: {customer['click_rate']}

Generate:
1. Churn Risk Analysis
2. Key Risk Factors
3. Retention Recommendations
4. Executive Summary
"""

# -----------------------------------
# OLLAMA RESPONSE
# -----------------------------------

response = ollama.chat(
    model="phi3",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

# -----------------------------------
# PRINT AI OUTPUT
# -----------------------------------

print("\n")
print("=" * 50)
print("AI RETENTION INSIGHTS")
print("=" * 50)

print(
    response["message"]["content"]
)