import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect('video_details.db')

# Query to fetch all records from the 'videos' table
query = "SELECT * FROM videos"

# Use pandas to read the SQL query into a DataFrame
df = pd.read_sql_query(query, conn)

# Close the database connection
conn.close()
print(df.__len__())
# Print two items from each column
for col in df.columns:
    print(f"{col} name of -----:")
    items = df[col].head(2).tolist()  # Fetch the first two items from the column
    for item in items:
        print(f"  - ----{item}")
        print()
    print("------\n")
