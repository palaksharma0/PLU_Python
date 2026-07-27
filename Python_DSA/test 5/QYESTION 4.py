'''
# 4. College Placement Portal
### Problem Statement
A college stores student records in SQLite.
Each student contains:
* Roll Number
* Name
* CGPA
* Skills
* Placement Status
### Requirements
1. Retrieve all students.
2. Sort students by CGPA using **Heap Sort**.
3. Search students by Roll Number.
4. Display students eligible for placements (CGPA > 7.5).
5. Update placement status after selection.
### Concepts
* Heap
* Heap Sort
* Binary Search
* SQL UPDATE
'''

import sqlite3
import heapq

def heap_sort(arr):
    heap = []
    for i in arr:
        heapq.heappush(heap, (i[2], i))
    return [heapq.heappop(heap)[1] for _ in range(len(heap))]

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

con = sqlite3.connect("college.db")
cur = con.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS students(
    roll INTEGER PRIMARY KEY,
    name TEXT,
    cgpa REAL,
    skills TEXT,
    status TEXT
)
""")

cur.execute("SELECT COUNT(*) FROM students")
if cur.fetchone()[0] == 0:
    data = [
        (101, "Arya", 8.9, "Python", "Not Placed"),
        (102, "Rahul", 7.2, "Java", "Not Placed"),
        (103, "Priya", 9.1, "AI", "Not Placed"),
        (104, "Amit", 6.8, "C++", "Not Placed"),
        (105, "Neha", 8.0, "Web", "Not Placed")
    ]
    cur.executemany("INSERT INTO students VALUES(?,?,?,?,?)", data)
    con.commit()

cur.execute("SELECT * FROM students")
students = cur.fetchall()

students = heap_sort(students)

print("Students Sorted by CGPA")
for s in students:
    print(s)

students.sort(key=lambda x: x[0])

roll = int(input("\nEnter Roll Number: "))
student = binary_search(students, roll)

if student:
    print("\nStudent Found")
    print(student)
else:
    print("Student Not Found")

print("\nEligible Students")
for s in students:
    if s[2] > 7.5:
        print(s)

roll = int(input("\nEnter Selected Student Roll No: "))
cur.execute("UPDATE students SET status='Placed' WHERE roll=?", (roll,))
con.commit()

print("\nUpdated Student List")
cur.execute("SELECT * FROM students")
for s in cur.fetchall():
    print(s)

con.close()