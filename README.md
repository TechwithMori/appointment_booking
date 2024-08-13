# Appointment Booking Service

## Overview

This project is a simple appointment booking service built using Flask and MySQL. The service includes a web service endpoint called `getTicket`, which allows users to book appointments with a doctor, provided that it does not exceed the doctor's appointment capacity.

## Features

- Book an appointment with a doctor using a POST request.
- Ensure that each user can only book an appointment with a doctor once.
- Prevent booking if the doctor's appointment capacity is exceeded.
- Scalable and tested with concurrent requests.

## Requirements

- Python 3.8+
- Flask
- Flask-SQLAlchemy
- MySQL
- Waitress (for serving the application)

## Installation

1. **Clone the Repository**:
   ```sh
   git clone https://github.com/TechwithMori/appointment_booking.git
   cd appointment_booking
   ```

2. **Create and Activate Virtual Environment**:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```sh
   pip install Flask Flask-SQLAlchemy mysql-connector-python pytest
   ```

4. **Set your Database**:
   - Use a MySQL Client such as "MySQL Command Line Client" to create your database and user
  
5. **Configure the Database**:
   - Update the database URL in 'app.py' to match your MySQL configuration.
   ```sh
   app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://appointment_user:password@localhost/appointment_db'
   ```

6. **Unit Tests**:
   - After cloning the repository, you can run the unit tests to ensure that the service is working correctly. To do so, use the following command:
   ```sh
   pytest tests/test_app.py
   ```

## Usage

1. **Run the Flask Application**:
   ```sh
   python app.py
   ```

2. **Test the API**:
   - Use Postman or a similar tool to send a POST request to 'http://127.0.0.1:5000/getTicket' with the following JSON body:
   ```sh
   {
    "userId": 1,
    "doctorId": 1
   }
   ```


## Performance Test

1. **Run the Performance Test**:
   - In another terminal run the performance test. The performance test script sends 100 concurrent requests to the service.
   ```sh
   python performance_test.py
   ```

2. **Expected Output**:
   - The first user should successfully book an appointment.
   - All subsequent users should receive a "No appointments available" message.


## Contribution
- Feel free to submit issues or pull requests. For major changes, please open an issue first to discuss what you would like to change.
