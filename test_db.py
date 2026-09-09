import psycopg2

try:
    conn = psycopg2.connect(host='localhost', port=5432, user='postgres')
    print('Connection successful without password!')
    conn.close()
except Exception as e:
    print('Connection error:', e)
