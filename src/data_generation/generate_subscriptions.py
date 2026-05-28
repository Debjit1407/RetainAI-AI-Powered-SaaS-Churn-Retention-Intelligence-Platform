import pandas as pd
import numpy as np
import random

users_df = pd.read_csv("data/raw/users.csv")

plans = {
    "Basic": 50,
    "Pro": 150,
    "Enterprise": 500
}

subscriptions = []

for _, row in users_df.iterrows():

    plan = random.choices(
        ["Basic", "Pro", "Enterprise"],
        weights=[0.6, 0.3, 0.1]
    )[0]

    revenue = plans[plan]

    churn_probability = {
        "Basic": 0.35,
        "Pro": 0.18,
        "Enterprise": 0.08
    }

    churned = np.random.rand() < churn_probability[plan]

    subscriptions.append({
        "subscription_id": random.randint(10000, 99999),
        "user_id": row["user_id"],
        "plan_type": plan,
        "monthly_revenue": revenue,
        "is_churned": int(churned)
    })

subscriptions_df = pd.DataFrame(subscriptions)

subscriptions_df.to_csv(
    "data/raw/subscriptions.csv",
    index=False
)

print(subscriptions_df.head())