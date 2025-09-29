#!/usr/bin/env python3
"""
Read 'imdb-movies-dataset.csv' (in the same folder), parse it without using any
external libraries, count how many movies belong to each genre and print the
counts. A movie that lists multiple genres is counted once for each of its
genres (e.g. a movie with "Comedy, Drama" increments both Comedy and Drama).

This implementation includes a small CSV line parser that handles quoted
fields and doubled quotes per CSV rules.
"""

import sys


def parse_csv_records(content):
    """Parse the full CSV content and return a list of records (each a list of fields).

    This parser handles quoted fields that may contain commas and newlines,
    and supports doubled quotes inside quoted fields. It does not use the
    csv module as requested.
    """
    records = []
    field = []
    record = []
    in_quotes = False
    i = 0
    length = len(content)
    while i < length:
        ch = content[i]
        if in_quotes:
            if ch == '"':
                # doubled quote -> literal quote
                if i + 1 < length and content[i + 1] == '"':
                    field.append('"')
                    i += 1
                else:
                    in_quotes = False
            else:
                field.append(ch)
        else:
            if ch == '"':
                in_quotes = True
            elif ch == ',':
                record.append(''.join(field))
                field = []
            elif ch == '\n':
                # end of record
                record.append(''.join(field))
                field = []
                records.append(record)
                record = []
            elif ch == '\r':
                # ignore CR (handles CRLF)
                pass
            else:
                field.append(ch)
        i += 1

    # append any trailing data as final record
    if in_quotes:
        # Unterminated quoted field; still try to finish the last field
        record.append(''.join(field))
        records.append(record)
    else:
        if field or record:
            record.append(''.join(field))
            records.append(record)

    return records


def main():
    csv_path = 'imdb-movies-dataset.csv'

    try:
        f = open(csv_path, 'r', encoding='utf-8')
    except Exception as e:
        sys.stderr.write('Error opening %s: %s\n' % (csv_path, e))
        return

    # Read full content and parse records (handles multiline fields)
    content = f.read()
    if not content:
        sys.stderr.write('CSV file is empty\n')
        f.close()
        return

    records = parse_csv_records(content)
    if not records:
        sys.stderr.write('No records found in CSV\n')
        f.close()
        return

    header = records[0]
    try:
        genre_idx = header.index('Genre')
    except ValueError:
        # try stripping whitespace variants
        cleaned = [h.strip() for h in header]
        if 'Genre' in cleaned:
            genre_idx = cleaned.index('Genre')
        else:
            sys.stderr.write('Could not find "Genre" column in header\n')
            f.close()
            return

    counts = {}
    # iterate records after header
    for rec in records[1:]:
        if genre_idx >= len(rec):
            continue
        genre_field = rec[genre_idx].strip()
        if not genre_field:
            continue
        parts = [g.strip() for g in genre_field.split(',') if g.strip()]
        for g in parts:
            counts[g] = counts.get(g, 0) + 1

    f.close()

    # Print results sorted by genre name
    for genre in sorted(counts.keys()):
        print(genre + ':', counts[genre])


if __name__ == '__main__':
    main()
