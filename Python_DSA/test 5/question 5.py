'''
# 5. Movie Recommendation System
### Problem Statement
A streaming platform stores movie information.
Each movie contains
* Movie ID
* Title
* Genre
* Rating
* Watch Count
### Requirements
1. Fetch all movies.
2. Sort movies based on Rating.
3. Search a movie using Movie ID.
4. Display Top 10 highest-rated movies.
5. Display the most watched movie in every genre.
### Concepts
* Sorting
* Searching
* Dictionaries
* SQL GROUP BY
'''



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

con = sqlite3.connect("movies.db")
cur = con.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS movies(
    movie_id INTEGER PRIMARY KEY,
    title TEXT,
    genre TEXT,
    rating REAL,
    watch_count INTEGER
)
""")

cur.execute("SELECT COUNT(*) FROM movies")
if cur.fetchone()[0] == 0:
    data = [
        (101,"Inception","Sci-Fi",9.2,500),
        (102,"Avengers","Action",8.8,700),
        (103,"Titanic","Romance",9.0,650),
        (104,"Interstellar","Sci-Fi",9.5,800),
        (105,"John Wick","Action",8.9,750),
        (106,"The Notebook","Romance",8.5,450),
        (107,"Avatar","Sci-Fi",8.7,900),
        (108,"Joker","Drama",9.1,850),
        (109,"3 Idiots","Comedy",9.4,950),
        (110,"Bahubali","Action",8.6,600)
    ]
    cur.executemany("INSERT INTO movies VALUES(?,?,?,?,?)", data)
    con.commit()

cur.execute("SELECT * FROM movies")
movies = cur.fetchall()

movies.sort(key=lambda x: x[3], reverse=True)

print("Movies Sorted by Rating")
for m in movies:
    print(m)

search_list = sorted(movies, key=lambda x: x[0])

mid = int(input("\nEnter Movie ID: "))
movie = binary_search(search_list, mid)

if movie:
    print("\nMovie Found")
    print(movie)
else:
    print("Movie Not Found")

print("\nTop 10 Highest Rated Movies")
for m in movies[:10]:
    print(m)

print("\nMost Watched Movie in Each Genre")
genres = {}

for m in movies:
    if m[2] not in genres or m[4] > genres[m[2]][4]:
        genres[m[2]] = m

for movie in genres.values():
    print(movie)

con.close()