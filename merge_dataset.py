import pandas as pd
import glob

files = glob.glob("SkinSAFE/*.csv")

print("Files Found:", len(files))

all_data = []

for file in files:
    df = pd.read_csv(file)
    all_data.append(df)

combined = pd.concat(all_data, ignore_index=True)

combined.to_csv("merged_products.csv", index=False)

print("Dataset Merged Successfully")
print("Total Rows:", len(combined))