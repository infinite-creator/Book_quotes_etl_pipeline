def create_tables(conn):
    cursor = conn.cursor()

    #JOBS TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            status TEXT NOT NULL,
            started_at TEXT,
            finished_at TEXT,
            error_message TEXT
        )
    """
    )

    #QUOTES TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quote TEXT NOT NULL,
            author TEXT NOT NULL,
            tags TEXT,
            UNIQUE(quote, author)
        )
    """)
    conn.commit()
