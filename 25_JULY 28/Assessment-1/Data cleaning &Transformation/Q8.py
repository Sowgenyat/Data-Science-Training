import pandas as pd
import numpy as np
import os
file_path = r"C:\Users\MY-PC\Desktop\Data-Science-Training\JULY 28\Assessment-1\CSV & JSON handling\students_cleaned.csv"
if os.path.exists(file_path):
    df = pd.read_csv(file_path)
    def make_tax_id(x):
        return f"TAX-{x}"
    df["Tax_ID"] = df["ID"].apply(make_tax_id)
    df["Status"] = np.where(df["Score"] >= 85, "Distinction",
                            np.where(df["Score"] >= 60, "Passed", "Failed"))
    df.to_csv("students_transformed.csv", index=False)
    print("Updated")
    print(df)


