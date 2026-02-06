from app import app, User
from sqlalchemy import inspect

with app.app_context():
    inst = inspect(User)
    columns = [c.key for c in inst.mapper.column_attrs]
    print(f"Columns in User table: {columns}")
    if 'trip_count' in columns:
        print("SUCCESS: trip_count column exists.")
    else:
        print("FAILURE: trip_count column is missing.")
