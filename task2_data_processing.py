import os
import glob
import pandas as pd

json_files = glob.glob("data/trends_*.json")

if not json_files:
    print("No JSON file found in data folder")
    exit()

latest_file = max(json_files, key=os.path.getmtime)

df = pd.read_json(latest_file)

print(f"Loaded {len(df)} stories from {latest_file}")

df = df.drop_duplicates(subset="post_id")
print(f"After removing duplicates: {len(df)}")

df = df.dropna(subset=["post_id", "title", "score"])
print(f"After removing nulls: {len(df)}")

df["title"] = df["title"].astype(str).str.strip()
df["score"] = pd.to_numeric(df["score"], errors="coerce")
df["num_comments"] = pd.to_numeric(df["num_comments"], errors="coerce").fillna(0)

df = df.dropna(subset=["score"])
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)

df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")

output_file = "data/trends_clean.csv"
df.to_csv(output_file, index=False)

print(f"\nSaved {len(df)} rows to {output_file}\n")

print("Stories per category:")
print(df["category"].value_counts())