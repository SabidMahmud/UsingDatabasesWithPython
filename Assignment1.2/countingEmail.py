import sqlite3

conn = sqlite3.connect('emaildb.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Counts')

cur.execute('''
CREATE TABLE Counts (org TEXT, count INTEGER)''')

fname = input('File name: ')
if (len(fname) < 1): fname = 'mbox-short.txt'
txtfile = open(fname)
for line in txtfile:
    if not line.startswith('From: '):
        continue

    email = line.split()[1]
    org = email.split("@")
    org = org[1]
    # print(email, org)
    
    cur.execute('SELECT count FROM Counts WHERE org = ? ', (org,))
    row = cur.fetchone()
    if row is None:
        cur.execute('''INSERT INTO Counts (org, count)
                VALUES (?, 1)''', (org,))
    else:
        cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ?',
                    (org,))
    conn.commit()

cur.close()
conn.close()