from txtai.embeddings import Embeddings
import json
import time

embeddings = Embeddings({
    "path": "sentence-transformers/all-MiniLM-L6-v2"
})

with open("data/output_material.json", "r") as f:
    data = json.load(f)["material"]
print(len(data))

txtai_data = []
i = 0
for text in data:
    txtai_data.append((i, text, None))
    i = i + 1

# print(txtai_data[0])
print("start")
start_time = time.time()
embeddings.index(txtai_data)
elapsed_time = time.time() - start_time

print(f"Loaded model in {elapsed_time:.2f} seconds")
print("finish")

res = embeddings.search("gasket", 10)
for r in res:
    print(f"Text: {data[r[0]]}")
    print(f"Similarity: {r[1]}")
    print()

embeddings.save("models/final")
