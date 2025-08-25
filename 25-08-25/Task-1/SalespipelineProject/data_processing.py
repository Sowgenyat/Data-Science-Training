import pandas as pd

# Read raw CSV file
df = pd.read_csv("raw_sales_data.csv")

# Save the original raw data to 'data/raw_sales_data.csv'
df.to_csv("data/raw_sales_data.csv", index=False)

# Normalize column names
df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

# Convert 'date' column to YYYY-MM-DD format if present
if 'date' in df.columns:
    df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.strftime('%Y-%m-%d')

# Remove rows with any missing values
df_clean = df.dropna()

# Save cleaned CSV
df_clean.to_csv("data/clean_sales_data.csv", index=False)

print(" Raw data saved to data/raw_sales_data.csv")
print("Cleaned data saved to data/clean_sales_data.csv")
print(f" Cleaned dataset shape: {df_clean.shape}")
