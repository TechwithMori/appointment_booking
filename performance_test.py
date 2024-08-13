import requests
import threading
import time
from app import app, db, Doctor

def reset_database():
    # Reset the database state
    with app.app_context():
        db.drop_all()
        db.create_all()
        # Add a doctor with a 1 appointment capacity
        doctor = Doctor(id=1, name='Dr. John', appointment_capacity=1)
        db.session.add(doctor)
        db.session.commit()

def send_request(user_id):
    url = 'http://127.0.0.1:5000/getTicket'
    payload = {'userId': user_id, 'doctorId': 1}
    try:
        response = requests.post(url, json=payload, timeout=10)
        print(f"User {user_id} response: {response.status_code}, {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"User {user_id} request failed: {e}")

# Reset the database state before starting the test
reset_database()

threads = []
for i in range(1, 101):  # Unique userIds from 1 to 100
    thread = threading.Thread(target=send_request, args=(i,))
    threads.append(thread)
    thread.start()
    time.sleep(0.1)  # Stagger thread starts to avoid overwhelming the server

for thread in threads:
    thread.join()
