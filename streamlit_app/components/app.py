import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import ollama

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="AI SaaS Churn Platform",
    layout="wide"
)

# =========================================
# PAGE TITLE
# =========================================

st.title(
    "AI-Powered SaaS Customer Churn Intelligence Platform"
)

st.write(
    "Enterprise AI Retention Analytics Dashboard"
)

# =========================================
# SIDEBAR NAVIGATION
# =========================================

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go To",
    [
        "Executive Dashboard",
        "Customer Intelligence",
        "AI Retention Insights"
    ]
)

# =========================================
# DATABASE CONNECTION
# =========================================

conn = sqlite3.connect(
    "data/warehouse/saas.db"
)

# =========================================
# LOAD DATA
# =========================================

df = pd.read_sql_query(
    """
    SELECT *
    FROM customer_360
    """,
    conn
)

# =========================================
# EXECUTIVE DASHBOARD
# =========================================

if page == "Executive Dashboard":

    st.header("Executive Dashboard")

    # -------------------------------------
    # KPI METRICS
    # -------------------------------------

    total_customers = len(df)

    churn_rate = (
        df["is_churned"].mean() * 100
    )

    avg_revenue = (
        df["monthly_revenue"].mean()
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Customers",
        total_customers
    )

    col2.metric(
        "Churn Rate",
        f"{churn_rate:.2f}%"
    )

    col3.metric(
        "Average Revenue",
        f"${avg_revenue:.2f}"
    )

    # -------------------------------------
    # CHURN DISTRIBUTION
    # -------------------------------------

    st.subheader(
        "Customer Churn Distribution"
    )

    fig, ax = plt.subplots()

    sns.countplot(
        data=df,
        x="is_churned",
        ax=ax
    )

    ax.set_title(
        "Customer Churn Distribution"
    )

    st.pyplot(fig)

    # -------------------------------------
    # PLAN ANALYSIS
    # -------------------------------------

    st.subheader(
        "Churn Rate by Plan Type"
    )

    plan_churn = df.groupby(
        "plan_type"
    )["is_churned"].mean()

    fig2, ax2 = plt.subplots()

    plan_churn.plot(
        kind="bar",
        ax=ax2
    )

    ax2.set_ylabel(
        "Churn Rate"
    )

    st.pyplot(fig2)

    # -------------------------------------
    # COUNTRY ANALYSIS
    # -------------------------------------

    st.subheader(
        "Churn Rate by Country"
    )

    country_churn = df.groupby(
        "country"
    )["is_churned"].mean()

    fig3, ax3 = plt.subplots(
        figsize=(10, 5)
    )

    country_churn.plot(
        kind="bar",
        ax=ax3
    )

    ax3.set_ylabel(
        "Churn Rate"
    )

    st.pyplot(fig3)

# =========================================
# CUSTOMER INTELLIGENCE PAGE
# =========================================

if page == "Customer Intelligence":

    st.header(
        "Customer Intelligence Lookup"
    )

    selected_customer = st.selectbox(
        "Select Customer ID",
        df["user_id"]
    )

    customer_data = df[
        df["user_id"] == selected_customer
    ]

    st.subheader(
        "Customer Details"
    )

    st.dataframe(customer_data)

    customer = customer_data.iloc[0]

    # -------------------------------------
    # CUSTOMER RISK INDICATORS
    # -------------------------------------

    st.subheader(
        "Customer Risk Indicators"
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Usage Events",
        int(customer["total_usage_events"])
    )

    col2.metric(
        "Support Tickets",
        int(customer["total_tickets"])
    )

    col3.metric(
        "Satisfaction Score",
        round(
            customer["avg_satisfaction"],
            2
        )
        if pd.notnull(
            customer["avg_satisfaction"]
        )
        else "N/A"
    )

    # -------------------------------------
    # CUSTOMER ENGAGEMENT CHART
    # -------------------------------------

    st.subheader(
        "Customer Engagement Metrics"
    )

    engagement_df = pd.DataFrame({
        "Metric": [
            "Usage Events",
            "Session Duration",
            "Email Open Rate",
            "Click Rate"
        ],
        "Value": [
            customer["total_usage_events"],
            customer["avg_session_duration"],
            customer["email_open_rate"],
            customer["click_rate"]
        ]
    })

    fig4, ax4 = plt.subplots()

    sns.barplot(
        data=engagement_df,
        x="Metric",
        y="Value",
        ax=ax4
    )

    ax4.set_title(
        "Customer Engagement Metrics"
    )

    st.pyplot(fig4)

# =========================================
# AI RETENTION INSIGHTS PAGE
# =========================================

if page == "AI Retention Insights":

    st.header(
        "AI Retention Intelligence"
    )

    selected_customer = st.selectbox(
        "Select Customer ID",
        df["user_id"],
        key="ai_customer"
    )

    customer_data = df[
        df["user_id"] == selected_customer
    ]

    st.subheader(
        "Selected Customer"
    )

    st.dataframe(customer_data)

    customer = customer_data.iloc[0]

    # -------------------------------------
    # AI GENERATION BUTTON
    # -------------------------------------

    if st.button(
        "Generate AI Retention Insights"
    ):

        with st.spinner(
            "Generating AI insights..."
        ):

            prompt = f"""
            You are an enterprise SaaS retention strategist.

            Analyze this customer.

            Country:
            {customer['country']}

            Industry:
            {customer['industry']}

            Plan:
            {customer['plan_type']}

            Monthly Revenue:
            {customer['monthly_revenue']}

            Usage Events:
            {customer['total_usage_events']}

            Average Session Duration:
            {customer['avg_session_duration']}

            Support Tickets:
            {customer['total_tickets']}

            Satisfaction Score:
            {customer['avg_satisfaction']}

            Email Open Rate:
            {customer['email_open_rate']}

            Click Rate:
            {customer['click_rate']}

            Generate:

            1. Churn Risk Analysis
            2. Key Risk Factors
            3. Retention Recommendations
            4. Executive Summary
            5. Customer Success Actions
            """

            response = ollama.chat(
                model="phi3",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            st.subheader(
                "AI Retention Recommendations"
            )

            st.write(
                response["message"]["content"]
            )

# =========================================
# FOOTER
# =========================================

st.markdown("---")

st.caption(
    "AI-Powered SaaS Customer Churn Prediction & Retention Intelligence Platform"
)