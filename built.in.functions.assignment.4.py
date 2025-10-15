"""
Simple CSV reader and sorter for the IMDB movies dataset.
Requirements: do not use any external modules or the csv module — only Python built-ins.

Functions:
 - parse_csv_text(text): parse CSV content into list of rows (lists of fields).
 - read_and_sort_by_director(path): read file, parse, and return list of rows sorted by Director (alphabetical).

This parser supports quoted fields with commas and double-quote escaping by doubling.
It assumes newlines do not appear inside quoted fields (which matches the provided dataset).
"""

from typing import List


def parse_csv_text(text: str) -> List[List[str]]:
    """Parse CSV text into rows of fields using only builtins.

    Supports:
      - Comma-separated fields
      - Fields optionally enclosed in double quotes
      - Escaped quotes inside quoted fields as "" (two double quotes)

    Note: This is a small, robust-enough CSV parser for the dataset provided.
    """
    rows: List[List[str]] = []
    i = 0
    n = len(text)
    row: List[str] = []
    field_chars: List[str] = []
    in_quotes = False

    while i < n:
        ch = text[i]

        if in_quotes:
            if ch == '"':
                # Could be end of quoted field or escaped quote
                if i + 1 < n and text[i + 1] == '"':
                    # Escaped quote -> append one quote and skip the next
                    field_chars.append('"')
                    i += 2
                    continue
                else:
                    # End of quoted field
                    in_quotes = False
                    i += 1
                    continue
            else:
                # Regular char inside quotes
                field_chars.append(ch)
                i += 1
                continue

        # not in_quotes
        if ch == ',':
            # end of field
            row.append(''.join(field_chars))
            field_chars = []
            i += 1
            continue

        if ch == '"':
            in_quotes = True
            i += 1
            continue

        if ch == '\n' or ch == '\r':
            # handle CRLF or LF
            # Finish current field and row when encountering a newline
            # But skip lone CR in CRLF sequence
            # Collect any consecutive CR/LF as a single newline
            # Append current field
            row.append(''.join(field_chars))
            field_chars = []

            # append row if it's not an empty line (or if it's the header / real row)
            rows.append(row)
            row = []

            # consume any following LF when we saw CR
            if ch == '\r' and i + 1 < n and text[i + 1] == '\n':
                i += 2
            else:
                i += 1
            continue

        # regular character
        field_chars.append(ch)
        i += 1

    # end while
    # finalize last field/row if any
    if in_quotes:
        # Unterminated quote - still try to salvage
        row.append(''.join(field_chars))
        rows.append(row)
    else:
        # if there is any buffered content or pending row
        if field_chars or row:
            row.append(''.join(field_chars))
            rows.append(row)

    return rows


def read_and_sort_by_director(path: str) -> List[List[str]]:
    """Read a CSV file at path and return rows sorted by Director (alphabetical).

    Returns the header row followed by data rows sorted by the Director column.
    If the Director column is missing, returns rows unsorted.
    """
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()

    rows = parse_csv_text(text)
    if not rows:
        return []

    header = rows[0]
    data = rows[1:]

    # find index for Director column (case-sensitive match to 'Director')
    try:
        director_idx = header.index('Director')
    except ValueError:
        # try case-insensitive fallback
        director_idx = None
        for idx, col in enumerate(header):
            if col.strip().lower() == 'director':
                director_idx = idx
                break

    if director_idx is None:
        # no director column found
        return [header] + data

    # Sort using director column, stripping whitespace and using lower-case for stable alphabetical order
    def key_fn(row: List[str]):
        if director_idx < len(row):
            return row[director_idx].strip().lower()
        return ''

    sorted_data = sorted(data, key=key_fn)
    return [header] + sorted_data


if __name__ == '__main__':
    # simple demo when run directly
    import sys

    if len(sys.argv) < 2:
        print('Usage: python sort_imdb_by_director.py <path-to-csv>')
        print('Example: python sort_imdb_by_director.py "c:\\\\Users\\\\hubba\\\\Downloads\\\\imdb-movies-dataset\\\\imdb-movies-dataset.csv"')
        sys.exit(1)

    path = sys.argv[1]
    rows = read_and_sort_by_director(path)

    # print top 100 directors & titles after sorting
    header = rows[0] if rows else []
    print('Header:', header)
    for r in rows[1:101]:
        # print Director and Title if present
        title = r[1] if len(r) > 1 else ''
        director = r[8] if len(r) > 8 else ''
        print(f'{director} - {title}')