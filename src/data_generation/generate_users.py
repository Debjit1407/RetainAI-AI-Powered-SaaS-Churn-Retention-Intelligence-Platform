import pandas as pd
import numpy as np
from faker import Faker
import random

fake = Faker()

np.random.seed(42)
random.seed(42)

NUM_USERS = 5000

industries = [
    "SaaS",
    "Healthcare",
    "Finance",
    "Retail",
    "Education"
]

company_sizes = [
    "Small",
    "Medium",
    "Enterprise"
]

countries = [
    "USA",
    "UK",
    "India",
    "Germany",
    "Canada"
]

users = []

for user_id in range(1, NUM_USERS + 1):

    signup_date = fake.date_between(
        start_date='-2y',
        end_date='today'
    )

    users.append({
        "user_id": user_id,
        "name": fake.name(),
        "email": fake.email(),
        "country": random.choice(countries),
        "industry": random.choice(industries),
        "company_size": random.choice(company_sizes),
        "signup_date": signup_date
    })

users_df = pd.DataFrame(users)

users_df.to_csv(
    "data/raw/users.csv",
    index=False
)

print(users_df.head())