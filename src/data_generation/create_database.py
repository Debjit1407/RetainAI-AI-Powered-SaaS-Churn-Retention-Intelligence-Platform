import sqlite3
import pandas as pd
import os

os.makedirs("data/warehouse", exist_ok=True)

conn = sqlite3.connect("data/warehouse/saas.db")

users = pd.read_csv("data/raw/users.csv")
subscriptions = pd.read_csv("data/raw/subscriptions.csv")
usage_events = pd.read_csv("data/raw/usage_events.csv")
support_tickets = pd.read_csv("data/raw/support_tickets.csv")
marketing_engagement = pd.read_csv(
    "data/raw/marketing_engagement.csv"
)

users.to_sql(
    "users",
    conn,
    if_exists="replace",
    index=False
)

subscriptions.to_sql(
    "subscriptions",
    conn,
    if_exists="replace",
    index=False
)

usage_events.to_sql(
    "usage_events",
    conn,
    if_exists="replace",
    index=False
)

support_tickets.to_sql(
    "support_tickets",
    conn,
    if_exists="replace",
    index=False
)

marketing_engagement.to_sql(
    "marketing_engagement",
    conn,
    if_exists="replace",
    index=False
)

print("Database created successfully")