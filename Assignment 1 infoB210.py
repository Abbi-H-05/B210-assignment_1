def infer_type(value):
    value = value.strip()
    if value == "":
        return "str"
    try:
        int(value)
        return "int"
    except ValueError:
        try:
            float(value)
            return "float"
        except ValueError:
            return "str"

def main():
    filename = "imdb-movies-dataset.csv"
    with open(filename, "r", encoding="utf-8") as f:
        header = f.readline().strip().split(",")
        first_row = f.readline().strip().split(",")
    types = []
    for value in first_row:
        types.append(infer_type(value))
    for col, dtype in zip(header, types):
        print(f"{col}: {dtype}")

if __name__ == "__main__":
    main()