from flask import Flask, render_template, request, jsonify, redirect, url_for
import cv2
import face_recognition
import numpy as np
import os
import json
import time
from datetime import datetime
import pickle

app = Flask(__name__)

# Directories
KNOWN_FACES_DIR = 'known_faces'
ATTENDANCE_DIR = 'attendance'
ENCODINGS_FILE = 'face_encodings.pkl'

# Ensure directories exist
os.makedirs(KNOWN_FACES_DIR, exist_ok=True)
os.makedirs(ATTENDANCE_DIR, exist_ok=True)

# Load or create face encodings
def load_face_encodings():
    if os.path.exists(ENCODINGS_FILE):
        with open(ENCODINGS_FILE, 'rb') as f:
            return pickle.load(f)
    return {}

def save_face_encodings(encodings):
    with open(ENCODINGS_FILE, 'wb') as f:
        pickle.dump(encodings, f)

face_encodings_db = load_face_encodings()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/mark_attendance')
def mark_attendance():
    return render_template('attendance.html')

@app.route('/view_attendance')
def view_attendance():
    return render_template('view_attendance.html')

@app.route('/api/register', methods=['POST'])
def api_register():
    try:
        data = request.json
        name = data.get('name')
        student_id = data.get('student_id')
        
        if not name or not student_id:
            return jsonify({'success': False, 'message': 'Name and Student ID are required'}), 400
        
        # Capture face from webcam
        cap = cv2.VideoCapture(0)
        time.sleep(0.5)  # Give camera time to initialize
        ret, frame = cap.read()
        cap.release()
        
        if not ret or frame is None:
            return jsonify({'success': False, 'message': 'Failed to capture image. Please ensure your camera is connected and not being used by another application.'}), 400
        
        # Find face locations and encodings
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        
        if len(face_locations) == 0:
            return jsonify({'success': False, 'message': 'No face detected. Please try again.'}), 400
        
        if len(face_locations) > 1:
            return jsonify({'success': False, 'message': 'Multiple faces detected. Please ensure only one person is in frame.'}), 400
        
        # Get face encoding
        face_encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]
        
        # Store encoding
        face_encodings_db[student_id] = {
            'name': name,
            'encoding': face_encoding,
            'registered_at': datetime.now().isoformat()
        }
        save_face_encodings(face_encodings_db)
        
        # Save sample image
        student_dir = os.path.join(KNOWN_FACES_DIR, student_id)
        os.makedirs(student_dir, exist_ok=True)
        cv2.imwrite(os.path.join(student_dir, f'{student_id}.jpg'), frame)
        
        return jsonify({
            'success': True,
            'message': f'Successfully registered {name} (ID: {student_id})'
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/mark_attendance', methods=['POST'])
def api_mark_attendance():
    try:
        # Capture image from webcam
        cap = cv2.VideoCapture(0)
        time.sleep(0.5)  # Give camera time to initialize
        ret, frame = cap.read()
        cap.release()
        
        if not ret or frame is None:
            return jsonify({'success': False, 'message': 'Failed to capture image. Please ensure your camera is connected and not being used by another application.'}), 400
        
        # Convert to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        
        if len(face_locations) == 0:
            return jsonify({'success': False, 'message': 'No face detected'}), 400
        
        # Get face encodings from the frame
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        
        # Compare with known faces
        recognized_students = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(
                [data['encoding'] for data in face_encodings_db.values()],
                face_encoding,
                tolerance=0.6
            )
            
            face_distances = face_recognition.face_distance(
                [data['encoding'] for data in face_encodings_db.values()],
                face_encoding
            )
            
            best_match_index = np.argmin(face_distances) if len(face_distances) > 0 else None
            
            if best_match_index is not None and matches[best_match_index]:
                student_id = list(face_encodings_db.keys())[best_match_index]
                student_data = face_encodings_db[student_id]
                
                # Mark attendance
                today = datetime.now().strftime('%Y-%m-%d')
                attendance_file = os.path.join(ATTENDANCE_DIR, f'{today}.json')
                
                attendance_data = {}
                if os.path.exists(attendance_file):
                    with open(attendance_file, 'r') as f:
                        attendance_data = json.load(f)
                
                if student_id not in attendance_data:
                    attendance_data[student_id] = {
                        'name': student_data['name'],
                        'student_id': student_id,
                        'timestamp': datetime.now().isoformat(),
                        'status': 'Present'
                    }
                    
                    with open(attendance_file, 'w') as f:
                        json.dump(attendance_data, f, indent=2)
                    
                    recognized_students.append({
                        'name': student_data['name'],
                        'student_id': student_id,
                        'status': 'Present'
                    })
                else:
                    recognized_students.append({
                        'name': student_data['name'],
                        'student_id': student_id,
                        'status': 'Already marked'
                    })
        
        if recognized_students:
            return jsonify({
                'success': True,
                'students': recognized_students,
                'message': f'Attendance marked for {len(recognized_students)} student(s)'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Face not recognized. Please register first.'
            }), 404
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/attendance/<date>')
def api_get_attendance(date):
    try:
        attendance_file = os.path.join(ATTENDANCE_DIR, f'{date}.json')
        
        if os.path.exists(attendance_file):
            with open(attendance_file, 'r') as f:
                attendance_data = json.load(f)
            return jsonify({
                'success': True,
                'date': date,
                'attendance': list(attendance_data.values())
            })
        else:
            return jsonify({
                'success': True,
                'date': date,
                'attendance': []
            })
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/registered_students')
def api_registered_students():
    students = [
        {
            'student_id': sid,
            'name': data['name'],
            'registered_at': data['registered_at']
        }
        for sid, data in face_encodings_db.items()
    ]
    return jsonify({'success': True, 'students': students})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

