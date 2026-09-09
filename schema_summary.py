import re

with open(r'sql\create_tables.sql', 'r') as f:
    sql = f.read()

tables = re.findall(r'CREATE TABLE \"(.*?)\" \((.*?)\);', sql, re.S)
for tname, tdef in tables:
    print(f'**{tname}**')
    lines = [l.strip() for l in tdef.split('\n') if l.strip() and not l.strip().startswith('--')]
    pk = []
    cols = []
    for l in lines:
        if l.startswith('CONSTRAINT'):
            m = re.search(r'PRIMARY KEY \((.*?)\)', l)
            if m: pk.extend([x.strip('" ') for x in m.group(1).split(',')])
            continue
        col_m = re.match(r'"([^"]+)"\s+([A-Za-z0-9_(),]+)(.*)', l)
        if col_m:
            cname = col_m.group(1)
            ctype = col_m.group(2)
            rest = col_m.group(3)
            is_nn = 'NOT NULL' in rest or 'PRIMARY KEY' in rest
            if 'PRIMARY KEY' in rest: pk.append(cname)
            cols.append(f'- `{cname}` ({ctype}, {"NOT NULL" if is_nn else "NULLABLE"})')
    print('**Primary Key:** ' + ', '.join([f'`{k}`' for k in pk]))
    print('\n'.join(cols))
    print('')
