import pandas as pd
import numpy as np

df_cleaned = pd.read_csv("students_cleaned.csv")
df_cleaned.to_json("students.json",orient='records',  indent=4)
print("students.json created from cleaned CSV")
