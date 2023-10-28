from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

db_config = {
    'host': 'host.docker.internal',
    'database': 'flask_crud_app_db',
    'user': 'postgres',
    'password': 'ilya20122018',
}

@app.route('/')
def index():
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    data = cur.fetchall()
    conn.close()
    return render_template('index.html', data=data)

@app.route('/create', methods=['POST'])
def create():
    if request.method == 'POST':
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        name = request.form['name']
        email = request.form['email']
        cur.execute('INSERT INTO users (name, email) VALUES (%s, %s)', (name, email))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    if request.method == 'POST':
   
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()

        name = request.form['name']
        email = request.form['email']
        cur.execute('UPDATE users SET name = %s, email = %s WHERE id = %s', (name, email, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))




@app.route('/delete/<int:id>')
def delete(id):
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()
    cur.execute('DELETE FROM users WHERE id = %s', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)