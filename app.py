from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from dotenv import load_dotenv
load_dotenv()

import db_config

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['MYSQL_HOST'] = db_config.MYSQL_HOST
app.config['MYSQL_USER'] = db_config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = db_config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = db_config.MYSQL_DB

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM employees")
    employees = cur.fetchall()
    cur.close()
    return render_template('index.html', employees=employees)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        position = request.form['position']
        salary = request.form['salary']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO employees (name, email, phone, position, salary) VALUES (%s, %s, %s, %s, %s)",
                    (name, email, phone, position, salary))
        mysql.connection.commit()
        cur.close()
        flash('Employee added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        position = request.form['position']
        salary = request.form['salary']
        cur.execute("UPDATE employees SET name=%s, email=%s, phone=%s, position=%s, salary=%s WHERE id=%s",
                    (name, email, phone, position, salary, id))
        mysql.connection.commit()
        cur.close()
        flash('Employee updated successfully!', 'warning')
        return redirect(url_for('index'))
    cur.execute("SELECT * FROM employees WHERE id=%s", (id,))
    employee = cur.fetchone()
    cur.close()
    if employee:
        return render_template('edit.html', employee={
            'id': employee[0],
            'name': employee[1],
            'email': employee[2],
            'phone': employee[3],
            'position': employee[4],
            'salary': employee[5]
        })
    flash('Employee not found!', 'danger')
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM employees WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    flash('Employee deleted successfully!', 'danger')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
