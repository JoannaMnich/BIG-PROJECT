import sqlite3

class bookDAO:
    def __init__(self):
        # The path to the SQLite database file. 
        self.db_path = '/home/JMnich/mysite/books.db'
        # Call the method to create the table if it doesn't exist
        self.create_table_if_not_exists()

    def get_connection(self):
        # SQLite connects to a file-based database, so I specify the path to the .db file
        conn = sqlite3.connect(self.db_path)
        # Row factory allows us to access columns by name, which is more convenient
        conn.row_factory = sqlite3.Row
        return conn

    def create_table_if_not_exists(self):
        db = self.get_connection()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                author TEXT,
                year INTEGER,
                price REAL,
                description TEXT
            )
        ''')
        db.commit()
        db.close()

    def get_all(self):
        db = self.get_connection()
        cursor = db.cursor()
        cursor.execute("SELECT id, title, author, year, price, description FROM books")
        rows = cursor.fetchall()
        # Convert rows to a list of dictionaries for easier handling in the application
        result = [dict(row) for row in rows]
        db.close()
        return result

    def create(self, book):
        db = self.get_connection()
        cursor = db.cursor()
        # In SQLite, ? is used as placeholders instead of %s 
        sql = "INSERT INTO books (title, author, year, price) VALUES (?, ?, ?, ?)"
        values = (book['Title'], book['Author'], book['Year'], book['Price'])
        cursor.execute(sql, values)
        db.commit()
        new_id = cursor.lastrowid
        db.close()
        return new_id

    def delete(self, id):
        db = self.get_connection()
        cursor = db.cursor()
        sql = "DELETE FROM books WHERE id = ?"
        cursor.execute(sql, (id,))
        db.commit()
        db.close()
        return True

    def update(self, id, book):
        db = self.get_connection()
        cursor = db.cursor()
        sql = "UPDATE books SET title=?, author=?, year=?, price=? WHERE id=?"
        values = (book.get('Title'), book.get('Author'), book.get('Year'), book.get('Price'), id)
        cursor.execute(sql, values)
        db.commit()
        db.close()
        return True

    def find_by_id(self, id):
        db = self.get_connection()
        cursor = db.cursor()
        sql = "SELECT * FROM books WHERE id = ?"
        cursor.execute(sql, (id,))
        row = cursor.fetchone()
        db.close()
        return dict(row) if row else None

    def update_description(self, id, description):
        db = self.get_connection()
        cursor = db.cursor()
        sql = "UPDATE books SET description = ? WHERE id = ?"
        cursor.execute(sql, (description, id))
        db.commit()
        db.close()

# Initialization of the bookDAO
book_dao = bookDAO()