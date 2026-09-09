path = r"C:\Users\dell\OneDrive\Desktop\financial_performance\data\raw\DimProduct.csv"

with open(path, "rb") as f:
    content = f.read()

# Check raw newlines
crlf_count = content.count(b"\r\n")
lf_only_count = content.count(b"\n") - crlf_count
cr_only_count = content.count(b"\r") - crlf_count

print(f"Total bytes: {len(content)}")
print(f"CRLF count: {crlf_count}")
print(f"LF only count: {lf_only_count}")
print(f"CR only count: {cr_only_count}")

# Check lines split by CRLF
lines = content.split(b"\r\n")
if lines[-1] == b"":
    lines = lines[:-1]

print(f"Total rows when split by CRLF: {len(lines)}")

# Check pipe count in each row
bad_rows = []
for i, l in enumerate(lines):
    pipes = l.count(b"|")
    if pipes != 35:
        bad_rows.append((i+1, pipes, len(l)))

print(f"Rows with != 35 pipes: {len(bad_rows)}")
if bad_rows:
    print("First 10 bad rows:", bad_rows[:10])
