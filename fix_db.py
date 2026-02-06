import sqlite3
import os

# Define all possible locations where the database might be hiding
possible_paths = [
    os.path.join(os.getcwd(), 'instance', 'tarist.db'),
    os.path.join(os.getcwd(), 'tarist.db'),
    r'd:\moath\i spark\tarist web\New folder (2)\instance\tarist.db',
    r'd:\moath\i spark\tarist web\New folder (2)\tarist.db'
]

def fix_database():
    print("Starting database fix...")
    for path in possible_paths:
        if os.path.exists(path):
            print(f"Checking database at: {path}")
            try:
                # Direct SQL connection is more reliable than SQLAlchemy for simple ALTERS
                conn = sqlite3.connect(path)
                cursor = conn.cursor()
                
                # Check current columns
                cursor.execute("PRAGMA table_info(user)")
                columns = [info[1] for info in cursor.fetchall()]
                
                if 'trip_count' not in columns:
                    print(f"Adding trip_count column to {path}")
                    cursor.execute("ALTER TABLE user ADD COLUMN trip_count INTEGER DEFAULT 0")
                    conn.commit()
                    print("Column added successfully.")
                else:
                    print(f"trip_count already exists in {path}")
                
                conn.close()
            except Exception as e:
                print(f"Could not fix database at {path}: {e}")
        else:
            print(f"No database found at: {path}")

if __name__ == "__main__":
    fix_database()
