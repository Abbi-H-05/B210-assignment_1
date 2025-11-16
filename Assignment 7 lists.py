def parse_csv_line(line):
    # simple CSV parser handling quoted fields and doubled quotes
    fields = []
    cur = []
    in_q = False
    i = 0
    while i < len(line):
        c = line[i]
        if c == '"':
            if in_q and i + 1 < len(line) and line[i + 1] == '"':
                cur.append('"')  # escaped quote
                i += 2
                continue
            in_q = not in_q
        elif c == ',' and not in_q:
            fields.append(''.join(cur))
            cur = []
        else:
            cur.append(c)
        i += 1
    # append last field
    fields.append(''.join(cur).rstrip('\n\r'))
    return fields

def export_titles_by_genre(csv_path):
    user_genre = input("Enter genre (e.g. Action): ").strip().lower()
    results = {}

    with open(csv_path, 'r', encoding='utf-8') as f:
        header = f.readline()
        if not header:
            print("Empty file.")
            return
        cols = parse_csv_line(header)
        # find column indices
        try:
            title_idx = cols.index('Title')
            duration_idx = cols.index('Duration (min)')
            genre_idx = cols.index('Genre')
        except ValueError:
            print("Required columns not found in CSV header.")
            return

        for raw in f:
            if not raw.strip():
                continue
            row = parse_csv_line(raw)
            # skip malformed rows
            if max(title_idx, duration_idx, genre_idx) >= len(row):
                continue
            title = row[title_idx].strip()
            genre_field = row[genre_idx].strip()
            # check genre membership (comma-separated)
            genres = [g.strip().lower() for g in genre_field.split(',') if g.strip()]
            if user_genre in genres:
                dur_raw = row[duration_idx].strip()
                # try to convert to int, else keep raw
                try:
                    duration = int(dur_raw)
                except Exception:
                    duration = dur_raw
                results[title] = duration

    out_name = f"movies_{user_genre.replace(' ', '_')}.txt"
    with open(out_name, 'w', encoding='utf-8') as outf:
        outf.write(repr(results))
    print(f"Wrote {len(results)} entries to {out_name}")

if __name__ == "__main__":
    csv_path = r"c:\Users\hubba\Downloads\imdb-movies-dataset\imdb-movies-dataset.csv"
    export_titles_by_genre(csv_path)
```// filepath: c:\Users\hubba\Downloads\imdb-movies-dataset\filter_by_genre.py
def parse_csv_line(line):
    # simple CSV parser handling quoted fields and doubled quotes
    fields = []
    cur = []
    in_q = False
    i = 0
    while i < len(line):
        c = line[i]
        if c == '"':
            if in_q and i + 1 < len(line) and line[i + 1] == '"':
                cur.append('"')  # escaped quote
                i += 2
                continue
            in_q = not in_q
        elif c == ',' and not in_q:
            fields.append(''.join(cur))
            cur = []
        else:
            cur.append(c)
        i += 1
    # append last field
    fields.append(''.join(cur).rstrip('\n\r'))
    return fields

def export_titles_by_genre(csv_path):
    user_genre = input("Enter genre (e.g. Action): ").strip().lower()
    results = {}

    with open(csv_path, 'r', encoding='utf-8') as f:
        header = f.readline()
        if not header:
            print("Empty file.")
            return
        cols = parse_csv_line(header)
        # find column indices
        try:
            title_idx = cols.index('Title')
            duration_idx = cols.index('Duration (min)')
            genre_idx = cols.index('Genre')
        except ValueError:
            print("Required columns not found in CSV header.")
            return

        for raw in f:
            if not raw.strip():
                continue
            row = parse_csv_line(raw)
            # skip malformed rows
            if max(title_idx, duration_idx, genre_idx) >= len(row):
                continue
            title = row[title_idx].strip()
            genre_field = row[genre_idx].strip()
            # check genre membership (comma-separated)
            genres = [g.strip().lower() for g in genre_field.split(',') if g.strip()]
            if user_genre in genres:
                dur_raw = row[duration_idx].strip()
                # try to convert to int, else keep raw
                try:
                    duration = int(dur_raw)
                except Exception:
                    duration = dur_raw
                results[title] = duration

    out_name = f"movies_{user_genre.replace(' ', '_')}.txt"
    with open(out_name, 'w', encoding='utf-8') as outf:
        outf.write(repr(results))
    print(f"Wrote {len(results)} entries to {out_name}")

if __name__ == "__main__":
    csv_path = r"c:\Users\hubba\Downloads\imdb-movies-dataset\imdb-movies-dataset.csv"
    export_titles_by_genre(csv_path)