import sqlite3

class MovieDatabase:
    def __init__(self):
        self.conn = sqlite3.connect('movies.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                author TEXT,
                year INTEGER
            )
        ''')
        self.conn.commit()

    def add_movie(self, title, author, year):
        self.cursor.execute('INSERT INTO movies (title, author, year) VALUES (?, ?, ?)', (title, author, year))
        self.conn.commit()

    def update_movie(self, movie_id, title, author, year):
        self.cursor.execute('UPDATE movies SET title=?, author=?, year=? WHERE id=?', (title, author, year, movie_id))
        self.conn.commit()

    def delete_movie(self, movie_id):
        self.cursor.execute('DELETE FROM movies WHERE id=?', (movie_id,))
        self.conn.commit()

    def get_all_movies(self):
        self.cursor.execute('SELECT * FROM movies')
        return self.cursor.fetchall()

    def get_movie_by_id(self, movie_id):
        self.cursor.execute('SELECT * FROM movies WHERE id=?', (movie_id,))
        return self.cursor.fetchone()

    def search_movie_by_title(self, title):
        self.cursor.execute('SELECT * FROM movies WHERE title LIKE ?', ('%' + title + '%',))
        return self.cursor.fetchall()

    def get_movie_count(self):
        self.cursor.execute('SELECT COUNT(*) FROM movies')
        return self.cursor.fetchone()[0]

    def close(self):
        self.conn.close()
