import pandas as pd
import numpy as np
import random
from faker import Faker

fake = Faker()

np.random.seed(42)
random.seed(42)

users_df = pd.read_csv("data/raw/users.csv")
subscriptions_df = pd.read_csv("data/raw/subscriptions.csv")

campaign_types = [
    "Onboarding",
    "Feature Update",
    "Discount Offer",
    "Newsletter",
    "Webinar Invite"
]

marketing_events = []

engagement_id = 1

for _, user in users_df.iterrows():

    user_id = user["user_id"]

    churned = subscriptions_df.loc[
        subscriptions_df["user_id"] == user_id,
        "is_churned"
    ].values[0]

    # Retained users engage more
    if churned:
        num_campaigns = random.randint(1, 5)
    else:
        num_campaigns = random.randint(5, 15)

    for _ in range(num_campaigns):

        campaign = random.choice(campaign_types)

        # Lower engagement for churned users
        if churned:
            opened = np.random.choice(
                [0, 1],
                p=[0.7, 0.3]
            )

            clicked = np.random.choice(
                [0, 1],
                p=[0.9, 0.1]
            )

        else:
            opened = np.random.choice(
                [0, 1],
                p=[0.2, 0.8]
            )

            clicked = np.random.choice(
                [0, 1],
                p=[0.4, 0.6]
            )

        marketing_events.append({
            "engagement_id": engagement_id,
            "user_id": user_id,
            "campaign_type": campaign,
            "email_opened": opened,
            "clicked": clicked,
            "engagement_time": fake.date_time_between(
                start_date='-6M',
                end_date='now'
            )
        })

        engagement_id += 1

marketing_df = pd.DataFrame(marketing_events)

marketing_df.to_csv(
    "data/raw/marketing_engagement.csv",
    index=False
)

print(marketing_df.head())
print(f"Total Marketing Events: {len(marketing_df)}")