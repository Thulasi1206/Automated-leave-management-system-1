from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Initialize the database
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS Employees (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL DEFAULT 'Employee'
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS LeaveRequests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    employee_id INTEGER NOT NULL,
                    leave_type TEXT NOT NULL,
                    start_date TEXT NOT NULL,
                    end_date TEXT NOT NULL,
                    status TEXT DEFAULT 'Pending',
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

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO Employees (name, email, password, role) VALUES (?, ?, ?, ?)",
                      (name, email, password, role))
            conn.commit()
            flash('Registration successful! Please login.')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Email already exists!')
        finally:
            conn.close()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM Employees WHERE email = ? AND password = ?", (email, password))
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
    conn = sqlite3.connect('database.db')
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

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO LeaveRequests (employee_id, leave_type, start_date, end_date) VALUES (?, ?, ?, ?)",
                  (employee_id, leave_type, start_date, end_date))
        conn.commit()
        conn.close()
        flash('Leave application submitted!')
        return redirect(url_for('employee_dashboard'))
    return render_template('apply_leave.html')

@app.route('/approve_leave/<int:request_id>')
def approve_leave(request_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("UPDATE LeaveRequests SET status = 'Approved' WHERE id = ?", (request_id,))
    conn.commit()
    conn.close()
    flash('Leave request approved!')
    return redirect(url_for('admin_dashboard'))

@app.route('/reject_leave/<int:request_id>')
def reject_leave(request_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("UPDATE LeaveRequests SET status = 'Rejected' WHERE id = ?", (request_id,))
    conn.commit()
    conn.close()
    flash('Leave request rejected!')
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    app.run(debug=True)