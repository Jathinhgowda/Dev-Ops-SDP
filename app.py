from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize the database
def init_db():
    conn = sqlite3.connect('theatre_booking.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        movie_title TEXT NOT NULL,
        showtime TEXT NOT NULL,
        seats INTEGER NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

# Home route - View all bookings
@app.route('/')
def index():
    conn = sqlite3.connect('theatre_booking.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bookings')
    bookings = cursor.fetchall()
    conn.close()
    return render_template('index.html', bookings=bookings)

# Create route - Add a new booking
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        movie_title = request.form['movie_title']
        showtime = request.form['showtime']
        seats = request.form['seats']

        conn = sqlite3.connect('theatre_booking.db')
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO bookings (name, email, movie_title, showtime, seats)
        VALUES (?, ?, ?, ?, ?)
        ''', (name, email, movie_title, showtime, seats))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('create.html')

# Update route - Edit an existing booking
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    conn = sqlite3.connect('theatre_booking.db')
    cursor = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        movie_title = request.form['movie_title']
        showtime = request.form['showtime']
        seats = request.form['seats']

        cursor.execute('''
        UPDATE bookings
        SET name=?, email=?, movie_title=?, showtime=?, seats=?
        WHERE id=?
        ''', (name, email, movie_title, showtime, seats, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    cursor.execute('SELECT * FROM bookings WHERE id = ?', (id,))
    booking = cursor.fetchone()
    conn.close()
    return render_template('update.html', booking=booking)

# Delete route - Delete an existing booking
@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    conn = sqlite3.connect('theatre_booking.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bookings WHERE id = ?', (id,))
    booking = cursor.fetchone()
    if request.method == 'POST':
        cursor.execute('DELETE FROM bookings WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('delete.html', booking=booking)

if __name__ == '__main__':
    init_db()  # Create the database when the app starts
    app.run(debug=True)
