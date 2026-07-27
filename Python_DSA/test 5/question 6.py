'''
# 6. Food Delivery Route Optimizer
### Problem Statement
A food delivery company stores restaurants and delivery locations.
Database tables:
Restaurant
Delivery
Orders
### Requirements
1. Fetch all pending orders.
2. Build a **Graph** representing restaurants and delivery areas.
3. Find the shortest delivery path using **BFS**.
4. Display delivery order sequence.
5. Mark completed deliveries in SQLite.
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
    order = []

    while q:
        node = q.popleft()
        if node not in visited:
            visited.add(node)
            order.append(node)
            for i in graph[node]:
                if i not in visited:
                    q.append(i)
    return order

con = sqlite3.connect("food.db")
cur = con.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS Orders(
    order_id INTEGER PRIMARY KEY,
    restaurant TEXT,
    delivery TEXT,
    status TEXT
)
""")

cur.execute("SELECT COUNT(*) FROM Orders")
if cur.fetchone()[0] == 0:
    data = [
        (101,"R1","A","Pending"),
        (102,"R1","B","Pending"),
        (103,"R2","C","Pending"),
        (104,"R2","D","Delivered")
    ]
    cur.executemany("INSERT INTO Orders VALUES(?,?,?,?)", data)
    con.commit()

cur.execute("SELECT * FROM Orders WHERE status='Pending'")
orders = cur.fetchall()

print("Pending Orders")
for o in orders:
    print(o)

graph = {
    "R1":["A","B"],
    "R2":["C","D"],
    "A":[],
    "B":[],
    "C":[],
    "D":[]
}

print("\nDelivery Path from R1")
path = bfs(graph, "R1")
print(path)

print("\nDelivery Sequence")
for place in path:
    print(place)

cur.execute("UPDATE Orders SET status='Delivered' WHERE status='Pending'")
con.commit()

print("\nUpdated Orders")
cur.execute("SELECT * FROM Orders")
for row in cur.fetchall():
    print(row)

con.close()