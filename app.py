from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql+mysqlconnector://appointment_user:password@localhost/appointment_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Doctor(db.Model):
    __tablename__ = 'doctors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    appointment_capacity = db.Column(db.Integer)

class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    doctor_id = db.Column(db.Integer)
    __table_args__ = (db.UniqueConstraint('user_id', 'doctor_id', name='_user_doctor_uc'),)

@app.route('/getTicket', methods=['POST'])
def get_ticket():
    logging.debug("Request received at /getTicket")
    data = request.get_json()
    logging.debug(f"Request data: {data}")
    user_id = data.get('userId')
    doctor_id = data.get('doctorId')

    doctor = Doctor.query.filter_by(id=doctor_id).first()
    logging.debug(f"Doctor found: {doctor}")
    if not doctor:
        logging.debug("Doctor not found")
        return jsonify({"message": "Doctor not found"}), 404

    appointment_count = Appointment.query.filter_by(doctor_id=doctor_id).count()
    logging.debug(f"Appointment count: {appointment_count}")
    if appointment_count >= doctor.appointment_capacity:
        logging.debug("No appointments available")
        return jsonify({"message": "No appointments available"}), 400

    existing_appointment = Appointment.query.filter_by(user_id=user_id, doctor_id=doctor_id).first()
    logging.debug(f"Existing appointment: {existing_appointment}")
    if existing_appointment:
        logging.debug("User already has an appointment")
        return jsonify({"message": "User already has an appointment"}), 400

    new_appointment = Appointment(user_id=user_id, doctor_id=doctor_id)
    db.session.add(new_appointment)
    db.session.commit()
    logging.debug("Appointment booked")

    return jsonify({"message": "Appointment booked"}), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    from waitress import serve
    from app import app
    serve(app, host='127.0.0.1', port=5000, threads=8, connection_limit=100, backlog=100)
