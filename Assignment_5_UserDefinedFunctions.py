def average_rating_for_certificate(csv_path, certificate, encoding='utf-8', round_digits=None):
    """
    Calculate the average 'Rating' for rows whose 'Certificate' equals the given certificate.
    - csv_path: path to CSV file (string)
    - certificate: certificate to match (string). Matching is case-insensitive and trims whitespace.
    - encoding: file encoding to use when opening the file (default 'utf-8')
    - round_digits: if not None, round the returned average to this many decimals

    Returns:
    - float average rating if at least one matching row found
    - None if no matching rows or if file contains no usable ratings
    """
    # Read entire file (keeps parser simple and allows newlines inside quoted fields)
    with open(csv_path, 'r', encoding=encoding, errors='replace') as f:
        text = f.read()

    rows = []
    field_chars = []
    fields = []
    in_quotes = False
    i = 0
    n = len(text)

    # RFC-style CSV parsing: handle quotes, escaped quotes ("" ) and allow newlines inside quotes
    while i < n:
        ch = text[i]
        if ch == '"':
            # If inside quotes and next is also quote -> escaped quote
            if in_quotes and i + 1 < n and text[i + 1] == '"':
                field_chars.append('"')
                i += 1  # skip the escaped quote
            else:
                in_quotes = not in_quotes
        elif ch == ',' and not in_quotes:
            fields.append(''.join(field_chars))
            field_chars = []
        elif ch == '\r' and not in_quotes:
            # Windows CRLF or lone CR: treat as end-of-record; skip an immediate LF if present
            fields.append(''.join(field_chars))
            field_chars = []
            rows.append(fields)
            fields = []
            if i + 1 < n and text[i + 1] == '\n':
                i += 1
        elif ch == '\n' and not in_quotes:
            fields.append(''.join(field_chars))
            field_chars = []
            rows.append(fields)
            fields = []
        else:
            field_chars.append(ch)
        i += 1

    # Finish any trailing field/row (if file does not end with newline)
    if field_chars or fields:
        fields.append(''.join(field_chars))
        rows.append(fields)

    if not rows:
        return None

    # Normalize header (strip whitespace) and find indices for Certificate and Rating (case-insensitive)
    header = rows[0]
    header_norm = [h.strip().lower() for h in header]
    try:
        cert_idx = header_norm.index('certificate')
    except ValueError:
        return None  # certificate column not found
    try:
        rating_idx = header_norm.index('rating')
    except ValueError:
        return None  # rating column not found

    target = certificate.strip().lower()
    total = 0.0
    count = 0

    # Iterate records (skip header row)
    for r in rows[1:]:
        # Some rows may be shorter than header; skip those
        if len(r) <= max(cert_idx, rating_idx):
            continue
        cert_val = r[cert_idx].strip().lower()
        if cert_val != target:
            continue
        rating_str = r[rating_idx].strip()
        if rating_str == '':
            continue
        # try parse float (skip if invalid)
        try:
            rating_val = float(rating_str)
        except Exception:
            continue
        total += rating_val
        count += 1

    if count == 0:
        return None

    avg = total / count
    if round_digits is not None:
        try:
            avg = round(avg, int(round_digits))
        except Exception:
            pass
    return avg


if __name__ == '__main__':
    csv_path = r"c:\Users\hubba\Downloads\imdb-movies-dataset\imdb-movies-dataset.csv"

    # Example certificates to test
    certs = ['R', 'PG-13', 'PG', 'UA', 'A', 'U']

    for c in certs:
        avg = average_rating_for_certificate(csv_path, c, round_digits=3)
        if avg is None:
            print(f"Certificate '{c}': no matching rows with usable ratings found.")
        else:
            print(f"Certificate '{c}': average rating = {avg}")
