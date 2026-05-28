import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import timedelta

fake = Faker()

np.random.seed(42)
random.seed(42)

users_df = pd.read_csv("data/raw/users.csv")
subscriptions_df = pd.read_csv("data/raw/subscriptions.csv")

event_types = [
    "login",
    "dashboard_view",
    "report_export",
    "api_call",
    "feature_usage"
]

usage_events = []

event_id = 1

for _, user in users_df.iterrows():

    user_id = user["user_id"]

    churned = subscriptions_df.loc[
        subscriptions_df["user_id"] == user_id,
        "is_churned"
    ].values[0]

    # Churned users have lower activity
    if churned:
        num_events = random.randint(5, 20)
    else:
        num_events = random.randint(40, 120)

    for _ in range(num_events):

        event_time = fake.date_time_between(
            start_date='-6M',
            end_date='now'
        )

        # Lower engagement for churned users
        if churned:
            session_duration = np.random.randint(1, 10)
        else:
            session_duration = np.random.randint(10, 60)

        usage_events.append({
            "event_id": event_id,
            "user_id": user_id,
            "event_type": random.choice(event_types),
            "event_time": event_time,
            "session_duration": session_duration
        })

        event_id += 1

usage_df = pd.DataFrame(usage_events)

usage_df.to_csv(
    "data/raw/usage_events.csv",
    index=False
)

print(usage_df.head())
print(f"Total Events Generated: {len(usage_df)}")