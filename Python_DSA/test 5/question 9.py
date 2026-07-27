'''
 9. Library Book Borrowing System
### Problem Statement
A library stores books and borrowing history.
Tables:
Books
Members
Borrowed Books
### Requirements
1. Display all available books.
2. Sort books alphabetically using **Merge Sort**.
3. Search books by Book ID.
4. Borrow a book.
5. Update book availability.
6. Display overdue books.
### Concepts
* Merge Sort
* Binary Search
* SQLite
* SQL UPDATE
'''

import sqlite3

def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    result = []

    i = j = 0
    while i < len(left) and j < len(right):
        if left[i][1] < right[j][1]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    return result + left[i:] + right[j:]

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

con = sqlite3.connect("library.db")
cur = con.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS Books(
    book_id INTEGER PRIMARY KEY,
    title TEXT,
    available TEXT,
    overdue TEXT
)
""")

cur.execute("SELECT COUNT(*) FROM Books")
if cur.fetchone()[0] == 0:
    books = [
        (101,"Python","Yes","No"),
        (102,"DBMS","Yes","No"),
        (103,"Operating System","No","Yes"),
        (104,"Computer Networks","Yes","No"),
        (105,"Data Structures","Yes","No")
    ]
    cur.executemany("INSERT INTO Books VALUES(?,?,?,?)", books)
    con.commit()

cur.execute("SELECT * FROM Books WHERE available='Yes'")
books = cur.fetchall()

books = merge_sort(books)

print("Available Books")
for b in books:
    print(b)

search_list = sorted(books, key=lambda x: x[0])

bid = int(input("\nEnter Book ID: "))
book = binary_search(search_list, bid)

if book:
    print("\nBook Found")
    print(book)

    cur.execute("UPDATE Books SET available='No' WHERE book_id=?", (bid,))
    con.commit()
    print("Book Borrowed Successfully")
else:
    print("Book Not Found")

print("\nOverdue Books")
cur.execute("SELECT * FROM Books WHERE overdue='Yes'")
for row in cur.fetchall():
    print(row)

con.close()