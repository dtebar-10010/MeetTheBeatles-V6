import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

print("=" * 60)
print("DATABASE VERIFICATION REPORT")
print("=" * 60)
print(f"\nTotal tables: {len(tables)}\n")

for table in tables:
    table_name = table[0]
    cursor.execute(f'SELECT COUNT(*) FROM "{table_name}"')
    count = cursor.fetchone()[0]
    print(f"{table_name}: {count} rows")

# Check specific tables for the project
print("\n" + "=" * 60)
print("PROJECT-SPECIFIC TABLE DETAILS")
print("=" * 60)

# Check Page table
try:
    cursor.execute("SELECT COUNT(*) FROM mtb_v5_app_page")
    page_count = cursor.fetchone()[0]
    cursor.execute("SELECT phase, COUNT(*) FROM mtb_v5_app_page GROUP BY phase ORDER BY phase")
    pages_by_phase = cursor.fetchall()
    print(f"\nPage table: {page_count} total pages")
    print("Pages by phase:")
    for phase, count in pages_by_phase:
        print(f"  Phase {phase}: {count} pages")
except Exception as e:
    print(f"\nError checking Page table: {e}")

# Check Media table
try:
    cursor.execute("SELECT COUNT(*) FROM mtb_v5_app_media")
    media_count = cursor.fetchone()[0]
    print(f"\nMedia table: {media_count} total media items")
except Exception as e:
    print(f"\nError checking Media table: {e}")

# Check History table
try:
    cursor.execute("SELECT COUNT(*) FROM mtb_v5_app_history")
    history_count = cursor.fetchone()[0]
    print(f"\nHistory table: {history_count} total history entries")
except Exception as e:
    print(f"\nError checking History table: {e}")

conn.close()
print("\n" + "=" * 60)
