import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import app, db, Doctor, Appointment

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

def test_get_ticket_success(client):
    doctor = Doctor(id=1, name='Dr. John', appointment_capacity=5)
    db.session.add(doctor)
    db.session.commit()

    response = client.post('/getTicket', json={"userId": 1, "doctorId": 1})
    assert response.status_code == 201
    assert response.get_json()['message'] == 'Appointment booked'

def test_get_ticket_no_capacity(client):
    doctor = Doctor(id=1, name='Dr. John', appointment_capacity=1)
    db.session.add(doctor)
    db.session.commit()

    client.post('/getTicket', json={"userId": 1, "doctorId": 1})
    response = client.post('/getTicket', json={"userId": 2, "doctorId": 1})
    assert response.status_code == 400
    assert response.get_json()['message'] == 'No appointments available'

def test_get_ticket_user_already_has_appointment(client):
    doctor = Doctor(id=1, name='Dr. John', appointment_capacity=5)
    db.session.add(doctor)
    db.session.commit()

    client.post('/getTicket', json={"userId": 1, "doctorId": 1})
    response = client.post('/getTicket', json={"userId": 1, "doctorId": 1})
    assert response.status_code == 400
    assert response.get_json()['message'] == 'User already has an appointment'
