# ...existing code...
def parse_csv_line(line):
    """Minimal CSV line parser handling quoted fields."""
    fields = []
    cur = []
    in_quotes = False
    i = 0
    while i < len(line):
        ch = line[i]
        if in_quotes:
            if ch == '"':
                # lookahead for double-quote escape
                if i + 1 < len(line) and line[i + 1] == '"':
                    cur.append('"')
                    i += 1
                else:
                    in_quotes = False
            else:
                cur.append(ch)
        else:
            if ch == '"':
                in_quotes = True
            elif ch == ',':
                fields.append(''.join(cur))
                cur = []
            else:
                cur.append(ch)
        i += 1
    # append last field (strip trailing newline)
    fields.append(''.join(cur).rstrip('\r\n'))
    return fields

def tokenize(text, min_len=2, stopwords=None):
    if stopwords is None:
        stopwords = {
            'the','and','a','an','is','it','to','of','in','that','this','with','for',
            'on','as','are','was','but','be','by','not','or','from','at','its','has',
            'have','they','their','i','you','he','she','we','his','her','them','who'
        }
    text = text.lower()
    words = []
    cur = []
    for ch in text:
        if ch.isalpha():
            cur.append(ch)
        else:
            if cur:
                w = ''.join(cur)
                if len(w) >= min_len and w not in stopwords:
                    words.append(w)
                cur = []
    if cur:
        w = ''.join(cur)
        if len(w) >= min_len and w not in stopwords:
            words.append(w)
    return words

def most_common_words_by_certificate(csv_path, top_n=10, min_word_len=2):
    """
    Returns dict: certificate -> list of (word, count) sorted by count desc.
    Does not use external modules.
    """
    counts_by_cert = {}
    try:
        f = open(csv_path, 'r', encoding='utf-8', errors='replace')
    except Exception as e:
        raise RuntimeError("Could not open file: " + str(e))
    with f:
        # read header and detect columns
        # Skip blank/comment lines until we find a plausible CSV header
        header_line = None
        while True:
            line = f.readline()
            if not line:
                return {}   # EOF before header found
            if not line.strip():
                continue    # skip empty lines
            if line.lstrip().startswith('#'):
                continue    # skip comment lines that start with '#'
            low = line.lower()
            # require a comma and at least one expected header token
            if ',' in line and ('title' in low or 'certificate' in low or 'review' in low):
                header_line = line
                break
            # otherwise keep searching (tolerant to stray lines before header)
        header = parse_csv_line(header_line)

        # DEBUG: show header found (helps when script returns nothing)
        print("DEBUG: header found ->", header)

        # Normalize header cells for reliable matching
        def norm(s):
            return ' '.join(s.strip().lower().split())

        header_norm = [norm(h) for h in header]

        # Use the provided header names exactly (case/whitespace tolerant)
        expected = [
            "title","year","certificate","duration (min)","genre","rating",
            "metascore","director","cast","votes","description","review count",
            "review title","review"
        ]
        expected_norm = [norm(e) for e in expected]

        # Build a map from normalized header -> index
        hdr_map = {}
        for i, hn in enumerate(header_norm):
            hdr_map[hn] = i

        # Find indices for Certificate and Review using exact expected names first
        cert_idx = hdr_map.get(norm("certificate"))
        review_idx = hdr_map.get(norm("review"))

        # If not found, try alternative expected names (e.g., "review title" -> "review")
        if review_idx is None:
            # prefer exact "review", then "description", then "review title"
            for alt in ("review", "description", "review title"):
                if hdr_map.get(norm(alt)) is not None:
                    review_idx = hdr_map.get(norm(alt))
                    break

        if cert_idx is None:
            # fallback to any header containing 'cert' or 'certificate'
            for i, hn in enumerate(header_norm):
                if 'cert' in hn or 'certificate' in hn:
                    cert_idx = i
                    break

        # final fallback: previous heuristic (keep robust behavior)
        if review_idx is None or cert_idx is None:
            review_idx = None
            cert_idx = None
            for i, col in enumerate(header):
                name = col.strip().lower()
                if review_idx is None and ('review' in name or 'plot' in name or 'description' in name or 'synopsis' in name or 'text' in name):
                    review_idx = i
                if cert_idx is None and ('certificate' in name or 'cert' in name or 'rating' == name or 'mpaa' in name):
                    cert_idx = i

        # DEBUG: show indices found
        print("DEBUG: cert_idx =", cert_idx, "review_idx =", review_idx)

        if review_idx is None or cert_idx is None:
            raise RuntimeError("Could not locate review and/or certificate columns in header: " + str(header))

        # process rows
        for line in f:
            if not line.strip():
                continue
            row = parse_csv_line(line)
            # guard for short rows
            if max(review_idx, cert_idx) >= len(row):
                continue
            cert = row[cert_idx].strip()
            review = row[review_idx].strip()
            if not cert or not review:
                continue
            words = tokenize(review, min_word_len)
            if not words:
                continue
            if cert not in counts_by_cert:
                counts_by_cert[cert] = {}
            bucket = counts_by_cert[cert]
            for w in words:
                bucket[w] = bucket.get(w, 0) + 1
    # build top-N lists
    result = {}
    for cert, bucket in counts_by_cert.items():
        items = list(bucket.items())
        items.sort(key=lambda x: x[1], reverse=True)
        result[cert] = items[:top_n]
    return result

# Example usage:
if __name__ == "__main__":
    # Use the actual CSV in Downloads (the OneDrive path you used earlier may not be the CSV you intend)
    path = r"C:\Users\hubba\Downloads\info_B210 fall 2025\imdb-movies-dataset.csv"
    print("Reading:", path)
    res = most_common_words_by_certificate(path, top_n=10)
    if not res:
        print("No results found — check the CSV path and header detection (see DEBUG above).")
    else:
        for cert, words in res.items():
            print(cert, ":", words)
# ...existing code...