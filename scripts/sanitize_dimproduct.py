import os

raw_file = r"C:\Users\dell\OneDrive\Desktop\financial_performance\data\raw\DimProduct.csv"
staging_dir = r"C:\Users\dell\OneDrive\Desktop\financial_performance\data\staging"
os.makedirs(staging_dir, exist_ok=True)
staging_file = os.path.join(staging_dir, "DimProduct_sanitized.csv")

with open(raw_file, "rb") as f_in:
    data = f_in.read()

nul_count = data.count(b"\x00")
print(f"Raw file read: {len(data)} bytes, {nul_count} NUL bytes.")

sanitized_data = data.replace(b"\x00", b"")

with open(staging_file, "wb") as f_out:
    f_out.write(sanitized_data)

print(f"Sanitized file written: {len(sanitized_data)} bytes.")
print(f"Sanitized NUL count: {sanitized_data.count(b'\x00')}")
print(f"Difference in bytes: {len(data) - len(sanitized_data)}")

assert nul_count == 574, f"Expected 574 NUL bytes, found {nul_count}"
assert len(data) - len(sanitized_data) == 574, "Mismatch in removed byte count"

# Verify line count and pipe count on sanitized file
with open(staging_file, "rb") as f:
    lines = f.readlines()
print(f"Sanitized file total lines: {len(lines)}")
assert len(lines) == 606, f"Expected 606 lines, found {len(lines)}"
for idx, l in enumerate(lines):
    pipes = l.count(b"|")
    assert pipes == 35, f"Line {idx+1} has {pipes} pipes instead of 35!"
print("Sanitization verified successfully: exactly 606 lines with 35 pipes each and 0 NUL bytes.")
