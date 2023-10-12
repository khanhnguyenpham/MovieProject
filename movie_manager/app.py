from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  

def connect_db():
    return sqlite3.connect('movies.db')

def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            year INTEGER
        )
    ''')
    conn.commit()
    conn.close()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_movie', methods=['POST'])
def add_movie():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO movies (title, author, year) VALUES (?, ?, ?)', (title, author, year))
        conn.commit()
        conn.close()
        flash('Phim đã được thêm thành công!', 'success')
        return redirect(url_for('list_movies'))

@app.route('/list_movies')
def list_movies():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM movies')
    movies = cursor.fetchall()
    conn.close()
    return render_template('result.html', movies=movies)

@app.route('/view_movie/<int:id>')
def view_movie(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM movies WHERE id = ?', (id,))
    movie = cursor.fetchone()
    conn.close()
    if movie:
        return render_template('view.html', movie=movie)
    flash('Phim không tồn tại!', 'danger')
    return redirect(url_for('list_movies'))

@app.route('/edit_movie/<int:id>', methods=['GET', 'POST'])
def edit_movie(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM movies WHERE id = ?', (id,))
    movie = cursor.fetchone()
    conn.close()
    if not movie:
        flash('Phim không tồn tại!', 'danger')
        return redirect(url_for('list_movies'))
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('UPDATE movies SET title = ?, author = ?, year = ? WHERE id = ?', (title, author, year, id))
        conn.commit()
        conn.close()
        flash('Thông tin phim đã được cập nhật thành công!', 'success')
        return redirect(url_for('list_movies'))
    return render_template('edit.html', movie=movie)

@app.route('/delete_movie/<int:id>')
def delete_movie(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM movies WHERE id = ?', (id,))
    movie = cursor.fetchone()
    if not movie:
        flash('Phim không tồn tại!', 'danger')
    else:
        cursor.execute('DELETE FROM movies WHERE id = ?', (id,))
        conn.commit()
        flash('Phim đã được xóa thành công!', 'success')
    conn.close()
    return redirect(url_for('list_movies'))

if __name__ == '__main__':
    create_table()
    app.run(debug=True)

