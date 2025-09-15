#Assignment 1 Copilot chat
#Write a python program that lists all variables in the file imdb-movies-dataset.csv with their data types. Do not use any python libraries or modules.​
Here is a pure Python program that reads imdb-movies-dataset.csv, lists all column names (variables), and infers their data types (int, float, or string) without using any external libraries or modules:
def infer_type(value):
    value = value.strip()
    if value == "":
        return "string"
    try:
        int(value)
        return "int"
    except ValueError:
        try:
            float(value)
            return "float"
        except ValueError:
            return "string"

filename = "imdb-movies-dataset.csv"

with open(filename, "r", encoding="utf-8") as f:
    header = f.readline().strip().split(",")
    types = ["unknown"] * len(header)
    for line in f:
        row = line.strip().split(",")
        for i, value in enumerate(row):
            t = infer_type(value)
            if types[i] == "unknown":
                types[i] = t
            elif types[i] != t:
                if (types[i] == "int" and t == "float") or (types[i] == "float" and t == "int"):
                    types[i] = "float"
                else:
                    types[i] = "string"
        # Only need a few rows to infer types, break after 100
        if f.tell() > 10000:
            break

for name, t in zip(header, types):
    print(f"{name}: {t}") 
This script:

Reads the first line for column names.
Reads up to 10,000 bytes of data to infer types.
Prints each variable (column) and its inferred type.
Let me know if you want this saved to a file or need any changes!

