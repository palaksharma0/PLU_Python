'''
# 2. Hospital Patient Queue Management
### Problem Statement
A hospital stores patient details in SQLite.
Each patient has:
* Patient ID
* Name
* Age
* Priority Level
### Requirements
1. Fetch all patients.
2. Create a **Priority Queue** based on Priority Level.
3. Attend patients in order of priority.
4. After attending a patient, update the database.
5. Display the remaining patients.
### Concepts
* SQLite
* Priority Queue
* UPDATE Query
* Heap/Priority Queue
'''

import sqlite3
import heapq

con = sqlite3.connect("hospital.db")
cur = con.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS patients(
    patient_id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER,
    priority INTEGER,
    status TEXT
)
""")

cur.execute("SELECT COUNT(*) FROM patients")
if cur.fetchone()[0] == 0:
    data = [
        (101, "Rahul", 25, 2, "Waiting"),
        (102, "Priya", 40, 1, "Waiting"),
        (103, "Amit", 35, 3, "Waiting"),
        (104, "Neha", 28, 2, "Waiting"),
        (105, "Riya", 50, 1, "Waiting")
    ]
    cur.executemany("INSERT INTO patients VALUES(?,?,?,?,?)", data)
    con.commit()

cur.execute("SELECT * FROM patients WHERE status='Waiting'")
rows = cur.fetchall()

pq = []
for row in rows:
    heapq.heappush(pq, (row[3], row[0], row[1], row[2]))

print("Patients in Priority Order")
while pq:
    patient = heapq.heappop(pq)
    print(patient[1], patient[2], patient[3], "Priority:", patient[0])

    cur.execute(
        "UPDATE patients SET status='Attended' WHERE patient_id=?",
        (patient[1],)
    )
    con.commit()

print("\nRemaining Patients")
cur.execute("SELECT * FROM patients WHERE status='Waiting'")
rows = cur.fetchall()

if rows:
    for row in rows:
        print(row)
else:
    print("No patients waiting.")

con.close()

