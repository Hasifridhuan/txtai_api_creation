from txtai.embeddings import Embeddings
import json
import time


embeddings = Embeddings()

start_time = time.time()
embeddings.load(path="models/final", cloud=None)
elapsed_time = time.time() - start_time

print(f"Loaded model in {elapsed_time:.2f} seconds")

with open("data/output.json", "r") as f:
    data = json.load(f)["descriptions"]
len(data)

txtai_data = []
i = 0
for text in data:
    txtai_data.append((i, text, None))
    i = i + 1

query = "gasket siemens comp centrifugal compressor 471-683-146 3mx8-10"

start_time = time.time()
results = embeddings.search(query, 1)
elapsed_time = time.time() - start_time
for r in results:
    print('1:')
    print(f"Text: {data[r[0]]}")
    print(f"Similarity: {r[1]}")
    print()

print(results)

data = "running the basket"
embeddings.upsert([(1025882, data, None)])
results = embeddings.search(data, 1)
elapsed_time = time.time() - start_time
for r in results:
    print("2:")
    # print(f"Text: {data[r[0]]}")
    # print(f"Similarity: {r[1]}")
    print()

print(results)

print(f"Search in {elapsed_time:.2f} seconds")
# for r in results:
#     print(f"Text: {data[r[0]]}")
#     print(f"Similarity: {r[1]}")
#     print()
#
# print(results)
