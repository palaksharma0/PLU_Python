import sqlite3

def binary_search(arr, key):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid][0] == key:
            return arr[mid]
        elif arr[mid][0] < key:
            low = mid + 1
        else:
            high = mid - 1
    return None

con = sqlite3.connect("sales.db")
cur = con.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS sales(
    emp_id INTEGER PRIMARY KEY,
    product TEXT,
    quantity INTEGER,
    revenue REAL,
    region TEXT,
    incentive TEXT
)
""")

cur.execute("SELECT COUNT(*) FROM sales")
if cur.fetchone()[0] == 0:
    data = [
        (101,"Laptop",10,50000,"North","No"),
        (102,"Mouse",50,15000,"South","No"),
        (103,"Keyboard",30,18000,"East","No"),
        (104,"Monitor",20,40000,"North","No"),
        (105,"Printer",15,30000,"West","No"),
        (106,"Scanner",12,25000,"South","No")
    ]
    cur.executemany("INSERT INTO sales VALUES(?,?,?,?,?,?)", data)
    con.commit()

cur.execute("SELECT * FROM sales")
sales = cur.fetchall()

sales.sort(key=lambda x: x[3], reverse=True)

print("Sales Records Sorted by Revenue")
for s in sales:
    print(s)

search_list = sorted(sales, key=lambda x: x[0])

emp = int(input("\nEnter Salesperson ID: "))
record = binary_search(search_list, emp)

if record:
    print("\nSalesperson Found")
    print(record)
else:
    print("Salesperson Not Found")

print("\nTop 5 Salespersons")
for s in sales[:5]:
    print(s)

region = {}

for s in sales:
    if s[4] not in region:
        region[s[4]] = 0
    region[s[4]] += s[3]

highest = max(region, key=region.get)
print("\nHighest Revenue Region:", highest, region[highest])

cur.execute("UPDATE sales SET incentive='Yes' WHERE revenue>=30000")
con.commit()

print("\nUpdated Sales Records")
cur.execute("SELECT * FROM sales")
for row in cur.fetchall():
    print(row)

con.close()