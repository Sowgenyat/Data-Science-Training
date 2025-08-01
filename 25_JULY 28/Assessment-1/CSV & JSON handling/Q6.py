import pandas as pd
import numpy as np

df = pd.read_csv("students.csv")
df["Age"] = df["Age"].fillna(df["Age"].mean())
df["Score"] = df["Score"].fillna(0)
df.to_csv("students_cleaned.csv", index=False)
print(" Cleaned data saved as students_cleaned.csv")
