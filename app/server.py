from flask import Flask, request, render_template, redirect, url_for, session
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'bb92a37c7afa4718bf814d96b0aa78d46c4ca2666e4b2de829aea4e436bcf987'  
                                # Change to a strong, secure key in production
                                # Required to create a session.

# Database Configuration
db_config = {
    'host': 'mariadb',    # Change to you MySQL hostname/ip
    'user': 'appuser',       # Change to your MySQL username
    'password': 'appuser@123', # Change to your MySQL password
    'database': 'productdb'
}


# Connect to the database
def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        print("Database connection error:", e)
        return None

# Home Page
@app.route('/home', methods=['GET'])
def home():
    return render_template('login.html')


# Login Route
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Vulnerable query (for demonstration purposes)
    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    print("Executing SQL:", query)
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    cursor.close()
    connection.close()

    if user:
        session['username'] = user[1]
        return redirect(url_for('welcome'))
    else:
        return render_template('failed.html')


# Welcome Route
@app.route('/welcome')
def welcome():
    if 'username' not in session:
        return redirect(url_for('home'))
    return render_template('welcome.html', username=session['username'])

# Products Route
@app.route('/products')
def products():
    if 'username' not in session:
        return redirect(url_for('home'))

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template('products.html', products=products)

# Delete Product Route (Demonstrates SQL Injection vulnerability)
@app.route('/delete_product/<product_id>', methods=['GET'])
def delete_product(product_id):
    if 'username' not in session:
        return redirect(url_for('home'))

    # Vulnerable query
    query = "DELETE FROM products WHERE id = %s"
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(query, (product_id,))
    connection.commit()
    cursor.close()
    connection.close()

    return redirect(url_for('products'))

# Logout Route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

# Run the app
if __name__ == '__main__':
    app.run(port=4000,host='0.0.0.0', debug=True)
