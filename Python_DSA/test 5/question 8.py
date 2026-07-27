'''
# 8. Ride Booking Management System
### Problem Statement
A cab company stores:
Drivers
Customers
Bookings
### Requirements
1. Fetch available drivers.
2. Store them in a Graph representing city connectivity.
3. Find the nearest available driver using **BFS**.
4. Assign the booking.
5. Update driver availability.
### Concepts
* Graph
* BFS
* SQL JOIN
* UPDATE
'''

import sqlite3
from collections import deque

def bfs(graph, start):
    visited = set()
    q = deque([start])

    while q:
        node = q.popleft()
        if node not in visited:
            visited.add(node)
            if node.startswith("D"):
                return node
            for i in graph[node]:
                if i not in visited:
                    q.append(i)
    return None

con = sqlite3.connect("cab.db")
cur = con.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS Drivers(
    driver_id TEXT PRIMARY KEY,
    location TEXT,
    available TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS Bookings(
    booking_id INTEGER PRIMARY KEY,
    customer TEXT,
    location TEXT
)
""")

cur.execute("SELECT COUNT(*) FROM Drivers")
if cur.fetchone()[0] == 0:
    drivers = [
        ("D1","A","Yes"),
        ("D2","B","Yes"),
        ("D3","C","No"),
        ("D4","D","Yes")
    ]
    cur.executemany("INSERT INTO Drivers VALUES(?,?,?)", drivers)

    bookings = [
        (101,"Arya","A")
    ]
    cur.executemany("INSERT INTO Bookings VALUES(?,?,?)", bookings)
    con.commit()

cur.execute("SELECT * FROM Drivers WHERE available='Yes'")
print("Available Drivers")
for row in cur.fetchall():
    print(row)

graph = {
    "A":["B","D1"],
    "B":["A","C","D2"],
    "C":["B","D","D3"],
    "D":["C","D4"],
    "D1":[],
    "D2":[],
    "D3":[],
    "D4":[]
}

cur.execute("SELECT location FROM Bookings WHERE booking_id=101")
start = cur.fetchone()[0]

driver = bfs(graph, start)

if driver:
    print("\nNearest Driver:", driver)

    cur.execute(
        "UPDATE Drivers SET available='No' WHERE driver_id=?",
        (driver,)
    )
    con.commit()

    print("Booking Assigned Successfully")
else:
    print("No Driver Available")

print("\nUpdated Driver Status")
cur.execute("SELECT * FROM Drivers")
for row in cur.fetchall():
    print(row)

con.close()