import sqlite3

DATABASE = "TikTok.db"
VIDEOS_TABLE = "videos"
UPLOADED_VIDEOS_TABLE = "uploaded_videos"


# Creating the tables
def create_table(cursor, name_table):
    cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {name_table} (
            id INTEGER PRIMARY KEY,
            url TEXT NOT NULL,
            name TEXT,
            hashtags TEXT,
            likes INTEGER, 
            date TEXT,
            song TEXT )
        """)


# Db connection
def connect_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()

        create_table(cursor, VIDEOS_TABLE)
        create_table(cursor, UPLOADED_VIDEOS_TABLE)

        conn.commit()


# Inserting data to the table
def insert_data(name_table, url, name, hashtags, likes, date, song):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()

        cursor.execute(f"""
            INSERT INTO {name_table} (url, name, hashtags, likes, date, song) VALUES (?, ?, ?, ?, ?, ?) 
        """, (url, name, hashtags, likes, date, song))

        conn.commit()


# Getting record with this url
def check_url(cursor, name_table, url):
    cursor.execute(f"""
        SELECT url 
        FROM {name_table} 
        WHERE url = ?
    """, (url,))

    return cursor.fetchone()


# Checking on exists this video in the tables
def existence_check(url):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()

        if check_url(cursor, VIDEOS_TABLE, url) or check_url(cursor, UPLOADED_VIDEOS_TABLE, url):
            return True
        else:
            return False


# Sorting by field "likes"
def sorted_by_likes(tag):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()

        cursor.execute(f"""
            SELECT url, name, hashtags, likes, date, song 
            FROM {VIDEOS_TABLE} 
            WHERE hashtags LIKE ?
            ORDER BY likes DESC
        """, ('%' + tag + '%',))

        try:
            first_record = cursor.fetchone()
            cursor.close()

            insert_data(UPLOADED_VIDEOS_TABLE, *first_record)
            delete_from_table(first_record[1])
            conn.commit()

            return first_record[1]
        except Exception:
            print(f"Can't find record with this tag: {tag}")


# Deleting from the table
def delete_from_table(name):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()

        cursor.execute(f"""
            DELETE
            FROM {VIDEOS_TABLE}
            WHERE name = ?
        """, (name, ))

