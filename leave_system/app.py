from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",       # Change if your MySQL is hosted elsewhere
        user="root",  # Replace with your MySQL username
        password="root",  # Replace with your MySQL password
        database="leavemanagement"  # Replace with your MySQL database name
    )

# Initialize the database
def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS Employees (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    role VARCHAR(50) NOT NULL DEFAULT 'Employee'
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS LeaveRequests (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    employee_id INT NOT NULL,
                    leave_type VARCHAR(255) NOT NULL,
                    start_date DATE NOT NULL,
                    end_date DATE NOT NULL,
                    status VARCHAR(50) DEFAULT 'Pending',
                    FOREIGN KEY (employee_id) REFERENCES Employees(id)
                )''')
    conn.commit()
    conn.close()

# Initialize the database when the app starts
init_db()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        conn = get_db_connection()
        c = conn.cursor()
        try:
            c.execute("INSERT INTO Employees (name, email, password, role) VALUES (%s, %s, %s, %s)",
                      (name, email, password, role))
            conn.commit()
            flash('Registration successful! Please login.')
            return redirect(url_for('login'))
        except mysql.connector.IntegrityError:
            flash('Email already exists!')
        finally:
            conn.close()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM Employees WHERE email = %s AND password = %s", (email, password))
        user = c.fetchone()
        conn.close()

        if user:
            if user[4] == 'Admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('employee_dashboard'))
        else:
            flash('Invalid credentials!')
    return render_template('login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT LeaveRequests.id, Employees.name, leave_type, start_date, end_date, status FROM LeaveRequests JOIN Employees ON LeaveRequests.employee_id = Employees.id")
    requests = c.fetchall()
    conn.close()
    return render_template('admin_dashboard.html', requests=requests)

@app.route('/employee/dashboard')
def employee_dashboard():
    return render_template('employee_dashboard.html')

@app.route('/apply_leave', methods=['GET', 'POST'])
def apply_leave():
    if request.method == 'POST':
        employee_id = 1  # Replace with logged-in user's ID
        leave_type = request.form['leave_type']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        conn = get_db_connection()
        c = conn.cursor()
        c.execute("INSERT INTO LeaveRequests (employee_id, leave_type, start_date, end_date) VALUES (%s, %s, %s, %s)",
                  (employee_id, leave_type, start_date, end_date))
        conn.commit()
        conn.close()
        flash('Leave application submitted!')
        return redirect(url_for('employee_dashboard'))
    return render_template('apply_leave.html')

@app.route('/approve_leave/<int:request_id>')
def approve_leave(request_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("UPDATE LeaveRequests SET status = 'Approved' WHERE id = %s", (request_id,))
    conn.commit()
    conn.close()
    flash('Leave request approved!')
    return redirect(url_for('admin_dashboard'))

@app.route('/reject_leave/<int:request_id>')
def reject_leave(request_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("UPDATE LeaveRequests SET status = 'Rejected' WHERE id = %s", (request_id,))
    conn.commit()
    conn.close()
    flash('Leave request rejected!')
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
