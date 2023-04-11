import sqlite3
import json


with open("data/output_material.json", "r") as f:
        data = json.load(f)["material"]

df = []
i = 0
for text in data:
        df.append((i, text))
        i = i + 1

# Connect to the database
conn = sqlite3.connect('materials.db')
c = conn.cursor()

# Create the materials table
c.execute('''CREATE TABLE materials
             (id INTEGER PRIMARY KEY, text TEXT)''')

# Insert data into the materials table
for row in df:
    c.execute('INSERT INTO materials VALUES (?, ?)', row)

c.execute('SELECT text FROM materials WHERE id=1')
results = c.fetchall()
for row in results:
    print(row)

# Commit changes and close the connection
conn.commit()
conn.close()
