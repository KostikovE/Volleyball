import sqlite3

conn = sqlite3.connect("data/app.db")

tables = [r[0] for r in conn.execute(
    "SELECT name FROM sqlite_master WHERE type='table'"
)]
print("Таблицы:", tables)

for table in tables:
    if table == "alembic_version":
        continue
    cols = [r[1] for r in conn.execute(f"PRAGMA table_info({table})")]
    print(f"{table}: {cols}")

print("alembic_version:", conn.execute("SELECT * FROM alembic_version").fetchall())

conn.close()