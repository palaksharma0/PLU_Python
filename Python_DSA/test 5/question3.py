'''
# 3. Online Banking Transaction Analyzer
### Problem Statement
A bank stores transactions in SQLite.
Each transaction contains:
* Transaction ID
* Account Number
* Amount
* Date
* Type (Credit/Debit)
### Requirements
1. Retrieve all transactions.
2. Sort them by amount using **Quick Sort**.
3. Search transactions using Transaction ID.
4. Calculate total credits and debits.
5. Display the top 5 highest-value transactions.
### Concepts
* SQL
* Quick Sort
* Binary Search
* Aggregation
'''


import sqlite3

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[0]
    left = [x for x in arr[1:] if x[2] <= pivot[2]]
    right = [x for x in arr[1:] if x[2] > pivot[2]]
    return quick_sort(left) + [pivot] + quick_sort(right)

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

con = sqlite3.connect("bank.db")
cur = con.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS transactions(
    tid INTEGER PRIMARY KEY,
    acc_no TEXT,
    amount REAL,
    date TEXT,
    type TEXT
)
""")

cur.execute("SELECT COUNT(*) FROM transactions")
if cur.fetchone()[0] == 0:
    data = [
        (101,"AC001",5000,"2026-07-01","Credit"),
        (102,"AC002",2000,"2026-07-02","Debit"),
        (103,"AC003",7000,"2026-07-03","Credit"),
        (104,"AC004",1500,"2026-07-04","Debit"),
        (105,"AC005",9000,"2026-07-05","Credit"),
        (106,"AC006",4000,"2026-07-06","Debit"),
        (107,"AC007",6500,"2026-07-07","Credit")
    ]
    cur.executemany("INSERT INTO transactions VALUES(?,?,?,?,?)", data)
    con.commit()

cur.execute("SELECT * FROM transactions")
transactions = cur.fetchall()

transactions = quick_sort(transactions)

print("Transactions Sorted by Amount")
for t in transactions:
    print(t)

by_id = sorted(transactions, key=lambda x: x[0])

tid = int(input("\nEnter Transaction ID: "))
result = binary_search(by_id, tid)

if result:
    print("\nTransaction Found:")
    print(result)
else:
    print("Transaction Not Found")

credit = sum(t[2] for t in transactions if t[4] == "Credit")
debit = sum(t[2] for t in transactions if t[4] == "Debit")

print("\nTotal Credit:", credit)
print("Total Debit:", debit)

print("\nTop 5 Highest Transactions")
for t in sorted(transactions, key=lambda x: x[2], reverse=True)[:5]:
    print(t)

con.close()

