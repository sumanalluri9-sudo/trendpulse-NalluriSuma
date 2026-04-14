import pandas as pd
import numpy as np

file_path = "data/trends_clean.csv"

df = pd.read_csv(file_path)

print(f"Loaded data: {df.shape}\n")

print("First 5 rows:")
print(df.head())

average_score = df["score"].mean()
average_comments = df["num_comments"].mean()

print(f"\nAverage score   : {average_score}")
print(f"Average comments: {average_comments}")

scores = df["score"].to_numpy()
comments = df["num_comments"].to_numpy()

print("\n--- NumPy Stats ---")
print(f"Mean score   : {np.mean(scores)}")
print(f"Median score : {np.median(scores)}")
print(f"Std deviation: {np.std(scores)}")
print(f"Max score    : {np.max(scores)}")
print(f"Min score    : {np.min(scores)}")

category_counts = df["category"].value_counts()
top_category = category_counts.idxmax()
top_category_count = category_counts.max()

print(f"\nMost stories in: {top_category} ({top_category_count} stories)")

most_commented_index = np.argmax(comments)
most_commented_title = df.iloc[most_commented_index]["title"]
most_commented_count = df.iloc[most_commented_index]["num_comments"]

print(f'\nMost commented story: "{most_commented_title}" - {most_commented_count} comments')

df["engagement"] = df["num_comments"] / (df["score"] + 1)
df["is_popular"] = df["score"] > average_score

output_file = "data/trends_analysed.csv"
df.to_csv(output_file, index=False)

print(f"\nSaved to {output_file}")