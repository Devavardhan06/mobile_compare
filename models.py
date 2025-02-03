import sqlite3
import os

# Step 1: Delete old database file (if it exists)
if os.path.exists("database.db"):
    os.remove("database.db")
    print("Old database deleted.")

# Step 2: Create a new SQLite database
conn = sqlite3.connect("database.db")  # Creates database.db file
cursor = conn.cursor()  # Create a cursor to execute SQL commands

# Step 3: Create 'mobiles' table
cursor.execute('''
    CREATE TABLE mobiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        brand TEXT NOT NULL,
        model TEXT NOT NULL,
        display TEXT,
        battery TEXT,
        camera TEXT,
        processor TEXT,
        pros TEXT,
        cons TEXT
    )
''')
print("New 'mobiles' table created.")

# Step 4: Insert Sample Data
cursor.execute("INSERT INTO mobiles (brand, model, display, battery, camera, processor, pros, cons) VALUES \
                ('Samsung', 'Galaxy S23', '6.1-inch AMOLED', '3900mAh', '50MP', 'Snapdragon 8 Gen 2', \
                'Great Display, Fast Performance', 'Expensive')")

# Step 5: Save changes and close the database connection
conn.commit()
conn.close()

print("Database setup complete! 🎉")
