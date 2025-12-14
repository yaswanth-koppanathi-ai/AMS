# Attendance Management System Using Face Recognition

A comprehensive attendance management system that uses face recognition technology to automatically mark attendance. Built with Python, OpenCV, Flask, and Machine Learning.

## 🚀 Features

- **Automated Face Detection**: Uses OpenCV and face_recognition library for real-time face detection
- **Face Recognition**: Machine learning-based face recognition to identify registered students
- **Attendance Marking**: Automatically marks attendance when a recognized face is detected
- **Web Interface**: Beautiful, modern web UI built with Flask
- **Attendance Records**: View attendance history by date
- **Student Registration**: Easy registration process to add new students to the system
- **Smart Camera Detection**: Automatically detects and uses available cameras (supports multiple camera indices)
- **Robust Error Handling**: Retry logic and graceful error messages for camera access issues
- **Graceful Degradation**: Application runs even without face_recognition module installed (with clear error messages)

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
- **CMake** (required for installing face-recognition library on Windows)
- **Visual Studio Build Tools with C++** (required for building dlib dependency on Windows)

## 📦 Installation

1. **Clone or download this repository**

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   # or
   source .venv/bin/activate  # On Linux/Mac
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   **Important Notes:**
   - The application will run even if `face-recognition` is not installed, but face recognition features will be disabled
   - To enable face recognition on Windows, you need:
     1. **Install CMake**: Download from [cmake.org](https://cmake.org/download/) and add to PATH during installation
     2. **Install Visual Studio Build Tools**: Download from [Visual Studio](https://visualstudio.microsoft.com/visual-cpp-build-tools/) and select "Desktop development with C++" workload
     3. Restart your terminal after installing
     4. Then run: `pip install face-recognition`

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

   The application will start on `http://127.0.0.1:5000` and `http://0.0.0.0:5000`

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
AMS/
│
├── app.py                 # Main Flask application with camera capture logic
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── .gitignore            # Git ignore file
│
├── templates/            # HTML templates
│   ├── index.html        # Home page with navigation
│   ├── register.html     # Student registration page
│   ├── attendance.html   # Mark attendance page
│   └── view_attendance.html  # View records page
│
├── known_faces/          # Stored face images (auto-created)
│   └── {student_id}/     # Individual student directories
│       └── {student_id}.jpg  # Sample face image
│
├── attendance/           # Attendance records (auto-created)
│   └── YYYY-MM-DD.json  # Daily attendance files
│
└── face_encodings.pkl    # Face encoding database (auto-created)
```

### Key Functions in app.py:
- `find_available_camera()`: Auto-detects available camera indices
- `capture_image_from_camera()`: Robust camera capture with retry logic
- `load_face_encodings()`: Loads stored face encodings from pickle file
- `save_face_encodings()`: Saves face encodings to pickle file

## 🔧 How It Works

1. **Camera Detection & Capture**:
   - System automatically detects available cameras (tries indices 0, 1, 2)
   - Uses retry logic (3 attempts) to handle temporary camera locks
   - Properly initializes camera with optimal settings (640x480)
   - Reads multiple frames to ensure camera is warmed up and stable
   - Frontend properly releases camera before backend access to avoid conflicts

2. **Face Registration**:
   - When a student is registered, the system captures their face using OpenCV
   - Uses face_recognition library to generate a 128-dimensional face encoding
   - Validates that exactly one face is detected
   - Stores the encoding along with student information in `face_encodings.pkl`
   - Saves a sample image in `known_faces/{student_id}/` directory

3. **Face Recognition**:
   - When marking attendance, the system captures a new image
   - Generates face encodings for detected faces
   - Compares new encodings with stored encodings using Euclidean distance
   - Uses tolerance of 0.6 for matching
   - If a match is found, attendance is marked

4. **Attendance Storage**:
   - Attendance records are stored as JSON files, one per day in `attendance/` directory
   - Each record includes student ID, name, timestamp, and status
   - Prevents duplicate entries for the same student on the same day

## 🎓 Highlights

- **Real-world Application**: Solves a practical problem faced in educational institutions
- **Machine Learning Integration**: Demonstrates ML concepts in a practical application
- **Full-stack Development**: Combines backend (Flask), frontend (HTML/CSS/JS), and ML
- **Automated Process**: Reduces manual work and human error in attendance tracking

## ⚠️ Important Notes

- **Camera Access**: The system automatically detects and uses available cameras. If you have multiple cameras, it will try indices 0, 1, and 2.
- **Lighting**: Ensure good lighting when capturing faces for best results
- **Face Position**: Face should be clearly visible and front-facing
- **Single Face**: Only one face should be in frame during registration
- **Consistent Conditions**: The system works best with consistent lighting conditions
- **Processing Time**: First-time face recognition may take a moment to process
- **Camera Conflicts**: If camera is in use by another app, the system will retry automatically (up to 3 times)
- **Face Recognition Module**: The app runs without face_recognition installed, but face recognition features will show error messages until installed

## 🔒 Privacy & Security

- Face encodings are stored locally on your machine
- No data is sent to external servers
- All attendance records are stored locally
- You can delete the `known_faces` and `attendance` directories to remove all data

## 🐛 Troubleshooting

### **Issue**: Camera not working / "Failed to capture image"

**Solutions:**
- The system automatically retries (3 attempts), so wait a moment
- Ensure your camera is not being used by another application (close other apps using camera)
- Check browser permissions for camera access (allow camera access when prompted)
- The system auto-detects cameras - if you have multiple cameras, it tries indices 0, 1, 2 automatically
- Try refreshing the page and allowing camera access again
- On Windows, ensure no other application has exclusive camera access
- Check Windows Camera privacy settings: Settings → Privacy → Camera → Allow apps to access your camera

### **Issue**: Face not recognized

**Solutions:**
- Ensure good lighting conditions
- Make sure the face is clearly visible and front-facing
- Try registering again with better lighting/angle
- Ensure only one face is in the frame
- The system uses a tolerance of 0.6 - very different angles or lighting may affect recognition

### **Issue**: Installation errors / face-recognition module

**Solutions:**
- Make sure you have Python 3.8+ (Python 3.13 may have compatibility issues with pre-built wheels)
- Try upgrading pip: `pip install --upgrade pip setuptools wheel`
- **For Windows - Installing face-recognition:**
  1. Install CMake from [cmake.org](https://cmake.org/download/) - **IMPORTANT**: Check "Add CMake to system PATH" during installation
  2. Install Visual Studio Build Tools from [Visual Studio](https://visualstudio.microsoft.com/visual-cpp-build-tools/) - Select "Desktop development with C++" workload
  3. **Restart your terminal/IDE** after installing both
  4. Verify CMake: `cmake --version` (should show version)
  5. Then install: `pip install face-recognition`
- **Note**: The app works without face-recognition installed, but face recognition features will be disabled

### **Issue**: "No module named 'face_recognition'"

**Solutions:**
- This is expected if face-recognition is not installed
- The app will still run, but face recognition features will show error messages
- Follow the installation steps above to install face-recognition
- See the "Installation" section for detailed CMake and Visual Studio Build Tools requirements

### **Issue**: Camera index errors

**Solutions:**
- The system now auto-detects cameras automatically
- If you have multiple cameras, it tries indices 0, 1, 2 in order
- No manual configuration needed

## 📝 License

This project is open source and available for educational purposes.

## 👨‍💻 Development

This project was created as a demonstration of:
- Machine Learning application in real-world scenarios
- Full-stack web development
- Computer vision and face recognition
- RESTful API design
- Modern web UI/UX
- Robust error handling and retry mechanisms
- Camera access management and conflict resolution

## 🔄 Recent Improvements

- **Smart Camera Detection**: Automatic camera index detection (0, 1, 2)
- **Retry Logic**: 3-attempt retry mechanism for camera access
- **Better Error Handling**: Clear, descriptive error messages
- **Camera Warm-up**: Reads multiple frames to ensure stable capture
- **Frontend-Backend Coordination**: Proper camera release sequence to avoid conflicts
- **Graceful Degradation**: App runs without face_recognition module
- **Improved Camera Initialization**: Sets optimal resolution and allows proper warm-up time

---

**Built with ❤️ using Python, OpenCV, Flask, and Machine Learning**
