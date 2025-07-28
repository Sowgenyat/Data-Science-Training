import numpy as np
import pandas as pd
scores = np.random.randint(35, 101, size=20)
above_75 = np.sum(scores > 75)
mean_score = np.mean(scores)
std_dev_score = np.std(scores)
df_scores = pd.DataFrame({"Score": scores})
df_scores.to_csv("scores.csv", index=False)
print("Generated Scores:", scores)
print("Number of students scoring above 75:", above_75)
print("Mean Score:", round(mean_score, 2))
print("Standard Deviation:", round(std_dev_score, 2))
