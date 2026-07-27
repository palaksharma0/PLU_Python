'''# 1. Smart Inventory Management System
### Problem Statement
An e-commerce warehouse stores product information in an SQLite database.
Each product has:
* Product ID
* Product Name
* Category
* Quantity
* Price
### Requirements
1. Fetch all products from the SQLite database.
2. Store them in Python objects.
3. Sort the products based on quantity using **Merge Sort**.
4. Allow the manager to search for a Product ID using **Binary Search**.
5. Display the complete product details.
6. Display products whose stock is below 10.
### Concepts
* SQLite
* Python Classes
* Merge Sort
* Binary Search
* SQL SELECT
'''

import sqlite3

class Product:
    def __init__(self, pid, name, category, quantity, price):
        self.pid = pid
        self.name = name
        self.category = category
        self.quantity = quantity
        self.price = price

    def display(self):
        print(f"{self.pid}\t{self.name}\t{self.category}\t{self.quantity}\t{self.price}")

conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS products(
    product_id INTEGER PRIMARY KEY,
    product_name TEXT,
    category TEXT,
    quantity INTEGER,
    price REAL
)
""")

cursor.execute("SELECT COUNT(*) FROM products")
count = cursor.fetchone()[0]

if count == 0:
    data = [
        (101, "Laptop", "Electronics", 15, 55000),
        (102, "Mouse", "Electronics", 8, 600),
        (103, "Keyboard", "Electronics", 20, 1200),
        (104, "Chair", "Furniture", 5, 3500),
        (105, "Table", "Furniture", 12, 6500),
        (106, "Monitor", "Electronics", 7, 12000)
    ]
    cursor.executemany("INSERT INTO products VALUES(?,?,?,?,?)", data)
    conn.commit()

cursor.execute("SELECT * FROM products")
rows = cursor.fetchall()

products = []

for row in rows:
    products.append(Product(row[0], row[1], row[2], row[3], row[4]))

def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i].quantity < right[j].quantity:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result

def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def binary_search(arr, key):
    low = 0
    high = len(arr) - 1

    while low <= high:
        mid = (low + high) // 2

        if arr[mid].pid == key:
            return arr[mid]
        elif arr[mid].pid < key:
            low = mid + 1
        else:
            high = mid - 1

    return None

def display_products(arr):
    print("\nID\tName\tCategory\tQuantity\tPrice")
    print("-" * 60)

    for p in arr:
        p.display()

def low_stock(arr):
    print("\nProducts with Stock Below 10")
    print("-" * 40)

    found = False

    for p in arr:
        if p.quantity < 10:
            p.display()
            found = True

    if not found:
        print("No products found.")

while True:
    print("\n===== SMART INVENTORY MANAGEMENT =====")
    print("1. Display All Products")
    print("2. Sort by Quantity")
    print("3. Search Product by ID")
    print("4. Display Low Stock Products")
    print("5. Exit")

    choice = int(input("Enter Choice: "))

    if choice == 1:
        display_products(products)

    elif choice == 2:
        products = merge_sort(products)
        display_products(products)

    elif choice == 3:
        products.sort(key=lambda x: x.pid)
        pid = int(input("Enter Product ID: "))
        result = binary_search(products, pid)

        if result:
            print("\nID\tName\tCategory\tQuantity\tPrice")
            result.display()
        else:
            print("Product Not Found")

    elif choice == 4:
        low_stock(products)

    elif choice == 5:
        break

    else:
        print("Invalid Choice")

conn.close()