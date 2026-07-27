'''
# 7. Employee Attendance Analytics
### Problem Statement
A company records employee attendance.
Each record contains:
* Employee ID
* Name
* Check-in Time
* Check-out Time
### Requirements
1. Retrieve attendance records.
2. Calculate total working hours.
3. Sort employees by total hours worked.
4. Search employees using Employee ID.
5. Display employees who worked more than 45 hours this week.
### Concepts
* SQL
* Sorting
* Binary Search
* DateTime
'''

import sqlite3
from datetime import datetime

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

con = sqlite3.connect("attendance.db")
cur = con.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS attendance(
    emp_id INTEGER PRIMARY KEY,
    name TEXT,
    check_in TEXT,
    check_out TEXT
)
""")

cur.execute("SELECT COUNT(*) FROM attendance")
if cur.fetchone()[0] == 0:
    data = [
        (101,"Arya","2026-07-01 09:00","2026-07-01 18:00"),
        (102,"Rahul","2026-07-01 09:30","2026-07-01 17:30"),
        (103,"Priya","2026-07-01 08:30","2026-07-01 19:30"),
        (104,"Neha","2026-07-01 09:00","2026-07-01 16:00"),
        (105,"Amit","2026-07-01 08:00","2026-07-01 18:30")
    ]
    cur.executemany("INSERT INTO attendance VALUES(?,?,?,?)", data)
    con.commit()

cur.execute("SELECT * FROM attendance")
rows = cur.fetchall()

employees = []

for row in rows:
    cin = datetime.strptime(row[2], "%Y-%m-%d %H:%M")
    cout = datetime.strptime(row[3], "%Y-%m-%d %H:%M")
    hours = (cout - cin).seconds / 3600
    week_hours = hours * 5
    employees.append((row[0], row[1], week_hours))

employees.sort(key=lambda x: x[2], reverse=True)

print("Employees Sorted by Working Hours")
for e in employees:
    print(e)

search_list = sorted(employees, key=lambda x: x[0])

emp = int(input("\nEnter Employee ID: "))
result = binary_search(search_list, emp)

if result:
    print("\nEmployee Found")
    print(result)
else:
    print("Employee Not Found")

print("\nEmployees Working More Than 45 Hours")
for e in employees:
    if e[2] > 45:
        print(e)

con.close()