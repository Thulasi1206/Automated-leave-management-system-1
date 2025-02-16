 Automated Leave Management System

The **Automated Leave Management System** is a web-based application designed to streamline the process of managing employee leave requests. Built with **Python Flask** for the backend and **MySQL** for the database, this system provides an intuitive interface for employees to submit leave requests and for managers to review and manage them efficiently.

## Key Features
- **Employee Leave Request Submission**:
  - Employees can submit leave requests with details such as name, email, leave dates, and reason.
- **Manager Dashboard**:
  - Managers can view all leave requests in a centralized dashboard.
  - Displays employee details, leave dates, reasons, and current status (e.g., Pending, Approved, Rejected).
- **Automated Workflow**:
  - Simplifies the leave approval process, reducing manual effort and paperwork.
- **User-Friendly Interface**:
  - Clean and responsive design for easy navigation and usage.

## Technologies Used
- **Frontend**: HTML, CSS
- **Backend**: Python Flask
- **Database**: MySQL
- **Deployment**: Localhost (can be extended to cloud platforms like Heroku, AWS, etc.)

## Installation and Setup
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Srikanthvatrapu/Automated-leave-management-system.git
Install Dependencies:

bash
Copy
pip install -r requirements.txt
Set Up the Database:

Create a MySQL database named leave_management.

Run the following SQL commands to create the leave_requests table:

sql
Copy
CREATE DATABASE leave_management;
USE leave_management;
CREATE TABLE leave_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    reason TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'Pending'
);
Run the Application:

bash
Copy
python app.py
Access the Application:

Employee Leave Request Form: http://127.0.0.1:5000/

Manager Dashboard: http://127.0.0.1:5000/manager

Usage
For Employees:

Visit the leave request form, fill in the required details, and submit your leave request.

For Managers:

Access the manager dashboard to view all leave requests and their current status.

Contributing
Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

Fork the repository.

Create a new branch for your feature or bugfix.

Commit your changes and push to the branch.

Submit a pull request with a detailed description of your changes.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Contact
For any questions or feedback, feel free to reach out:

Email: srikanthreddyvatrapu@gmail.com

GitHub: https://github.com/Srikanthvatrapu
