import pandas as pd
import sqlite3

# =====================================
# CONNECT DATABASE
# =====================================

conn = sqlite3.connect(
    "data/warehouse/saas.db"
)

# =====================================
# LOAD CUSTOMER 360
# =====================================

df = pd.read_sql_query(
    """
    SELECT *
    FROM customer_360
    """,
    conn
)

# =====================================
# EXPORT CSV
# =====================================

df.to_csv(
    "data/powerbi/customer_360.csv",
    index=False
)

print(
    "Power BI CSV Exported Successfully"
)