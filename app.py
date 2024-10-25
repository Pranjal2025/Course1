from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import errorcode

app = Flask(__name__)

# Database connection setup
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host='database1.c764ie00s14k.ap-southeast-2.rds.amazonaws.com',      # Change if your MySQL server is running elsewhere
            user='admin1',  # Your MySQL username
            password='pranjalpawara',  # Your MySQL password
            database='courses'     # The database/schema you created
        )
        print("Database connection established.")  # Debug line
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        return None

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Apply route (handles form submission)
@app.route('/apply', methods=['POST'])
def apply():
    if request.method == 'POST':
        course = request.form.get('course')
        name = request.form.get('name')
        email = request.form.get('email')

        print(f"Received: Name: {name}, Email: {email}, Course: {course}")  # Debug line

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute('INSERT INTO applications (name, email, course) VALUES (%s, %s, %s)', (name, email, course))
                conn.commit()
                print(f"Inserted {cursor.rowcount} row(s) into applications.")  # Debug line
            except mysql.connector.Error as err:
                print(f"Error: {err}")  # Print error if any
            finally:
                cursor.close()
                conn.close()
        
        return redirect(url_for('index'))

# Main entry point
if __name__ == '__main__':
    app.run(debug=True)
