import pandas as pd
import numpy as np
import random
from faker import Faker

fake = Faker()

np.random.seed(42)
random.seed(42)

users_df = pd.read_csv("data/raw/users.csv")
subscriptions_df = pd.read_csv("data/raw/subscriptions.csv")

support_tickets = []

ticket_id = 1

for _, user in users_df.iterrows():

    user_id = user["user_id"]

    churned = subscriptions_df.loc[
        subscriptions_df["user_id"] == user_id,
        "is_churned"
    ].values[0]

    # Churned users create more tickets
    if churned:
        num_tickets = random.randint(3, 10)
    else:
        num_tickets = random.randint(0, 4)

    for _ in range(num_tickets):

        priority = random.choice([
            "Low",
            "Medium",
            "High"
        ])

        # Longer resolution for churned users
        if churned:
            resolution_time = np.random.randint(24, 120)
            satisfaction_score = np.random.randint(1, 6)
        else:
            resolution_time = np.random.randint(1, 48)
            satisfaction_score = np.random.randint(6, 10)

        support_tickets.append({
            "ticket_id": ticket_id,
            "user_id": user_id,
            "priority": priority,
            "resolution_time_hours": resolution_time,
            "satisfaction_score": satisfaction_score,
            "created_at": fake.date_time_between(
                start_date='-6M',
                end_date='now'
            )
        })

        ticket_id += 1

support_df = pd.DataFrame(support_tickets)

support_df.to_csv(
    "data/raw/support_tickets.csv",
    index=False
)

print(support_df.head())
print(f"Total Tickets Generated: {len(support_df)}")