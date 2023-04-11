import pandas as pd
import json

df = pd.read_csv("material_result.csv")

material_description = df["MaterialDescription"].tolist()

dictionary = {"material":material_description}

with open('output_material.json', 'w') as f:
    json.dump(dictionary, f, indent=4)