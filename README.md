# Attendance Management System Using Face Recognition

A comprehensive attendance management system that uses face recognition technology to automatically mark attendance. Built with Python, OpenCV, Flask, and Machine Learning.

## 🚀 Features

- **Automated Face Detection**: Uses OpenCV and face_recognition library for real-time face detection
- **Face Recognition**: Machine learning-based face recognition to identify registered students
- **Attendance Marking**: Automatically marks attendance when a recognized face is detected
- **Web Interface**: Beautiful, modern web UI built with Flask
- **Attendance Records**: View attendance history by date
- **Student Registration**: Easy registration process to add new students to the system

## 🛠️ Technology Stack

- **Python 3.8+**: Core programming language
- **OpenCV**: Computer vision and image processing
- **face_recognition**: Face recognition library (dlib-based)
- **Flask**: Web framework for backend API
- **Machine Learning**: Face encoding and recognition algorithms

## 📋 Prerequisites

- Python 3.8 or higher
- Webcam/Camera access
- pip (Python package manager)

## 📦 Installation

1. **Clone or download this repository**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   Note: If you encounter issues installing `face-recognition` on Windows, you may need to install Visual C++ Build Tools or use pre-compiled wheels.

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

## 🎯 Usage

### 1. Register a Student

1. Click on "Register Student" from the home page
2. Enter the student's full name and unique Student ID
3. Click "Register Student"
4. Allow camera access when prompted
5. Position the student's face clearly in front of the camera
6. The system will capture and register the face

### 2. Mark Attendance

1. Click on "Mark Attendance" from the home page
2. Click "Mark Attendance" button
3. Allow camera access when prompted
4. Position the student's face in front of the camera
5. The system will automatically detect and recognize the face
6. Attendance will be marked if the student is recognized

### 3. View Attendance

1. Click on "View Attendance" from the home page
2. Select a date from the date picker
3. Click "Load Attendance" to view records for that date
4. View statistics and detailed attendance records

## 📁 Project Structure

```
attendance-system/
│
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
│
├── templates/            # HTML templates
│   ├── index.html        # Home page
│   ├── register.html     # Student registration page
│   ├── attendance.html   # Mark attendance page
│   └── view_attendance.html  # View records page
│
├── known_faces/          # Stored face images (auto-created)
├── attendance/           # Attendance records (auto-created)
└── face_encodings.pkl    # Face encoding database (auto-created)
```

## 🔧 How It Works

1. **Face Registration**:
   - When a student is registered, the system captures their face
   - Uses face_recognition library to generate a 128-dimensional face encoding
   - Stores the encoding along with student information

2. **Face Recognition**:
   - When marking attendance, the system captures a new image
   - Generates face encodings for detected faces
   - Compares new encodings with stored encodings using Euclidean distance
   - If a match is found (within tolerance), attendance is marked

3. **Attendance Storage**:
   - Attendance records are stored as JSON files, one per day
   - Each record includes student ID, name, timestamp, and status

## 🎓 Highlights

- **Real-world Application**: Solves a practical problem faced in educational institutions
- **Machine Learning Integration**: Demonstrates ML concepts in a practical application
- **Full-stack Development**: Combines backend (Flask), frontend (HTML/CSS/JS), and ML
- **Automated Process**: Reduces manual work and human error in attendance tracking

## ⚠️ Important Notes

- Ensure good lighting when capturing faces
- Face should be clearly visible and front-facing
- Only one face should be in frame during registration
- The system works best with consistent lighting conditions
- First-time face recognition may take a moment to process

## 🔒 Privacy & Security

- Face encodings are stored locally on your machine
- No data is sent to external servers
- All attendance records are stored locally
- You can delete the `known_faces` and `attendance` directories to remove all data

## 🐛 Troubleshooting

**Issue**: Camera not working
- Ensure your camera is not being used by another application
- Check browser permissions for camera access
- Try refreshing the page

**Issue**: Face not recognized
- Ensure good lighting
- Make sure the face is clearly visible
- Try registering again with better lighting/angle

**Issue**: Installation errors
- Make sure you have Python 3.8+
- Try upgrading pip: `pip install --upgrade pip`
- For Windows, you may need Visual C++ Build Tools for face-recognition

## 📝 License

This project is open source and available for educational purposes.

## 👨‍💻 Development

This project was created as a demonstration of:
- Machine Learning application in real-world scenarios
- Full-stack web development
- Computer vision and face recognition
- RESTful API design
- Modern web UI/UX

---

**Built with ❤️ using Python, OpenCV, Flask, and Machine Learning**

