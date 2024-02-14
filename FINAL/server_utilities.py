import sqlite3

# Connect to an SQLite database (creates a new file if it doesn't exist)
conn = sqlite3.connect('my_database.db')

# Create a cursor
cursor = conn.cursor()

# Create a table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY,
        name TEXT,
        age INTEGER
    )
''')

# Insert data
cursor.execute('''
    INSERT INTO students (name, age) VALUES (?, ?)
''', ('Alice', 22),)
conn.commit()

# Query data
cursor.execute('SELECT * FROM students')
rows = cursor.fetchall()

for row in rows:
    print(row)

# Update and delete data
cursor.execute('UPDATE students SET age = ? WHERE name = ?', (23, 'Alice'))
cursor.execute('DELETE FROM students WHERE name = ?', ('Alice',))
conn.commit()

# Close the connection
conn.close()
