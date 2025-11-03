# ...existing code...
class Movie:
    """
    Simple Movie data container.
    Attributes are created from CSV header names (sanitized to valid identifiers).
    """
    def __init__(self, **fields):
        for key, val in fields.items():
            # sanitize header -> attribute name (alphanumeric and underscores, lowercased)
            attr = ''.join(ch if ch.isalnum() else '_' for ch in key).lower()
            setattr(self, attr, val)

    def __repr__(self):
        # show title and year if available
        title = getattr(self, 'title', None) or getattr(self, 'Title', None) or 'Unknown'
        year = getattr(self, 'year', None) or ''
        return f"<Movie {title!r} {year}>"

def _parse_csv_text(text):
    """
    Minimal CSV parser (no modules) that handles quoted fields with commas,
    doubled quotes inside quoted fields, and newlines inside quoted fields.
    Returns a list of rows, each row is a list of field strings.
    """
    rows = []
    row = []
    field = []
    in_quotes = False
    i = 0
    L = len(text)
    while i < L:
        ch = text[i]
        if ch == '"':
            if in_quotes and i+1 < L and text[i+1] == '"':
                # doubled quote -> literal quote
                field.append('"')
                i += 2
                continue
            in_quotes = not in_quotes
            i += 1
            continue
        if ch == ',' and not in_quotes:
            row.append(''.join(field))
            field = []
            i += 1
            continue
        if ch == '\n' and not in_quotes:
            row.append(''.join(field))
            field = []
            rows.append(row)
            row = []
            i += 1
            continue
        # regular character (including \r)
        if ch != '\r':
            field.append(ch)
        i += 1
    # handle last field / row if file does not end with newline
    if field or row:
        row.append(''.join(field))
        rows.append(row)
    return rows

def load_movies_from_csv(path):
    """
    Reads CSV at path and returns list of Movie objects.
    Does not use any external modules.
    """
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        text = f.read()
    rows = _parse_csv_text(text)
    if not rows:
        return []
    header = rows[0]
    movies = []
    for r in rows[1:]:
        # align row length with header (missing -> empty string)
        if len(r) < len(header):
            r += [''] * (len(header) - len(r))
        # ignore extra columns if any
        rowdict = {header[i]: r[i] for i in range(min(len(header), len(r)))}
        movies.append(Movie(**rowdict))
    return movies

if __name__ == '__main__':
    # change this path if your CSV is elsewhere
    csv_path = r'c:\Users\hubba\Downloads\imdb-movies-dataset\imdb-movies-dataset.csv'
    movies = load_movies_from_csv(csv_path)
    print(f'Loaded {len(movies)} movies')
    # show first 5 titles
    for m in movies[:5]:
        print(m)
# ...existing code...